import ast
import asyncio
import cv2
from datetime import datetime, timedelta, timezone
import math
import os
from random import random, randint, choice
import re
import sys

import discord
from discord.ext import tasks, commands
import psutil
import psycopg2, psycopg2.extras
import traceback

from sub import box, status, avatar, calc, battle

JST = timezone(timedelta(hours=+9), 'JST')

item_emoji_a = {
    1:"<:card:786514637289947176>",
    2:"<a:hp_potion_a:786982694479200336>",
    3:"<a:mp_potion_a:786982694839124021>",
    4:"<:soul_fire:786513145010454538>",
    5:"<a:toishi_a:786974865777229864>",
    6:"<:maseki:785641515561123921>",
    7:"<a:masuisyou_a:786982694948306974>",
    8:"<a:magic_coin_a:786966211594289153>"
}


client = pg = None
def first_set(c,p):
    global client, pg
    client = c
    pg = p

async def magic_1(player,mob):
    ch = mob.mob
    start_check = await battle.battle_start(player,mob)
    if start_check is False: return
    if player.now_mp < 30:
        em=discord.Embed(description="MPが不足…！")
        await ch.send(embed=em)
        return
    if random() <= 0.25:
        buff_num = 2
    else:
        buff_num = 0
    up_num = 0.8 + (player.magic_lv()/100000)
    player.magic_lv(1)
    # 戦闘処理（Player先手） #
    if player.AGI() >= mob.agi():
        text1 = battle.create_battle_text(player,mob,atk_word="『DrumFang』",str_up_num=up_num,buff=buff_num)
        text2 = battle.create_battle_text(mob,player)
    # 戦闘処理（Player後手） #
    else:
        text1 = battle.create_battle_text(mob,player)
        text2 = battle.create_battle_text(player,mob,atk_word="『DrumFang』",str_up_num=up_num,buff=buff_num)
    magic_log = f"```diff\n{text1}``````diff\n{text2}```"
    player.magic_lv(1)
    player.cut_mp(30)
    result_em,spawn_em,anti_magic_em = await battle.battle_result(player, mob)
    await ch.send(content=magic_log,embed=result_em)
    if spawn_em:await ch.send(embed=spawn_em)
    if anti_magic_em:await ch.send(embed=anti_magic_em)

# HealPrex #
async def magic_2(player,mob):
    ch = mob.mob
    start_check = await battle.battle_start(player,mob)
    if start_check is False: return
    if player.magic_lv() < 500:
        em=discord.Embed(description="魔法練度が不足…！")
        await ch.send(embed=em)
        return
    if player.now_mp < 80:
        em=discord.Embed(description="MPが不足…！")
        await ch.send(embed=em)
        return
    healing_amount = player.max_hp - player.now_hp
    if healing_amount <= 0:
        em=discord.Embed(description="まだ回復力が無いようだ…")
        await ch.send(embed=em)
        return
    players = mob.battle_players
    players.remove(player.ID())
    if players == []:
        em=discord.Embed(description="回復出来る人が居ないようだ…")
        await ch.send(embed=em)
        return
    heal_text = ""
    for id in players:
        p = box.players[id]
        p.now_hp += healing_amount
        if p.now_hp > p.max_hp: p.now_hp = p.max_hp
        heal_text += f"\n<@{p.user.id}> のHPを{healing_amount}回復！"
    em=discord.Embed(title="HealPrex",description=heal_text)
    await ch.send(embed=em)
    player.magic_lv(1)
    player.cut_mp(80)
    
        
# FlecteImpetus #
async def magic_3(player,mob):
    ch = mob.mob
    start_check = await battle.battle_start(player,mob)
    if start_check is False: return
    if player.magic_lv() < 1000:
        em=discord.Embed(description="魔法練度が不足…！")
        await ch.send(embed=em)
        return
    if player.now_mp < 130:
        em=discord.Embed(description="MPが不足…！")
        await ch.send(embed=em)
        return
    if player.ID() in box.atk_switch:
        em=discord.Embed(description="既に発動しているようだ…")
        await ch.send(embed=em)
        return
    box.atk_switch[mob.ID()] = player.ID()
    magic_text = f"次の{mob.name}の攻撃対象が<@{player.ID()}>になった！"
    em=discord.Embed(title="FlecteImpetus",description=magic_text)
    await ch.send(embed=em)
    player.magic_lv(1)
    player.cut_mp(130)
        
# UnMagicParry #
async def magic_4(player,mob):
    ch = mob.mob
    start_check = await battle.battle_start(player,mob)
    if start_check is False: return
    parry_percent = min(((player.now_defe/mob.STR()-1) if player.now_defe>0 else 0), 0.75)
    if random() <= parry_percent:
        player.now_defe = player.max_defe
        text1 = battle.create_battle_text(mob,player,parry=True)
    else:
        text1 = battle.create_battle_text(mob,player)
    text2 = battle.create_battle_text(player,mob,atk_word="『UnMagicParry』",str_up_num=up_num,buff=buff_num)
    magic_log = f"```diff\n+ {player.name} は防御姿勢をとった…``````diff\n{text1}``````diff\n{text2}```"
    result_em,spawn_em,anti_magic_em = await battle.battle_result(player, mob)
    await ch.send(content=magic_log,embed=result_em)
    if spawn_em:await ch.send(embed=spawn_em)
    if anti_magic_em:await ch.send(embed=anti_magic_em)

# PyrobolusLacrima #
async def magic_5(player,mob):
    pass


async def open_magic(user,ch):
    player = box.players[user.id]
    magic_em = discord.Embed(title="Player Magic Board",description="各魔法の数値は熟練度による補正を加算済みです。")
    magic_em.add_field(name="`1.`DrumFang",value=f"必要熟練度.**0**\n消費MP.**30**\n攻撃力**{80+(player.magic_lv()/1000)}**%の攻撃魔法 **25**%で敵に**5**ターンNerf付与 ",inline=False)
    magic_em.add_field(name="`2.`HealPrex",value=f"必要熟練度.**500**\n消費MP.**80**\n自分が受けているダメージ量 戦闘に参加している他のプレイヤーのHPを回復",inline=False)
    magic_em.add_field(name="`3.`FlecteImpetus",value=f"必要熟練度.**1000**\n消費MP.**130**\n次に味方が受ける攻撃を肩代わり",inline=False)
    magic_em.set_thumbnail(url=user.avatar_url)
    await ch.send(embed=magic_em)

async def use_magic(user,ch,magic):
    player = box.players[user.id]
    mob = box.mobs[ch.id]
    if magic in ["1","DrumFang","DM"]:
        await magic_1(player,mob)
    if magic in ["2","HealPrex","HP"]:
        await magic_2(player,mob)
    if magic in ["3","FlecteImpetus","FI"]:
        await magic_3(player,mob)
    if magic in ["4","UnMagicParyy","UMP"]:
        await magic_4(player,mob)
