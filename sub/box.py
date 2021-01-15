# ※全要素をkey->idで管理するように!!
players = {}
mobs = {}
cmd_user = []
cbt_user = {}
cbt_ch = {}
cmd_ch = []

# デバフ　バフ系
stun = {}
nerf = {}
power_charge = {}
magic_charge = {}
atk_switch = {}
anti_magic = []
exp_up_buff = []
fleez = []

# items_~ #
items_name = {
    1:"冒険者カード",
    2:"HP回復薬",3:"MP回復薬",
    4:"魂の焔",
    5:"砥石",6:"魔石",7:"魔晶",8:"魔硬貨",
    9:"HP全回復薬",10:"MP全回復薬",
}

items_id = {
    "冒険者カード":1,
    "HP回復薬":2,"MP回復薬":3,
    "魂の焔":4,
    "砥石":5,"魔石":6,"魔晶":7,"魔硬貨":8,
    "HP全回復薬":9,"MP全回復薬":10,
}

items_emoji = {
    1:"<:card:786514637289947176>",
    2:"<:hp_potion:786236538584694815>",
    3:"<:mp_potion:786236615575339029>",
    4:"<:soul_fire:786513145010454538>",
    5:"<:toishi:786513144691556364>",
    6:"<:maseki:785641515561123921>",
    7:"<:masuisyou:786516036673470504>",
    8:"<:magic_coin:786513121236746260>",
    9:"<:hp_full_potion:788668620074385429>",
    10:"<:mp_full_potion:788668620314116106>",
}

items_emoji_a = {
    1:"<:card:786514637289947176>",
    2:"<a:hp_potion_a:786982694479200336>",
    3:"<a:mp_potion_a:786982694839124021>",
    4:"<:soul_fire:786513145010454538>",
    5:"<a:toishi_a:786974865777229864>",
    6:"<:maseki:785641515561123921>",
    7:"<a:masuisyou_a:786982694948306974>",
    8:"<a:magic_coin_a:786966211594289153>",
    9:"<:hp_full_potion:788668620074385429>",
    10:"<:mp_full_potion:788668620314116106>",
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
}
