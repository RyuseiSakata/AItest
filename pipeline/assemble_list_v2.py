# -*- coding: utf-8 -*-
# リスト系サンプルv2: 高情報密度版(9項目・3層非冗長・進捗バー・カウンター)
import av
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS, SR = 480, 832, 16, 22050

# (wav, メインテロップ(圧縮キーワード=音声と非冗長), ぷにまる小ネタ, バッジ)
SECTIONS = [
    ("v2_0.wav",  ["人生を溶かす", "習慣 9選"], "3つは当てはまるにゃ", ""),
    ("v2_1.wav",  ["① 無限スクロール"], "朝後悔するやつにゃ", "1/9"),
    ("v2_2.wav",  ["② “あとで”の在庫化"], "在庫は腐るにゃ", "2/9"),
    ("v2_3.wav",  ["③ 通知の即開封"], "犬すぎるにゃ", "3/9"),
    ("v2_4.wav",  ["④ 迷ったら課金"], "財布が痩せるにゃ", "4/9"),
    ("v2_5.wav",  ["⑤ 口癖 “疲れた”"], "言うほど疲れるにゃ", "5/9"),
    ("v2_6.wav",  ["⑥ 寝溜めで休日消滅"], "猫でも予定あるにゃ", "6/9"),
    ("v2_7.wav",  ["⑦ 他人の成功の見すぎ"], "よそのchにゃ", "7/9"),
    ("v2_8.wav",  ["⑧ “明日から本気”更新"], "聞き飽きたにゃ", "8/9"),
    ("v2_9.wav",  ["⑨ 完璧な計画で満足"], "やるのは今日にゃ", "9/9"),
    ("v2_10.wav", ["3つ以上 → 保存"], "数はコメントで晒すにゃ", ""),
]

font_big = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 54)
font_cat = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 27)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 30)

cat_src = Image.open(OUT + r"\punimaru_smoke_00001_.webp").convert("RGB")
cw, chh = cat_src.size
cat = cat_src.crop((int(cw*0.18), int(chh*0.38), int(cw*0.82), int(chh*0.95))).resize((210, 187))
mask = Image.new("L", cat.size, 0)
ImageDraw.Draw(mask).ellipse([4, 4, cat.size[0]-4, cat.size[1]-4], fill=255)

PALETTES = [((255,150,20),(255,190,40)), ((30,90,220),(60,130,255)), ((200,30,90),(240,70,130)), ((20,150,90),(40,190,120))]

def radial_bg(t, pal):
    img = Image.new("RGB", (W, H), pal[0])
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    n = 18
    rot = t * 0.5
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

def make_frame(idx, lines, gag, badge, t, sec_len, progress):
    pal = PALETTES[idx % len(PALETTES)]
    img = radial_bg(t, pal)
    d = ImageDraw.Draw(img)
    # メインテロップ(ポップイン: 0.12秒で拡大着地)
    scale = min(1.0, 0.55 + t / 0.12 * 0.45) if t < 0.12 else 1.0
    base_y = 250
    for i, line in enumerate(lines):
        f = font_big if scale >= 1.0 else ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", int(54 * scale))
        col = "white" if i % 2 == 0 else (255, 245, 80)
        outlined(d, (W//2, base_y + i * 80), line, f, col)
    # バッジ(右上カウンター)
    if badge:
        d.rounded_rectangle([W-120, 24, W-16, 72], radius=14, fill="black")
        d.text((W-68, 48), badge, font=font_badge, fill="white", anchor="mm")
    # ぷにまる+小ネタ(0.5秒で即出し=テンポ優先)
    img.paste(cat, (W//2 - 105, H - 240), mask)
    if gag and t > min(0.5, sec_len * 0.3):
        bx, by = W//2, H - 272
        d.rounded_rectangle([bx-200, by-25, bx+200, by+25], radius=20, fill="white", outline="black", width=3)
        d.text((bx, by), gag, font=font_cat, fill="black", anchor="mm")
    # 進捗バー(最下部)
    d.rectangle([0, H-10, int(W * progress), H], fill="white")
    return img

out = av.open(OUT + r"\list_sample_v2.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "20"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"
audio_all = np.zeros(0, dtype=np.int16)

durs = []
for wav, _, _, _ in SECTIONS:
    durs.append(len(read_wav(STG + "\\" + wav)) / SR + 0.15)
total_dur = sum(durs)

elapsed = 0.0
for idx, (wav, lines, gag, badge) in enumerate(SECTIONS):
    narr = read_wav(STG + "\\" + wav)
    sec_len = durs[idx]
    total = int(sec_len * FPS)
    seg = np.zeros(total * SR // FPS, dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    for i in range(total):
        prog = (elapsed + i / FPS) / total_dur
        img = make_frame(idx, lines, gag, badge, i / FPS, sec_len, prog)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
    elapsed += sec_len
    print("sec ok:", idx, total, "frames")

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
print("V2 OK  total_sec =", len(audio_all) / SR)
