import ast
import asyncio
import cv2
from datetime import datetime, timedelta, timezone
import math
import os
import random
import re
import signal
import sys

def handler(signum, frame):
    loop = asyncio.get_event_loop()
    loop.create_task(client.change_presence(activity=discord.Game(name=f"今から落ちるよ…")))

signal.signal(signal.SIGTERM, handler)

import discord
from discord.ext import tasks, commands
import psutil
import psycopg2, psycopg2.extras
import traceback

from sub import (
    avatar,
    battle,
    box,
    check_macro,
    help,
    magic_wolf,
    magic_armadillo,
    magic_orca,
    rank,
    shop,
    status,
    training,
)



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


def inverse_lookup(d, x):
    for k,v in d.items():
        if x == v:
            return k

def split_n(text, n):
    return [ text[i*n:i*n+n] for i in range(len(text)/n) ]


# 時間軸、データベースのURL、ボットのToken、Client、pg変数設定
JST = timezone(timedelta(hours=+9), 'JST')
dsn = os.environ.get('DATABASE_URL')
token = os.environ.get('TOKEN')
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix="^^")
pg = Postgres(dsn)
shop.pg, battle.pg, rank.pg, status.pg, avatar.pg, check_macro.pg = pg, pg, pg, pg, pg, pg
shop.client = battle.client = rank.client = status.client = help.client = avatar.client = check_macro.client = magic_wolf.client = magic_armadillo.client = magic_orca = client


# コマンド使用中のチャンネル
cmd_lock = {}

# 公式鯖ID
official_guild_id = 719165196861702205

# 役職別ID
announce_role = 719176372773453835
c_lv1 = 763640405534441472
c_lv2 = 743323912837922906
c_lv3 = 743323569668227143
c_lv4 = 719165979262844998
c_lv5 = 719165521706352640

ID = 763635688234942475
role_id = {
    "1️⃣":719176372773453835,
    "2️⃣":763640405534441472,
    "3️⃣":743323912837922906,
    "4️⃣":743323569668227143
}

"""
create table player_tb(
    id bigint,
    lv bigint,
    max_lv bigint, max_exp bigint,
    now_exp bigint, now_stp bigint,
    str_p bigint, def_p bigint, agi_p bigint,
    magic_class int, magic_lv bigint,
    kill_count bigint, item jsonb, money bigint,
    primary key (id)
)

"""

#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"起動中…"))
    loop.start()
    player_ids = [ i["id"] for i in pg.fetchdict("select id from player_tb order by lv desc;")]
    for player_id in player_ids:
        if client.get_user(player_id):
            player = avatar.Player(client, player_id)
            box.players[player_id] = player
            print("Playerデータ挿入： ",player.user,"\n",player.dtd.values())
    print(len(player_ids), len(box.players))
    p_num_result = (len(player_ids)==len(box.players))
    desc = (
          f"\n+Prefix『^^』"
        + f"\n+Server『{len(client.guilds)}』"
        + f"\n+Player『{p_num_result} {len(box.players)}』"
    )
    embed = discord.Embed(title="起動ログ", description=f"```diff\n{desc}```")
    embed.timestamp = datetime.now(JST)
    ch = client.get_channel(784271793640833035)
    await ch.send(embed = embed)
    print("""
⬛⬛⬛⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬛⬛⬛⬛⬜
⬛⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬛⬜⬜⬜⬛
⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬜⬜
⬛⬛⬛⬛⬜⬜⬜⬛⬜⬛⬛⬛⬛⬛⬜⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬛⬛⬜⬛⬛⬜⬛⬛⬛⬛
⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬜⬜⬛⬛⬜⬜⬜⬛⬛
⬛⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬛
⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬛⬛
⬛⬛⬛⬛⬜⬜⬜⬛⬜⬜⬜⬛⬛⬛⬜⬛⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜
    """)

#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

@tasks.loop(seconds=10)
async def loop():
    MEM = psutil.virtual_memory().percent
    sub_msg = '^^start'
    if client.get_channel(761571389345759232).name=='true':
        sub_msg = "開発作業中"
    await client.change_presence(activity=discord.Game(name=f"{sub_msg}￤{len(client.guilds)}server"))

#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

@client.event
async def on_guild_join(guild):
    log_ch = client.get_channel(752551728553132102)
    embed = discord.Embed(
        title="BitRPG導入ログ",
        description=f"{guild.name}({guild.id})が導入\n現在の導入数：{len(client.guilds)}"
    )
    embed.timestamp=datetime.now(JST)
    await log_ch.send(embed=embed)

@client.event
async def on_guild_remove(guild):
    log_ch = client.get_channel(752551728553132102)
    embed = discord.Embed(
        title="BitRPG撤去ログ",
        description=f"{guild.name}({guild.id})が撤去\n現在の導入数：{len(client.guilds)}"
    )
    embed.timestamp=datetime.now(JST)
    await log_ch.send(embed=embed)

#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
#➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

@client.event
async def on_message(message):
    global cmd_lock, macro_checking, doubt_count

    m_ctt = message.content
    m_em = message.embeds
    m_id = message.id
    m_ch = message.channel
    m_guild = message.guild
    m_author = message.author


    if m_ctt.startswith("^^") and not m_author.id in check_macro.macro_checking and not m_author.bot:

        if cmd_lock.get(m_ch.id) is True:
            cmd_em = discord.Embed(description="コマンド処理中。終わらない場合は`><fix`。")
            await m_ch.send(embed=cmd_em)
            return

        if m_ctt == '^^start':
            print("^^start: ",m_author)
            id_list = [ i["id"] for i in pg.fetchdict("select id from player_tb;")]
            print(id_list)
            def check(m):
                if not m.author.id == m_author.id: return 0
                return 1
            def check2(m):
                if not m.author.id == m_author.id: return 0
                if not m.content in ("y","Y","n","N"): return 0
                return 1
            if m_author.id in id_list:
                msg_em = discord.Embed(description="【警告】登録済みです。全てのデータを消して再登録しますか？ \nyes -> y\nno -> n")
                await m_ch.send(embed=msg_em)
                try:
                    msg = await client.wait_for("message", timeout=60, check=check)
                except asyncio.TimeoutError:
                    msg_em = discord.Embed(description="キャセルン！！")
                    await m_ch.send(embed=msg_em)
                    return
                else:
                    if msg.content in ("y","Y"):
                        msg_em = discord.Embed(description="再登録を致します。")
                        await m_ch.send(embed=msg_em)
                        magic_type_flag = True
                        pg.execute(f"delete from player_tb where id = {m_author.id}")
                    else:
                        return
            msg_em = discord.Embed(description=f"{m_author.mention}さんの冒険者登録を開始。")
            await m_ch.send(embed=msg_em)
            magic_type_flag = False
            while not magic_type_flag is True:
                magic_type_em = discord.Embed(
                    title=f"{m_author.name} の所属魔法領域を選択",
                    description=("所属する魔法領域の対応番号を半角英数字で送信してください 再選択は出来ません")
                )
                magic_type_em.add_field(name="1:Wolf",value="`火力特化`")
                magic_type_em.add_field(name="2:Armadillo",value="`防御特化`")
                magic_type_em.add_field(name="3:Orca",value="`テクニカル性特化`")
                await m_ch.send(embed=magic_type_em)
                try:
                    msg = await client.wait_for("message", timeout=60, check=check)
                except asyncio.TimeoutError:
                    msg_em = discord.Embed(description=f"時間切れです もう一度`^^start`でやり直して下さい ")
                    await m_ch.send(embed=msg_em)
                    break
                else:
                    respons = int(msg.content) if msg.content in ("1","2","3") else 0
                    if not respons in (1,2,3):
                        msg_em = discord.Embed(description=f"`1,2,3`で答えて下さい ")
                        await m_ch.send(embed=msg_em)
                        continue
                    select_magic_type = "Wolf" if respons==1 else "Armadillo" if respons==2 else "Orca" 
                    msg_em = discord.Embed(description=f"『{select_magic_type}』で宜しいですか？\nyes -> y\nno -> n")
                    await m_ch.send(embed=msg_em)
                    try:
                        msg = await client.wait_for("message", timeout=10, check=check2)
                    except asyncio.TimeoutError:
                        msg_em = discord.Embed(description=f"時間切れです もう一度`^^start`でやり直して下さい")
                        await m_ch.send(embed=msg_em)
                        break
                    else:
                        if msg.content in ("y","Y"):
                            msg_em = discord.Embed(description=f"『{select_magic_type}』で登録します")
                            await m_ch.send(embed=msg_em)
                            magic_type_flag = True
                        elif msg.content in ("n","N"):
                            msg_em = discord.Embed(description=f"魔法領域の選択画面に戻ります")
                            await m_ch.send(embed=msg_em)
                            break
            if not magic_type_flag == True:
                return
            jsonb_items = "'冒険者カード',1, 'HP回復薬',10, 'MP回復薬',10, 'HP全回復薬',1, 'MP全回復薬',1, '魔石',1, '魂の焔',0, '砥石',0, '魔晶',0, '魔硬貨',0"
            cmd = (
                f"INSERT INTO player_tb VALUES ("
                +f"{m_author.id},1,1000,1,1,10,1,1,1,{respons},0,0,jsonb_build_object({jsonb_items}),0"
                +");"
            )
            print(f"NewPlayer：{m_author}({m_author.id}),{select_magic_type}")
            try:
                pg.execute(cmd)
            except Exception as e:
                await m_ch.send('type:' + str(type(e)), '\nargs:' + str(e.args), '\ne自身:' + str(e))
            else:
                emojis = status.items_emoji_a
                msg_em = discord.Embed(description=f"<@{m_author.id}> さんの冒険者登録が完了しました\nアイテム配布： 冒険者カード{emojis[1]}×1 HP回復薬{emojis[2]}×10 MP回復薬{emojis[3]}×10 魔石{emojis[6]}×1")
                await m_ch.send(embed=msg_em)
            player = avatar.Player(client, m_author.id)
            if m_author.id in id_list:
                del box.players[m_author.id]
            box.players[m_author.id] = player
            await status.open_status(m_author, m_ch)
            await help.help(m_ch, m_author)
            msg_em = discord.Embed(
                title="初期行動リスト",
                description=(
                    f"・`^^help`でHelpページの確認"
                    + f"\n・`^^url`で公式サーバーに参加"
                    + f"\n・`^^tr`でトレーニングをし、まずはLv2を目指す"
                    + f"\n・`^^status`で上がったステータスを確認"
                    + f"\n・`^^item 冒険者カード`で上がったステータスを確認"
                    + f"\n・`^^item`で所持アイテムを確認"
                    + f"\n・`^^point str 10`でLvUPで手に入ったSTPでStrength(攻撃力)を強化"
                    + f"\n・適当なLv１チャンネルで`^^attack`"
                    + f"\n・`^^magic`で自分の魔法を確認"
            ))
            await m_author.send(embed=msg_em)
            msg_em = discord.Embed(
                title="開発者から挨拶",
                description=(
                    ". こんにちは。BitRPG2代目開発者の**Sakuraga**です。この度は**BitRPG**にご登録いただきまことにありがとうございます。"
                    + "\n　**BitRPG**は知名度の高い**TAO**や**ReStart**と異なり、**プレイヤー間の協力と戦略**に視点を向けたRPGです。敵との戦闘においても、個々人の性能だけで戦うのには限度があります。"
                    + "魔法領域の性能面も各々がかなり偏っており、個人戦闘には基本向きません。ですが仮に敵一体に**Wolf・Armadillo・Orca**の３人で挑めば、勝率や戦略性が広がります。"
                    + "まずは`^^url`で、公式サーバーに参加し、BitRPGの遊び方を覚えるとともに他のPlayerと関係を築くことをお勧めします。"
                    + "\n　`【追記】\nBitRPGは比較的入り組んだデザインをしており、Playerによっては名前の長さ上、見栄えが悪くなるような不自然な改行などが発生することがございます。"
                    + "極力そのようなことがないようデザインに力を注いではいるのですが、念のためスマホ版Discordを使用している方は、`設定->テーマ`から、テキストサイズを90%以下（80%推奨）に設定し直しますようお願いいたします。`"
            ))
            await m_author.send(embed=msg_em)
        if client.get_channel(761571389345759232).name=='true':
            guild = client.get_guild(official_guild_id)
            if not m_author in guild.members:
                msg_em = discord.Embed(description=f"現在開発作業中につき、ClearanceLv3未満のプレイヤーのコマンド使用を制限しています。")
                await m_ch.send(embed=msg_em)
                return
            user_roles = [i.name for i in guild.get_member(m_author.id).roles]
            clearance_lv3_user = "Clearance-Lv3" in user_roles
            clearance_lv4_user = "Clearance-Lv4" in user_roles
            clearance_lv5_user = "Clearance-Lv5" in user_roles
            if not clearance_lv3_user or not clearance_lv4_user or not clearance_lv5_user:
                msg_em = discord.Embed(description=f"現在開発作業中につき、ClearanceLv3未満のプレイヤーのコマンド使用を制限しています。")
                await m_ch.send(embed=msg_em)
                return

        cmd_lock[m_ch.id] = True
        mob = avatar.Mob(client, m_ch.id)

        try:
            if random.random() <= 0.005:
                result = await check_macro.check_macro(client, m_author, m_ch)
                if not result:
                    return

            cmd_list = ["^^help","^^st","^^status","^^point","^^attack","^^atk","^^rank","^^item","^^reset","^^re"]
            if not m_author.id in box.players:
                id_list = [ i["id"] for i in pg.fetchdict("select id from player_tb;")]
                if m_author.id in id_list:
                    msg_em = discord.Embed(description=f"<@{m_author.id}>のデータがプレイヤー一覧に入っていませんでした。強制的に挿入します。")
                    await m_ch.send(embed=msg_em)
                    player = avatar.Player(client, m_author.id)
                    box.players[m_author.id] = player
                else:
                    msg_em = discord.Embed(description=f"<@{m_author.id}>は冒険者登録をしていません。`^^start`で登録してください。")
                    await m_ch.send(embed=msg_em)
                    return


            # URL #
            if m_ctt == "^^url":
                print("^^url: ",m_author)
                await m_ch.send(embed=discord.Embed(
                    title="Invite & Other URL",
                    description="▶︎[BitRPGBot招待](https://discord.com/api/oauth2/authorize?client_id=715203558357598240&permissions=8&scope=bot)\n▶︎[公式鯖参加](https://discord.gg/NymwEUP)\n"
                ))


            # ヘルプ #
            if m_ctt == "^^help":
                await help.help(m_author, m_ch)


            # ステータスの表示 #
            if m_ctt.startswith("^^st"):
                print("^^st: ",m_author)
                temp = m_ctt
                pattern = r"\^\^(st|status|st (.+)|status (.+))$"
                result = re.search(pattern, temp)
                if result:
                    await status.open_status(m_author, m_ch)


            # 戦闘 #
            if m_ctt.startswith("^^attack") or m_ctt.startswith("^^atk"):
                print("^^atk: ",m_author)
                temp = m_ctt
                pattern = r"\^\^(atk|attack|atk (.+)|attack (.+))$"
                result = re.search(pattern, temp)
                if result: await battle.cbt_proc(m_author,m_ch)

            # アイテム #
            if m_ctt.startswith("^^m"):
                print("^^magic: ",m_author)
                pattern = r"^\^\^(m|magic) (.+)"
                pattern2 = r"^\^\^(m|magic)$"
                result = re.search(pattern, m_ctt)
                result2 = re.search(pattern2, m_ctt)
                if result:await battle.use_magic(m_author,m_ch,result.group(2))
                elif result2:await battle.open_magic(m_author,m_ch)

            # 戦闘から離脱 #
            if m_ctt.startswith("^^re"):
                print("^^re: ",m_author)
                temp = m_ctt
                pattern = r"^\^\^(re|reset|reset (.+)|re (.+))$"
                result = re.search(pattern, temp)
                if result: await battle.reset(m_author, m_ch)


            # training #
            if m_ctt.startswith("^^tr"):
                print("^^training: ",m_author)
                temp = m_ctt
                pattern = r"^\^\^(tr|training|training (.+)|tr (.+))$"
                result = re.search(pattern, temp)
                if result:
                    training.client, training.pg = client, pg
                    await training.abc_training(m_author, m_ch)


            # STPの振り分け #
            if m_ctt.startswith("^^point"):
                print("^^point: ",m_author)
                pattern = r"\^\^point (str|STR|def|DEF|agi|AGI) (\d{1,})$"
                result = re.search(pattern, m_ctt)
                if result: await status.divid(m_author, m_ch, result)


            # レベルランキングの表示 #
            if m_ctt == "^^ranking":
                print("^^ranking: ",m_author)
                ranking = rank.RankClass(client)
                ranking.channel(m_author,m_ch)


            # アイテム #
            if m_ctt.startswith("^^i"):
                print("^^item: ",m_author)
                pattern = r"\^\^(i|item) (.+)"
                pattern2 = r"\^\^(i|item)$"
                result = re.search(pattern, m_ctt)
                result2 = re.search(pattern2, m_ctt)
                if result:await status.use_item(m_author, m_ch, result.group(2))
                elif result2: await status.open_inventory(m_author, m_ch)


            # Lv上限解放 #
            if m_ctt == "^^lvunlock":
                print("^^lvunlock: ",m_author)
                await status.up_max_lv(m_author, m_ch)


            # shop #
            if m_ctt == "^^shop":
                print("^^shop: ", m_author)
                await shop.shop(m_author, m_ch)

        finally:
            cmd_lock[m_ch.id] = False


    if not m_author.bot:
        if m_ctt.startswith('><embed '):
            pattern = r'^><embed "(.+)" "(.+)"'
            result = re.match(pattern,m_ctt)
            if result:
                await m_author.send(m_ctt)
                await message.delete()
                embed = discord.Embed(title=result.group(1),description=result.group(2))
                await m_ch.send(embed=embed)
        if m_ctt == '><report':
            embed = discord.Embed(
                title = '<Safe> -YUI- will help you!!',
                description = (
                    'こんにちは、開発者代理の**天乃 結**です!'
                    +'\nレポート確認開始! 今から5分間待つから、その間にレポートをできるだけ詳しく書いて送信してね。'
                    +'\n最初のメッセージしか送信しないから注意してね。ちなみに画像も一緒に送信できるよd(˙꒳˙* )'))
            # embed.set_footer(text='待機中…')
            await m_ch.send(embed=embed)
            def check(m):
                if m.author.id != m_author.id:
                    return 0
                if m.channel.id != m_ch.id:
                    return 0
                return 1
            try:
                re_m = await client.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                await m_ch.send('これ以上待てないよォ…\n5分以内で終わらない時は、先にまとめてかららコピペして送信するといいよ!')
            else:
                ans = re_m.content
                atch = None
                if re_m.attachments:
                    atch = re_m.attachments
                re_em = discord.Embed(description=ans)
                re_em.set_author(name=m_author)
                await client.get_channel(761516423959805972).send(embed=re_em, file=atch)
                await m_ch.send('レポートありがとう!')


        if m_ctt == '><fix':
            embed = discord.Embed(
                title = '<Safe> -YUI- will help you!!',
                description = (
                    'こんにちは、開発者代理の**天乃 結**です!'
                    +'\n私が来たからにはもう大丈夫、大体のバグを強制的に治しちゃうよ!'
                    +'\n診断していくから`y, n`で答えてね!'))
            await m_ch.send(embed=embed)
            def check(m):
                if m.author.id != m_author.id: return 0
                if m.channel.id != m_ch.id: return 0
                if not m.content in ('y','n'): return 0
                return 1
            if m_ch.id in cmd_lock:
                em = discord.Embed(description='もしかしてコマンド処理が終わらないんじゃない?\n`y/n`')
                await m_ch.send(embed=em)
                try:
                    re_m = await client.wait_for('message', timeout=60, check=check)
                except asyncio.TimeoutError:
                    await m_ch.send('答えないんなら次行くね?')
                else:
                    answer = re_m.content
                    if answer == 'y':
                        cmd_lock[m_ch.id] = False
            embed = discord.Embed(description='これで全部かな?\nお待たせしてごめんね、修理完了したよ!\n今後ともBitRPGをよろしく!!')
            await m_ch.send(embed=embed)



    if m_ctt == "SystemCall":
        m_ctt = m_ctt.split("SystemCall")[1].strip("\n")
        guild = client.get_guild(official_guild_id)
        user_is_c_lv2 = guild.get_role(c_lv3).get_role(c_lv2) in m_author.roles
        user_is_c_lv3 = guild.get_role(c_lv3) in guild.get_member(m_author.id).roles
        user_is_c_lv4 = guild.get_role(c_lv4) in guild.get_member(m_author.id).roles
        user_is_c_lv5 = guild.get_role(c_lv5) in guild.get_member(m_author.id).roles
        if not user_is_c_lv4 and not user_is_c_lv5:
            clv = 3 if user_is_c_lv3 else 2 if user_is_c_lv2 else 1
            await m_ch.send(f"*<@{m_author.id}> is CrealanceLv{clv}. You need at least ClearanceLv4 to call the system.*")
            return
        else:
            clv = 5 if user_is_c_lv5 else 4
            await m_ch.send(f"*<@{m_author.id}> is CrealanceLv{clv}. System was already came.*")
            def check(m):
                if m.author.id != m_author.id: return 0
                if m.channel.id != m_ch.id: return 0
                return 1
            try:
                remsg = await client.wait_for("message", check=check)
            except:
                pass
            else:
                ctt = remsg.content
                try:
                    if ctt.startswith("psql "):
                        cmd = ctt.split("psql ")[1]
                        await m_ch.send(f"`::DATABASE=> {cmd}`")
                        result = None
                        if "select" in cmd:
                            result = f"{pg.fetch(cmd+' LIMIT 10')}\n(DataCount『{len(pg.fetch(cmd))}』)"
                        else:
                            try:
                                pg.execute(cmd)
                            except Exception as error:
                                result = f"{error}"
                            else:
                                result = True
                        try:
                            await m_ch.send(f"```py\n{result}```")
                        except:
                            await m_ch.send("Error.")
                    if ctt.startswith("excec "):
                        cmd = ctt.split("excec ")[1]
                        await m_ch.send(f"`::python=>{cmd}`")
                        try:
                            excec(cmd)
                        except:
                            result = False
                        else:
                            retult = True
                        await m_ch.send(result)
                        
                finally:
                    await m_ch.send("*Completed. System was already closed.*")



@bot.command()
async def getrole(ctx, num):
    if ctx.message.channel.id != 725486353151819899:
        await ctx.send("このコマンドは<@725486353151819899>専用です。")
        return
    await ctx.message.delete()
    annouce_role = ctx.guild.get_role(announce_role)
    c_lv1 = ctx.guild.get_role(c_lv1)
    c_lv2 = ctx.guild.get_role(c_lv2)
    c_lv3 = ctx.guild.get_role(c_lv3)
    role = announce_role if num=="0" else c_lv1 if num=="1" else c_lv2 if num=="2" else c_lv3 if num=="3" else None
    result_msg = "該当する役職がありません。"
    if role:
        await ctx.message.author.add_role(role)
        result_msg = f"<@{role.id}> を付与しました。"
    send_msg = await ctx.send(result_msg)
    await asyncio.sleep(5)
    await send.msg.delete()



@bot.command()
async def remrole(ctx, role_num):
    if not ctx.message.channel.id == 725486353151819899:
        await ctx.send("このコマンドは<@725486353151819899>専用です。")
        return
    await ctx.message.delete()
    annouce_role = ctx.guild.get_role(announce_role)
    c_lv1 = ctx.guild.get_role(c_lv1)
    c_lv2 = ctx.guild.get_role(c_lv2)
    c_lv3 = ctx.guild.get_role(c_lv3)
    role = announce_role if num=="0" else c_lv1 if num=="1" else c_lv2 if num=="2" else c_lv3 if num=="3" else None
    result_msg = "該当する役職がありません。"
    if role:
        await ctx.message.author.add_role(role)
        result_msg = f"<@{role.id}> を解除しました。"
    send_msg = await ctx.send(result_msg)
    await asyncio.sleep(5)
    await send.msg.delete()



client.run(token)
