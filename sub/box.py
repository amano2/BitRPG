from collections import namedtuple

# ※全要素をkey->idで管理するように!!
players = {}
mobs = {}
weapons = {}

# デバフ　バフ系
stun = {}
nerf = {}
power_charge = {}
magic_charge = {}
atk_switch = {}
anti_magic = []
exp_up_buff = []
fleez = []

#gui emoji
menu_emojis = {
    "left":"<:left:800980952461213706>",
    "close":"<:close:800980952414158908>",
    "right":"<:right:800980952426741770>",
    "buy_mode":"<:buy_mode:801006516185858078>"
}

menu_emojis2 = {
    "left2":"<:left2:803184312954126357>",
    "left":"<:left:800980952461213706>",
    "close":"<:close:800980952414158908>",
    "right":"<:right:800980952426741770>",
    "right2":"<:right2:803184312702074922>",
    "create_mode":"<:create_mode:802203960772919316>"
}

gauge_emoji = {
    "hp_head":"<:emoji_25:804370116409032704>",
    "hp_full":"<:emoji_23:804366539284807680>",
    "hp_half":"<:emoji_24:804369368196579370>",
    "hp_empty":"<:emoji_31:804616997932892231>",
    "hp_end_full":"<:emoji_26:804486128450928691>",
    "hp_end_empty":"<:emoji_27:804486160621371483>",
    "defe_full":"<:emoji_28:804490050935062528>",
    "defe_half":"<:emoji_29:804490083478536263>",
    "defe_empty":"<:emoji_30:804490107574943765>",
}

damaged_gauge_emoji = {
'hp_joit':'<:emoji_36:804843054015840307>',
'hp_half':'<:emoji_38:804844577156497438>',
'hp_full':'<:emoji_37:804843399902920714>',
'hp_end_full':'<:emoji_35:804843027586875474>',
}

# items_~ #
items_name = {
    1:"冒険者カード",
    2:"HP回復薬",3:"MP回復薬",
    4:"魂の焔",
    5:"砥石",6:"魔石",7:"魔晶",8:"魔硬貨",
    9:"HP全回復薬",10:"MP全回復薬",
    11:'キャラメル鉱石',12:'キャラメル鋼',
    13:'ブラッド鉱石',14:'ブラッド鋼',
    15:'ゴールド鉱石',16:'ゴールド鋼',
    17:'ダーク鉱石',18:'ダーク鋼',
    19:'ミスリル鉱石',20:'ミスリル鋼',
    21:'オリハルコン鉱石',22:'オリハルコン鋼',
    23:"鉄",24:"黒色酸化鉄",
    25:"ハンマー",26:"型枠-インゴット",27:"型枠-武器強化チップ",
    28:"炭素粉末",29:"カーボンプレート",30:"カーボンチップ",
}

items_id = {v: k for k, v in items_name.items()}

items_emoji = {
    1:"<:card2:799771986523062322>",
    2:"<:hp_potion:786236538584694815>",
    3:"<:mp_potion:786236615575339029>",
    4:"<:soul_fire:786513145010454538>",
    5:"<:toishi2:799771986125520937>",
    6:"<:masyou2:799771986426593320>",
    7:"<:masuisyou:786516036673470504>",
    8:"<:magic_coin2:799771986476924998>",
    9:"<:hp_full_potion:788668620074385429>",
    10:"<:mp_full_potion:788668620314116106>",
    11:"<:caramel_ore:798207261595271200>",
    12:"<:caramel_ingot:798207112643608616>",
    13:"<:blood_ore:798207261964501002>",
    14:"<:blood_ingot:798207112630894592>",
    15:"<:gold_ore:798207261901586483>",
    16:"<:gold_ingot:798207112584232970>",
    17:"<:dark_ore:798207262068834364>",
    18:"<:dark_ingot:798207112601010236>",
    19:"<:mithril_ore:798207261922164776>",
    20:"<:mithril_ingot:798207112219328553>",
    21:"<:orihalcon_ore:798207262438064209>",
    22:"<:orihalcon_ingot:798207112441364511>",
    23:"<:iron_ingot:800198788043767849>",
    24:"<:black_iron_ingot:800198989676806164>",
    25:"<:hammer:800197618336530462>",
    26:"<:ingot_frame:802076807234060308>",
    27:"<:chip_frame:802078804163166229>",
    28:"<:carbon_powder:800197618286198813>",
    29:"<:carbon_plate:800197618327486584>",
    30:"<:carbon_chip:802069938973704194>",
}
# 画像があるアイテムの {名前:画像URL} #
items_image = {
    "HP回復薬":"https://media.discordapp.net/attachments/719855399733428244/786984382673977374/hp_potion.gif",
    "MP回復薬":"https://media.discordapp.net/attachments/719855399733428244/786984396887556096/mp_potion.gif",
    "魔石":"https://media.discordapp.net/attachments/719855399733428244/757449362652790885/maseki.png",
    "魔硬貨":"https://media.discordapp.net/attachments/719855399733428244/786984393594896474/magic_coin.gif"
}


shop_weapons = {
    'サバイバルナイフ':('<:w4:798469938380800011>',10000,2),
    '１０式シャベル':('<:w1:798469938595495967>',10000,2),
    'パイプ':('<:w2:798469938536644628>',10000,2),
    'ブロンズソード':('<:w3:798469938511216650>',10000,2),
    'バスターアックス':('<:w5:798469938175934505>',15000,2),
    '刀':('<:w17:798469941753806869>',15000,2),
    'グラム':('<:w6:798469938137792515>',15000,2),
    'セラミックソード':('<:w7:798469938180128779>',15000,2),
    '二刀一対':('<:w9:798469938401509396>',15000,2),
    'ストームブリンガー':('<:w16:798469938682658846>',15000,2),
    'ワイドブレード':('<:w35:798469938666405888>',15000,2),
    'セラミックスピア':('<:w18:798469938317885441>',15000,2),
    'ワンハンドアックス':('<:w26:798469938477400105>',15000,2),
    '十手':('<:w10:798469938389188658>',15000,2),
    'カラドボルグ':('<:w11:798469938418286602>',20000,2),
    'シーパンサー':('<:w12:798469938514886708>',20000,2),
    'フラガラック':('<:w13:798469938532712468>',20000,2),
    'ジャイアントカッター':('<:w14:798469938574393345>',20000,2),
    'スカイブレード':('<:w24:798469938464423953>',25000,2),
    'スカイアックス':('<:w28:798469938498371584>',25000,2),
    'バーンナックル':('<:w21:798469938310021132>',30000,3),
    'レーヴァンティン':('<:w23:798469938426675210>',30000,3),
    'ティルヴィング':('<:w25:798469938469011486>',30000,3),
    'デュランダル':('<:w20:798469938302025729>',30000,3),
    'ツーハンドデッドアックス':('<:w27:798469938481594388>',35000,3),
    'ネックカッター':('<:w29:798469938498502656>',35000,3),
    'ソウルイーター':('<:w30:798469938535858176>',35000,3),
    '黒桜':('<:w22:798469938418286692>',35000,3),
    '小狐丸':('<:w8:798469938208702465>',35000,3),
    'エンダーソード':('<:w31:798469938535989298>',40000,3),
    'スターライトグラム':('<:w19:798469938234523689>',45000,3),
    'カゲミツG4':('<:w32:798469938552897556>',45000,3),
    'ミスリルパイプ':('<:w36:798469938054299719>',45000,3),
    'リーフカッター':('<:w33:798469938565349396>',50000,4),
    'ロンギヌスの槍':('<:w34:798469938603884564>',50000,4),
    'ロストソング':('<:w37:798471199729778748>',50000,4),
    '永久のコイン':('<:w39:799848024640716822>',50000,4)
}
NpcWeapon = namedtuple("Weapon", [
    "name",
    "emoji",
    "id",
    "create_cost",
    "max_rank",
    "rate_of_rankup"
])
npc_weapons = {}
num = 0
for name,info in zip(tuple(shop_weapons.keys()),tuple(shop_weapons.values())):
    num += 1
    npc_weapons[num] = NpcWeapon(name,info[0],num,info[1],info[2],0.75)
player_weapons = [
    ('サバイバルナイフ', '<:w4:798469938380800011>', 1), 
    ('１０式シャベル', '<:w1:798469938595495967>', 1),
    ('パイプ', '<:w2:798469938536644628>', 1),
    ('ブロンズソード', '<:w3:798469938511216650>', 1), 
    ('バスターアックス', '<:w5:798469938175934505>', 2), 
    ('刀', '<:w17:798469941753806869>', 2), 
    ('グラム', '<:w6:798469938137792515>', 2), 
    ('セラミックソード', '<:w7:798469938180128779>', 2), 
    ('二刀一対', '<:w9:798469938401509396>', 2),
    ('ストームブリンガー', '<:w16:798469938682658846>', 2), 
    ('ワイドブレード', '<:w35:798469938666405888>', 2),
    ('セラミックスピア', '<:w18:798469938317885441>', 2), 
    ('ワンハンドアックス', '<:w26:798469938477400105>', 2),
    ('十手', '<:w10:798469938389188658>', 2),
    ('カラドボルグ', '<:w11:798469938418286602>', 3), 
    ('シーパンサー', '<:w12:798469938514886708>', 3),
    ('フラガラック', '<:w13:798469938532712468>', 3),
    ('ジャイアントカッター', '<:w14:798469938574393345>', 3), 
    ('スカイブレード', '<:w24:798469938464423953>', 3),
    ('スカイアックス', '<:w28:798469938498371584>', 3), 
    ('バーンナックル', '<:w21:798469938310021132>', 4), 
    ('レーヴァンティン', '<:w23:798469938426675210>', 4),
    ('ティルヴィング', '<:w25:798469938469011486>', 4), 
    ('デュランダル', '<:w20:798469938302025729>', 4), 
    ('ツーハンドデッドアックス', '<:w27:798469938481594388>', 5),
    ('ネックカッター', '<:w29:798469938498502656>', 5),
    ('ソウルイーター', '<:w30:798469938535858176>', 5), 
    ('黒桜', '<:w22:798469938418286692>', 5), 
    ('小狐丸', '<:w8:798469938208702465>', 5),
    ('エンダーソード', '<:w31:798469938535989298>', 6), 
    ('スターライトグラム', '<:w19:798469938234523689>', 6), 
    ('カゲミツG4', '<:w32:798469938552897556>', 6),
    ('ミスリルパイプ', '<:w36:798469938054299719>', 6),
    ('リーフカッター', '<:w33:798469938565349396>', 6), 
    ('ロンギヌスの槍', '<:w34:798469938603884564>', 6), 
    ('ロストソング', '<:w37:798471199729778748>', 7),
    ('永久のコイン', '<:w39:799848024640716822>', 7)
]
#c d b g m o
weapons_price = (50000,75000,100000,125000,150000,175000,200000)
material_emoji = (
    items_emoji[4],
    items_emoji[12],items_emoji[14],
    items_emoji[16],items_emoji[18],
    items_emoji[20],items_emoji[22],
    items_emoji[23],
)
weapons_recipe = (
    (1000,25, 25, 5, 5, 0, 0, 100,),
    (1000, 50, 50, 10, 10, 0, 0, 200,),
    (1000, 75, 75, 20, 20, 0, 0, 400,),
    (1000, 100, 100, 30, 30, 5, 5, 600,),
    (1000, 125, 125, 45, 45, 5, 5, 800,),
    (1000, 150, 150, 50, 50, 10, 10, 1000,),
    (1000, 175, 175, 60, 60, 10, 10, 1200,),
)
rank_rate = (0.5,0.55,0.6,0.65,0.7,0.75,0.8)
