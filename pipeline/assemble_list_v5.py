# -*- coding: utf-8 -*-
# v5: 中央にぷにまる演技アニメ窓を実装(v4のコメント2連発・動き密度は維持)
import av
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS, SR = 480, 832, 16, 22050

SECTIONS = [
    ("v2_0.wav",  ["人生を溶かす", "習慣 9選"], "3つは当てはまるにゃ", "", "⏳", ["診断スタートw", "怖いもの見たさ"], "anim_00"),
    ("v2_1.wav",  ["① 無限スクロール"], "朝後悔するやつにゃ", "1/9", "📱", ["気づいたら3時", "わかりすぎる"], "anim_01"),
    ("v2_2.wav",  ["② “あとで”の在庫化"], "在庫は腐るにゃ", "2/9", "📦", ["タブ100個ある", "積読も同じ"], "anim_02"),
    ("v2_3.wav",  ["③ 通知の即開封"], "犬すぎるにゃ", "3/9", "🔔", ["既読つけたら負け", "休憩が終わらん"], "anim_03"),
    ("v2_4.wav",  ["④ 迷ったら課金"], "財布が痩せるにゃ", "4/9", "💸", ["ガチャのことか", "限定に弱い"], "anim_04"),
    ("v2_5.wav",  ["⑤ 口癖 “疲れた”"], "言うほど疲れるにゃ", "5/9", "😩", ["言うと余計疲れる", "口癖になってた"], "anim_05"),
    ("v2_6.wav",  ["⑥ 寝溜めで休日消滅"], "猫でも予定あるにゃ", "6/9", "🛌", ["起きたら夕方", "休日どこ行った"], "anim_06"),
    ("v2_7.wav",  ["⑦ 他人の成功の見すぎ"], "よそのchにゃ", "7/9", "👀", ["比較して病むやつ", "見るだけで満足"], "anim_07"),
    ("v2_8.wav",  ["⑧ “明日から本気”更新"], "聞き飽きたにゃ", "8/9", "🔥", ["万年明日組w", "通知は消した"], "anim_08"),
    ("v2_9.wav",  ["⑨ 完璧な計画で満足"], "やるのは今日にゃ", "9/9", "📝", ["計画だけA評価", "ノートだけ綺麗"], "anim_09"),
    ("v2_10.wav", ["3つ以上 → 保存"], "数はコメントで晒すにゃ", "", "💾", ["4つだった…", "保存した"], "anim_10"),
]

def jf(size):
    return ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", size)

font_cat = jf(26)
font_badge = jf(30)
font_emoji = ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf", 64)

PALETTES = [((255,150,20),(255,190,40)), ((30,90,220),(60,130,255)), ((200,30,90),(240,70,130)), ((20,150,90),(40,190,120))]

ANIM_SIZE = 330
anim_mask = Image.new("L", (ANIM_SIZE, ANIM_SIZE), 0)
ImageDraw.Draw(anim_mask).rounded_rectangle([0, 0, ANIM_SIZE, ANIM_SIZE], radius=36, fill=255)

def load_clip(prefix):
    c = av.open(OUT + "\\" + prefix + "_00001_.mp4")
    frames = [f.to_image().resize((ANIM_SIZE, ANIM_SIZE)) for f in c.decode(video=0)]
    c.close()
    return frames

def radial_bg(t, pal):
    img = Image.new("RGB", (W, H), pal[0])
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2 - 60
    n = 18
    rot = t * 1.2
    for i in range(n):
        a0 = rot + i * 2 * math.pi / n
        a1 = a0 + math.pi / n
        R = 1200
        d.polygon([(cx, cy), (cx + R*math.cos(a0), cy + R*math.sin(a0)), (cx + R*math.cos(a1), cy + R*math.sin(a1))], fill=pal[1] if i % 2 else pal[0])
    return img

def outlined(d, xy, text, font, fill, outline="black", ow=4, anchor="mm"):
    x, y = xy
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx or dy:
                d.text((x+dx, y+dy), text, font=font, fill=outline, anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def read_wav(path):
    with wave.open(path, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            data = data[::2]
    return data

CHAR_SPEED = 0.045

def draw_comment(img, text, cx, cy, tilt, age):
    pop = min(1.0, age / 0.12)
    size = int(29 * (0.6 + 0.4 * pop))
    f = jf(size)
    tmp = Image.new("RGBA", (400, 90), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = td.textlength(text, font=f)
    td.rounded_rectangle([200 - tw/2 - 15, 14, 200 + tw/2 + 15, 76], radius=16, fill=(255, 255, 255, 240), outline=(0, 0, 0, 255), width=3)
    td.text((200, 45), text, font=f, fill="black", anchor="mm")
    tmp = tmp.rotate(tilt, resample=Image.BICUBIC, expand=False)
    drift = int(4 * math.sin(age * 5))
    img.paste(tmp, (int(cx - 200), int(cy - 45 + drift)), tmp)

def make_frame(idx, lines, gag, badge, emoji, t, sec_len, progress, comments, clip):
    pal = PALETTES[idx % len(PALETTES)]
    img = radial_bg(t, pal)
    d = ImageDraw.Draw(img)

    # 絵文字(左上・揺れ)
    e = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    ImageDraw.Draw(e).text((50, 50), emoji, font=font_emoji, anchor="mm", embedded_color=True)
    e = e.rotate(6 * math.sin(t * 5), resample=Image.BICUBIC)
    img.paste(e, (16, 20 + int(4 * math.sin(t * 4))), e)

    # メインテロップ(文字送り+着地バウンド)
    base_y = 200
    shown_budget = int(t / CHAR_SPEED) + 1
    for li, line in enumerate(lines):
        prior = sum(len(l) for l in lines[:li])
        vis = max(0, min(len(line), shown_budget - prior))
        if vis <= 0:
            continue
        text = line[:vis]
        last_char_age = t - (prior + vis - 1) * CHAR_SPEED
        bounce = -10 * math.exp(-last_char_age * 14) if last_char_age >= 0 else 0
        col = "white" if li % 2 == 0 else (255, 245, 80)
        size = 50 if max(len(l) for l in lines) <= 11 else 42
        outlined(d, (W//2, base_y + li * 74 + bounce), text, jf(size), col)

    # 中央アニメ窓(ぷにまる演技クリップ・ループ再生・入場ポップ)
    frame_idx = int(t * FPS) % len(clip)
    pop = min(1.0, t / 0.15)
    size_now = int(ANIM_SIZE * (0.75 + 0.25 * pop))
    cf = clip[frame_idx].resize((size_now, size_now))
    m = anim_mask.resize((size_now, size_now))
    ax = W//2 - size_now//2
    ay = 300 + (ANIM_SIZE - size_now)//2 + int(4 * math.sin(t * 3))
    img.paste(cf, (ax, ay), m)
    d.rounded_rectangle([ax, ay, ax + size_now, ay + size_now], radius=int(36 * size_now/ANIM_SIZE), outline="white", width=5)

    # バッジ(右上・脈動)
    if badge:
        pulse = 1 + 0.06 * math.sin(t * 6)
        bw = int(52 * pulse)
        d.rounded_rectangle([W-118, 48-bw//2, W-14, 48+bw//2], radius=14, fill="black")
        d.text((W-66, 48), badge, font=font_badge, fill="white", anchor="mm")

    # コメント2連発(アニメ窓の縁に重ねる)
    c1_at = sec_len * 0.22
    c2_at = sec_len * 0.52
    if len(comments) > 0 and t >= c1_at:
        draw_comment(img, comments[0], W * 0.30, 330, 5, t - c1_at)
    if len(comments) > 1 and t >= c2_at:
        draw_comment(img, comments[1], W * 0.70, 612, -5, t - c2_at)

    # ぷにまるのセリフ(アニメ窓の下)
    if gag and t > min(0.5, sec_len * 0.3):
        age = t - min(0.5, sec_len * 0.3)
        pop2 = min(1.0, age / 0.1)
        bx, by = W//2, 700
        hw = int(205 * pop2)
        d.rounded_rectangle([bx-hw, by-27, bx+hw, by+27], radius=20, fill="white", outline="black", width=3)
        if pop2 >= 1.0:
            d.text((bx, by), "ぷにまる「" + gag + "」", font=font_cat, fill="black", anchor="mm")

    # 進捗バー
    d.rectangle([0, H-12, int(W * progress), H], fill="white")
    d.rectangle([0, H-12, W, H], outline="black", width=2)

    # セクション頭: フラッシュ+シェイク
    if t < 0.12:
        k = (0.12 - t) / 0.12
        flash = Image.new("RGB", (W, H), "white")
        img = Image.blend(img, flash, k * 0.75)
        dx = int(6 * math.sin(idx * 3.1 + t * 90))
        dy = int(5 * math.cos(idx * 1.7 + t * 70))
        img = img.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy))

    # 常時ズーム脈動
    z = 1 + 0.02 * (0.5 + 0.5 * math.sin(t * 4))
    zw, zh = int(W * z), int(H * z)
    img = img.resize((zw, zh)).crop(((zw-W)//2, (zh-H)//2, (zw-W)//2 + W, (zh-H)//2 + H))
    return img

out = av.open(OUT + r"\list_sample_v5.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "20"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"
audio_all = np.zeros(0, dtype=np.int16)

durs = [len(read_wav(STG + "\\" + s[0])) / SR + 0.15 for s in SECTIONS]
total_dur = sum(durs)

elapsed = 0.0
for idx, (wav, lines, gag, badge, emoji, comments, animp) in enumerate(SECTIONS):
    clip = load_clip(animp)
    narr = read_wav(STG + "\\" + wav)
    sec_len = durs[idx]
    total = int(sec_len * FPS)
    seg = np.zeros(total * SR // FPS, dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    for i in range(total):
        prog = (elapsed + i / FPS) / total_dur
        img = make_frame(idx, lines, gag, badge, emoji, i / FPS, sec_len, prog, comments, clip)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
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
print("V5 OK  total_sec =", len(audio_all) / SR)
