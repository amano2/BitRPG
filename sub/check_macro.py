import ast
import asyncio
import cv2
from datetime import datetime, timedelta, timezone
import math
import os
import random
import re
import sys

import discord
from discord.ext import tasks, commands
import psutil
import psycopg2, psycopg2.extras
import traceback

from sub import box, status
from anti_macro import anti_macro


doubt_count = {}
macro_checking = []

client = pg = None
def first_set(c,p):
    global client, pg
    client = c
    pg = p

async def check_macro(user, ch):
    P_list = pg.fetch(f"select * from player_tb where id = {user.id};")
    if not user.id in doubt_count:
        doubt_count[user.id] = 0
    check_flag = True
    result = False
    while check_flag == True:
        flag = await ch.send("デデドン！！")
        await asyncio.sleep(1)
        check_id = flag.id
        macro_checking.append(user.id)
        img, num = await anti_macro.get_img(client)
        cv2.imwrite('anti_macro/num_img/temp.png', img)
        check_em = discord.Embed(
            title = "マクロ検知ぃいい！！(迫真)",
            description=f'{user.mention}さんのマクロチェックです(突然の冷静)\n以下の画像に書かれている数字を20秒以内に**半角**で送信してください\n※`CheckID『{check_id}』`')
        check_em.set_image(url="attachment://temp.png")
        check_msg = await ch.send(embed=check_em,file=discord.File(fp="anti_macro/num_img/temp.png"))
        def check(m):
            if not m.author.id == user.id or m.channel.id != ch.id:
                return 0
            if not m.content in ['0','1','2','3','4','5','6','7','8','9']:
                return 0
            return 1
        try:
            answer = await client.wait_for('message', timeout=20, check=check)
        except asyncio.TimeoutError:
            doubt_count[user.id] += 1
            temp = None
            await ch.send(f'無回答!!　不正カウント+1(現在{doubt_count[user.id]})')
            result = False
        else:
            temp = answer.content
            if int(answer.content) == int(num):
                await ch.send(f'正解!!\nアイテム配布: 魔石×10')
                status.get_item(user, 6, 10)
                check_flag = False
                result = True
            elif str(num) != str(answer.content):
                doubt_count[user.id] += 1
                await ch.send(f'不正解!! 不正カウント+1(現在{doubt_count[user.id]})')
                result = False
        print(f"MacroCheck：({user.id}) TrueAnswer[{num}], UsersAnswer[{temp}]")
        embed=discord.Embed(title="マクロ検知ログ", color=0x37ff00)
        embed.add_field(name="CheckID", value=check_id, inline=False)
        embed.add_field(name="Result", value=result, inline=False)
        embed.add_field(name="MissNum", value=doubt_count[user.id], inline=False)
        if len(str(P_list)) <= 1024:
            embed.add_field(name="UserData", value=str(P_list), inline=False)
        embed.set_image(url="attachment://temp.png")
        await client.get_channel(763299968353304626).send(embed=embed, file=discord.File(fp="anti_macro/num_img/temp.png"))
        macro_checking.remove(user.id)
        if doubt_count[user.id] >= 3:
            check_flag = False
            await ch.send(f'不正カウントが規定量に達しました。ログを送信します。')
            await client,get_channel(799960054840557618).send(embed)
        return result
