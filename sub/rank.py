  
import math
import ast
import asyncio
from datetime import datetime, timedelta, timezone
import discord
from discord.ext import tasks
import glob
import os
import psutil
import psycopg2
import psycopg2.extras
import random
import re
import traceback
import sub.box
import sub.calc

JST = timezone(timedelta(hours=+9), 'JST')

dsn = os.environ.get('DATABASE_URL')

class Postgres:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def execute(self, sql):
        self.cur.execute(sql)

    def fetch(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def fetchdict(self, sql):
        self.cur.execute (sql)
        results = self.cur.fetchall()
        dict_result = []
        for row in results:
            dict_result.append(dict(row))
        return dict_result

standard_set = "name,sex,id,lv,max_hp,now_hp,max_mp,now_mp,str,def,agi,stp,str_stp, def_stp, agi_stp,all_exp,now_exp,money"
standard_mobset = "name,id,lv,max_hp,now_hp,str,def,agi,img_url"

token = os.environ.get('TOKEN')
client = discord.Client()

admin_list = [
    715192735128092713,
    710207828303937626,
    548058577848238080,
]




getmagic_list = [
    "001|Heal",
    "002|FireBall",
    "003|StrRein",
    "004|DefRein",
    "005|AgiRein",
    "006|LifeConversion"


]

loop = asyncio.get_event_loop()
pg = Postgres(dsn)


def split_list(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return:
    """
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

def open_bord(ch, em_list):
    page_count = 0
    page_content_list = em_list
    first_em = page_content_list[0]
    send_message = await ch.send(embed=first_em)
    await send_message.add_reaction("🔷")
    await send_message.add_reaction("➕")
    reactions = ["➖","🔷","➕"]
    def react_check(reaction, user):
        if reaction.message.id != send_message.id:
            return 0
        if reaction.emoji in reactions:
            if user != m_author:
                return 0
            else:
                return reaction, user
    while not client.is_closed():
        try:
            reaction, user = await client.wait_for('reaction_add', check=react_check, timeout=20.0)
        except asyncio.TimeoutError:
            await send_message.clear_reactions()
            em = page_content_list[page_count]
            em.set_footer(text="※ページ変更待機終了済み")
            await send_message.edit(embed=em)
        else:
            if reaction.emoji == reactions[2] and page_count < len(page_content_list) - 1:
                page_count += 1
            if reaction.emoji == reactions[0] and page_count > 0:
                page_count -= 1
            if reaction.emoji == reactions[1]:
                await send_message.delete()
            if send_message:
                em = page_content_list[page_count]
                try:
                    await send_message.clear_reactions()
                    await send_message.edit(embed=em)
                except:
                    await ch.send("【報告】不明なエラーが発生。")
                else:
                    if page_count == 0:
                        for reaction in ["🔷","➕"]:
                            await send_message.add_reaction(reaction)
                    elif 0 < page_count and (len(page_content_list) - 1) > page_count:
                        for reaction in reactions:
                            await send_message.add_reaction(reaction)
                    elif page_count == len(page_content_list) - 1:
                        for reaction in ["➖","🔷"]:
                            await send_message.add_reaction(reaction)





def channel(ch):
    rank_list = []
    em_list = []
    result = pg.fetch("select id, lv from mob_tb order by lv desc;")[0:20]
    for data in result:
        id = data["id"]
        lv = data["lv"]
        channel = client.get_channel(id)
        print(id, channel)
        if channel:
            prace = channel.guild.name
        else:
            prace = "データ破損"
        rank_list.append((prace, lv))
    junni = 0
    rank_list = list(split_list(rank_list, 10))
    page = 0
    for i in rank_list:
        text = ""
        page += 1
        for data_set in i:
            junni += 1
            text += ( "\n" + f"[{junni}位]{data_set[0]} (Lv:{data_set[1]})")
        em = discord.Embed(
            title = f"ChannelRankingBord(page.{page})",
            description = text
        )
        em_list.append(em)
    open_bord(ch, em_list)
