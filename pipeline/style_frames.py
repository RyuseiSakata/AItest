# -*- coding: utf-8 -*-
# スタイル案3枚(静止画)— 選定後に動画化する
import av
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H = 720, 1248

def gothic(size): return ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", size)
def mincho(size): return ImageFont.truetype(r"C:\Windows\Fonts\yumindb.ttf", size)
def bizgo(size):  return ImageFont.truetype(r"C:\Windows\Fonts\BIZ-UDGothicB.ttc", size)

# アニメクリップから1フレーム
c = av.open(OUT + r"\anim_03_00001_.mp4")
anim = list(c.decode(video=0))[20].to_image()
c.close()

def rounded(img, size, radius):
    img = img.resize((size, size))
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return img, m

def soft_shadow_rect(base, box, radius, blur, alpha, offset=(0, 10)):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0]+offset[0], box[1]+offset[1], box[2]+offset[0], box[3]+offset[1]], radius=radius, fill=(0, 0, 0, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))

# ============ 案A: 和モダン編集(生成り×墨×朱・明朝) ============
def style_a():
    img = Image.new("RGBA", (W, H), (247, 244, 238, 255))
    rng = np.random.default_rng(3)
    noise = Image.fromarray(rng.integers(0, 14, (H//2, W//2), dtype=np.uint8), "L").resize((W, H))
    img.paste((225, 220, 210), (0, 0), noise)
    d = ImageDraw.Draw(img)
    SUMI = (34, 33, 31)
    SHU = (196, 64, 52)
    # 上部: 小さなラベル+大見出し(明朝)
    d.text((60, 70), "人生を溶かす習慣", font=gothic(26), fill=SHU)
    d.line([60, 112, 200, 112], fill=SHU, width=2)
    d.text((48, 150), "通知の", font=mincho(88), fill=SUMI)
    d.text((48, 258), "即開封", font=mincho(88), fill=SUMI)
    # 大きな番号(明朝・薄墨)
    d.text((W-70, 200), "03", font=mincho(170), fill=(34, 33, 31, 38), anchor="mm")
    d.text((W-70, 306), "— 09", font=gothic(24), fill=(120, 116, 108), anchor="mm")
    # アニメ窓(白フチの写真カード風)
    a, m = rounded(anim, 500, 18)
    soft_shadow_rect(img, (104, 434, 616, 946), 22, 26, 70)
    d.rounded_rectangle([96, 426, 624, 954], radius=22, fill=(255, 255, 255, 255))
    img.paste(a, (110, 440), m)
    # コメント(付箋風・墨文字)
    d.rounded_rectangle([56, 986, 400, 1052], radius=6, fill=(255, 252, 240), outline=(210, 200, 180), width=2)
    d.text((76, 1019), "既読つけたら負け", font=bizgo(28), fill=SUMI, anchor="lm")
    d.rounded_rectangle([330, 1072, 664, 1138], radius=6, fill=(255, 252, 240), outline=(210, 200, 180), width=2)
    d.text((350, 1105), "休憩が終わらん", font=bizgo(28), fill=SUMI, anchor="lm")
    # ぷにまるのセリフ(下部・朱の鉤括弧)
    d.text((W//2, 1188), "ぷにまる「犬すぎるにゃ」", font=gothic(30), fill=SUMI, anchor="mm")
    # 進捗(朱の細線)
    d.rectangle([0, H-5, int(W*0.33), H], fill=SHU)
    return img.convert("RGB")

# ============ 案B: 上質バラエティ(白×2色帯・視認性全振り) ============
def style_b():
    img = Image.new("RGBA", (W, H), (252, 252, 250, 255))
    d = ImageDraw.Draw(img)
    NAVY = (28, 52, 94)
    YELL = (255, 205, 40)
    # 上部の帯テロップ(番組風)
    d.rectangle([0, 60, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 140], fill=YELL)
    d.text((W//2, 94), "人生を溶かす習慣 9選", font=bizgo(40), fill="white", anchor="mm")
    # 番号ロゼット+見出し
    d.ellipse([48, 190, 148, 290], fill=YELL)
    d.text((98, 240), "3", font=bizgo(56), fill=NAVY, anchor="mm")
    sh = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(sh).text((178+2, 240+4), "通知の即開封", font=bizgo(58), fill=(0,0,0,60), anchor="lm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d.text((178, 240), "通知の即開封", font=bizgo(58), fill=NAVY, anchor="lm")
    # アニメ窓(角丸・紺の細フチ)
    a, m = rounded(anim, 500, 26)
    soft_shadow_rect(img, (110, 360, 610, 860), 26, 22, 60)
    img.paste(a, (110, 356), m)
    d.rounded_rectangle([110, 356, 610, 856], radius=26, outline=NAVY, width=4)
    # コメント(白カード+紺フチ)
    for (x, y, t) in [(70, 900, "既読つけたら負け"), (330, 986, "休憩が終わらん")]:
        tw = d.textlength(t, font=bizgo(30))
        soft_shadow_rect(img, (x, y, x+tw+48, y+64), 32, 12, 45, offset=(0,6))
        d.rounded_rectangle([x, y, x+tw+48, y+64], radius=32, fill="white", outline=NAVY, width=3)
        d.text((x+24, y+32), t, font=bizgo(30), fill=(40, 42, 48), anchor="lm")
    # 下部: セリフ帯
    d.rectangle([0, 1120, W, 1190], fill=(245, 244, 240))
    d.text((W//2, 1155), "ぷにまる「犬すぎるにゃ」", font=bizgo(32), fill=NAVY, anchor="mm")
    d.rectangle([0, H-8, int(W*0.33), H], fill=YELL)
    return img.convert("RGB")

# ============ 案C: 洗練ポップ(v5の明るさ+品) ============
def style_c():
    # 淡いクリーム→ペールブルーのグラデ
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    g = Image.new("RGB", (1, H))
    for y in range(H):
        k = y / H
        g.putpixel((0, y), (int(255 - 12*k), int(250 - 6*k), int(242 + 10*k)))
    img.paste(g.resize((W, H)), (0, 0))
    d = ImageDraw.Draw(img)
    CORAL = (255, 122, 89)
    DEEP = (52, 56, 66)
    # ふわっとした水玉(ごく淡い)
    for (x, y, r, col) in [(90, 180, 60, (255, 214, 200)), (640, 120, 44, (205, 226, 255)), (620, 1050, 70, (255, 236, 190))]:
        d.ellipse([x-r, y-r, x+r, y+r], fill=col)
    # 見出し(ゴシック太+コーラルのマーカー下線)
    d.rectangle([120, 236, 600, 270], fill=(255, 214, 200))
    sh = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(sh).text((W//2+2, 210+4), "③ 通知の即開封", font=gothic(58), fill=(0,0,0,50), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d.text((W//2, 210), "③ 通知の即開封", font=gothic(58), fill=DEEP, anchor="mm")
    d.text((W-64, 80), "3/9", font=gothic(34), fill="white", anchor="mm")
    d.rounded_rectangle([W-124, 52, W-24, 108], radius=28, outline=CORAL, width=3)
    d.text((W-74, 80), "3/9", font=gothic(32), fill=CORAL, anchor="mm")
    # アニメ窓(白い太フチ=ポラロイド風、傾き2度)
    a, m = rounded(anim, 480, 20)
    card = Image.new("RGBA", (540, 540), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, 540, 540], radius=26, fill="white")
    card.paste(a, (30, 30), m)
    card = card.rotate(2, resample=Image.BICUBIC, expand=True)
    soft_shadow_rect(img, (100, 350, 630, 880), 30, 28, 55)
    img.alpha_composite(card, (86, 330))
    # コメント(角丸ピル・コーラル/ブルーの2色)
    for (x, y, t, col) in [(70, 930, "既読つけたら負け", CORAL), (320, 1016, "休憩が終わらん", (77, 130, 235))]:
        tw = d.textlength(t, font=gothic(30))
        soft_shadow_rect(img, (x, y, x+tw+52, y+64), 32, 12, 40, offset=(0,6))
        d.rounded_rectangle([x, y, x+tw+52, y+64], radius=32, fill="white")
        d.ellipse([x+14, y+22, x+34, y+42], fill=col)
        d.text((x+46, y+32), t, font=gothic(30), fill=DEEP, anchor="lm")
    d.text((W//2, 1170), "ぷにまる「犬すぎるにゃ」", font=gothic(32), fill=DEEP, anchor="mm")
    d.rounded_rectangle([24, H-14, int(W*0.33), H-6], radius=4, fill=CORAL)
    return img.convert("RGB")

style_a().save(STG + r"\style_A_wamodern.png")
style_b().save(STG + r"\style_B_variety.png")
style_c().save(STG + r"\style_C_pop.png")
print("3 styles saved")
