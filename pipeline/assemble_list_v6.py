# -*- coding: utf-8 -*-
# v6: 高級感モーション版
# 原則: イージング(ease-out)/要素は入場後に静止/深い配色+金アクセント/柔らかい影/
#       ビネット+フィルムグレイン/クロスディップ切替/24fps/720p
import av
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS, SR = 720, 1248, 24, 22050
GOLD = (217, 185, 106)
INK = (240, 238, 232)

SECTIONS = [
    ("v2_0.wav",  ["人生を溶かす", "習慣 9選"], "3つは当てはまるにゃ", "", ["診断スタートw", "怖いもの見たさ"], "anim_00"),
    ("v2_1.wav",  ["① 無限スクロール"], "朝後悔するやつにゃ", "1/9", ["気づいたら3時", "わかりすぎる"], "anim_01"),
    ("v2_2.wav",  ["② “あとで”の在庫化"], "在庫は腐るにゃ", "2/9", ["タブ100個ある", "積読も同じ"], "anim_02"),
    ("v2_3.wav",  ["③ 通知の即開封"], "犬すぎるにゃ", "3/9", ["既読つけたら負け", "休憩が終わらん"], "anim_03"),
    ("v2_4.wav",  ["④ 迷ったら課金"], "財布が痩せるにゃ", "4/9", ["ガチャのことか", "限定に弱い"], "anim_04"),
    ("v2_5.wav",  ["⑤ 口癖 “疲れた”"], "言うほど疲れるにゃ", "5/9", ["言うと余計疲れる", "口癖になってた"], "anim_05"),
    ("v2_6.wav",  ["⑥ 寝溜めで休日消滅"], "猫でも予定あるにゃ", "6/9", ["起きたら夕方", "休日どこ行った"], "anim_06"),
    ("v2_7.wav",  ["⑦ 他人の成功の見すぎ"], "よそのchにゃ", "7/9", ["比較して病むやつ", "見るだけで満足"], "anim_07"),
    ("v2_8.wav",  ["⑧ “明日から本気”更新"], "聞き飽きたにゃ", "8/9", ["万年明日組w", "通知は消した"], "anim_08"),
    ("v2_9.wav",  ["⑨ 完璧な計画で満足"], "やるのは今日にゃ", "9/9", ["計画だけA評価", "ノートだけ綺麗"], "anim_09"),
    ("v2_10.wav", ["3つ以上 → 保存"], "数はコメントで晒すにゃ", "", ["4つだった…", "保存した"], "anim_10"),
]

def jf(size):
    return ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", size)

# ---- イージング ----
def ease_out_expo(x):
    return 1 if x >= 1 else 1 - 2 ** (-10 * x)

def ease_out_back(x, s=1.4):
    x = min(1.0, x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2

# ---- 背景素材(事前計算) ----
def make_base_bg():
    g = Image.new("RGB", (1, H))
    for y in range(H):
        k = y / H
        r = int(18 + 10 * k); gr = int(21 + 8 * k); b = int(34 + 14 * k)
        g.putpixel((0, y), (r, gr, b))
    return g.resize((W, H))

BASE_BG = make_base_bg()

GLOW = Image.new("L", (600, 600), 0)
gd = ImageDraw.Draw(GLOW)
for r in range(300, 0, -6):
    gd.ellipse([300-r, 300-r, 300+r, 300+r], fill=int(60 * (1 - r/300) ** 1.6))

VIGNETTE = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(VIGNETTE)
for i in range(120):
    a = int(90 * (i / 120) ** 2)
    vd.rectangle([i*3, i*3, W - i*3, H - i*3], outline=a)
VIGNETTE = VIGNETTE.filter(ImageFilter.GaussianBlur(60))

rng = np.random.default_rng(7)
GRAINS = []
for _ in range(4):
    n = rng.integers(0, 28, (H // 2, W // 2), dtype=np.uint8)
    GRAINS.append(Image.fromarray(n, "L").resize((W, H)))

ANIM_SIZE = 480
anim_mask = Image.new("L", (ANIM_SIZE, ANIM_SIZE), 0)
ImageDraw.Draw(anim_mask).rounded_rectangle([0, 0, ANIM_SIZE, ANIM_SIZE], radius=44, fill=255)
SHADOW = Image.new("RGBA", (ANIM_SIZE + 120, ANIM_SIZE + 120), (0, 0, 0, 0))
ImageDraw.Draw(SHADOW).rounded_rectangle([60, 74, ANIM_SIZE + 60, ANIM_SIZE + 74], radius=44, fill=(0, 0, 0, 130))
SHADOW = SHADOW.filter(ImageFilter.GaussianBlur(24))

CARD_SH = Image.new("RGBA", (560, 150), (0, 0, 0, 0))
ImageDraw.Draw(CARD_SH).rounded_rectangle([30, 40, 530, 120], radius=22, fill=(0, 0, 0, 110))
CARD_SH = CARD_SH.filter(ImageFilter.GaussianBlur(14))

def load_clip(prefix):
    c = av.open(OUT + "\\" + prefix + "_00001_.mp4")
    frames = [f.to_image().resize((ANIM_SIZE, ANIM_SIZE)) for f in c.decode(video=0)]
    c.close()
    return frames

def read_wav(path):
    with wave.open(path, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            data = data[::2]
    return data

def soft_text(img, xy, text, font, fill, anchor="mm", shadow_alpha=140):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((xy[0] + 3, xy[1] + 5), text, font=font, fill=(0, 0, 0, shadow_alpha), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(4))
    ld2 = ImageDraw.Draw(layer)
    ld2.text(xy, text, font=font, fill=fill, anchor=anchor)
    img.alpha_composite(layer)

def draw_card(img, text, cx, cy, age, tilt=0):
    k = ease_out_back(min(1.0, age / 0.28))
    rise = int(26 * (1 - k))
    alpha = int(255 * min(1.0, age / 0.15))
    f = jf(31)
    tmp = Image.new("RGBA", (560, 150), (0, 0, 0, 0))
    tmp.alpha_composite(CARD_SH)
    td = ImageDraw.Draw(tmp)
    tw = td.textlength(text, font=f)
    td.rounded_rectangle([280 - tw/2 - 24, 36, 280 + tw/2 + 24, 108], radius=20, fill=(250, 249, 245, 255))
    td.line([280 - tw/2 - 24, 104, 280 - tw/2 - 24 + 46, 104], fill=GOLD, width=4)
    td.text((280, 70), text, font=f, fill=(30, 32, 40), anchor="mm")
    if tilt:
        tmp = tmp.rotate(tilt, resample=Image.BICUBIC, expand=False)
    tmp.putalpha(tmp.getchannel("A").point(lambda a: a * alpha // 255))
    img.alpha_composite(tmp, (int(cx - 280), int(cy - 70 + rise)))

def make_frame(idx, lines, gag, badge, t, sec_len, progress, comments, clip, frame_no):
    img = BASE_BG.copy().convert("RGBA")

    # 淡い光のブロブ2つ(ゆっくり漂う唯一の常時運動・低不透明度)
    for bi, (spd, ph, tint) in enumerate([(0.05, 0.0, (90, 110, 200)), (0.035, 2.4, (200, 170, 90))]):
        bx = int(W/2 + 260 * math.sin(t * spd * 2 * math.pi + ph + idx))
        by = int(H * 0.35 + 300 * math.cos(t * spd * 1.4 * math.pi + ph))
        blob = Image.new("RGBA", (600, 600), tint + (0,))
        blob.putalpha(GLOW.point(lambda a: a // 3))
        img.alpha_composite(blob, (bx - 300, by - 300))

    # メインテロップ: フェード+ライズ入場 → 完全静止
    base_y = 240
    for li, line in enumerate(lines):
        delay = li * 0.12
        k = ease_out_expo(max(0.0, (t - delay)) / 0.5) if t > delay else 0.0
        if k <= 0:
            continue
        size = 62 if max(len(l) for l in lines) <= 11 else 52
        y = base_y + li * 92 + int(24 * (1 - k))
        f = jf(size)
        col = INK if li % 2 == 0 else GOLD
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        soft_text(layer, (W//2, y), line, f, col + (int(255 * k),))
        img.alpha_composite(layer)
    # 金の下線がスッと引かれる
    uk = ease_out_expo(max(0.0, t - 0.35) / 0.4)
    if uk > 0:
        ln = int(150 * uk)
        d0 = ImageDraw.Draw(img)
        uy = base_y + (len(lines) - 1) * 92 + 58
        d0.line([W//2 - ln, uy, W//2 + ln, uy], fill=GOLD + (255,), width=3)

    # 中央アニメ窓: scale-in(ease-out-back)→ 静止。柔らかい影+金の細枠
    frame_idx = int(t * 16) % len(clip)
    k = ease_out_back(min(1.0, t / 0.35), s=1.1)
    size_now = max(2, int(ANIM_SIZE * (0.88 + 0.12 * k)))
    ax = W//2 - size_now//2
    ay = 470 + (ANIM_SIZE - size_now)//2
    img.alpha_composite(SHADOW.resize((size_now + 120, size_now + 120)), (ax - 60, ay - 60))
    cf = clip[frame_idx].resize((size_now, size_now))
    m = anim_mask.resize((size_now, size_now))
    img.paste(cf, (ax, ay), m)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([ax, ay, ax + size_now, ay + size_now], radius=int(44 * size_now/ANIM_SIZE), outline=GOLD + (230,), width=3)

    # バッジ(右上・静止・ダークチップに金文字)
    if badge:
        d.rounded_rectangle([W-150, 40, W-32, 96], radius=16, fill=(28, 30, 42, 235), outline=GOLD + (180,), width=2)
        d.text((W-91, 68), badge, font=jf(32), fill=GOLD, anchor="mm")

    # コメントカード2枚(スライドイン→静止)
    c1_at = sec_len * 0.24
    c2_at = sec_len * 0.54
    if len(comments) > 0 and t >= c1_at:
        draw_card(img, comments[0], W * 0.32, 452, t - c1_at, tilt=2)
    if len(comments) > 1 and t >= c2_at:
        draw_card(img, comments[1], W * 0.68, 972, t - c2_at, tilt=-2)

    # ぷにまるのセリフ(下部・金ルール付きの静かなカード)
    g_at = min(0.6, sec_len * 0.35)
    if gag and t >= g_at:
        age = t - g_at
        k = ease_out_expo(min(1.0, age / 0.4))
        alpha = int(255 * k)
        fy = 1108 + int(16 * (1 - k))
        f = jf(30)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        text = "— ぷにまる「" + gag + "」"
        ld.text((W//2, fy), text, font=f, fill=INK + (alpha,), anchor="mm")
        img.alpha_composite(layer)

    # 進捗(細い金ライン)
    d.rectangle([0, H-6, int(W * progress), H], fill=GOLD + (255,))

    # セクション切替: 短いディップ(明度を落として戻す)
    if t < 0.18:
        dip = (0.18 - t) / 0.18 * 0.55
        black = Image.new("RGBA", img.size, (8, 9, 14, int(255 * dip)))
        img = Image.alpha_composite(img, black)

    # ビネット+フィルムグレイン
    img.paste((0, 0, 0), (0, 0), VIGNETTE)
    grain = GRAINS[frame_no % 4]
    img.paste((255, 255, 255), (0, 0), grain.point(lambda a: a // 3))
    return img.convert("RGB")

out = av.open(OUT + r"\list_sample_v6.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "19"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"
audio_all = np.zeros(0, dtype=np.int16)

durs = [len(read_wav(STG + "\\" + s[0])) / SR + 0.25 for s in SECTIONS]
total_dur = sum(durs)

frame_no = 0
elapsed = 0.0
for idx, (wav, lines, gag, badge, comments, animp) in enumerate(SECTIONS):
    clip = load_clip(animp)
    narr = read_wav(STG + "\\" + wav)
    sec_len = durs[idx]
    total = int(sec_len * FPS)
    seg = np.zeros(int(total * SR / FPS), dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    for i in range(total):
        prog = (elapsed + i / FPS) / total_dur
        img = make_frame(idx, lines, gag, badge, i / FPS, sec_len, prog, comments, clip, frame_no)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
        frame_no += 1
    elapsed += sec_len
    print("sec ok:", idx)

for i in range(0, len(audio_all), 1024):
    seg = audio_all[i:i+1024]
    af = av.AudioFrame.from_ndarray(seg.reshape(1, -1), format="s16", layout="mono")
    af.sample_rate = SR
    for pkt in asr.encode(af):
        out.mux(pkt)
for pkt in vs.encode():
    out.mux(pkt)
for pkt in asr.encode():
    out.mux(pkt)
out.close()
print("V6 OK  total_sec =", len(audio_all) / SR)
