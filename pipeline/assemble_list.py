# -*- coding: utf-8 -*-
# リスト系サンプル: 放射背景+デカ文字+ぷにまる進行+読み上げ → mp4
import av
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS, SR = 480, 832, 16, 22050

SECTIONS = [
    ("list0.wav", ["人生がラクになる", "考え方 5選"], None),
    ("list1.wav", ["① 他人の期待は", "他人の荷物"], "背負わんにゃ"),
    ("list2.wav", ["② 休む =", "メンテナンス"], "猫は16時間寝るにゃ"),
    ("list3.wav", ["③ 怒りは6秒で", "消える"], "おやつ待機にゃ"),
    ("list4.wav", ["④ 全部やる =", "全部できない"], "昼寝は死守にゃ"),
    ("list5.wav", ["⑤ 比べるのは", "昨日の自分"], "他人はよそのchにゃ"),
    ("list6.wav", ["保存して", "見返すにゃ"], "また明日にゃ"),
]

font_big = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 52)
font_cat = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 26)

# ぷにまるマスコット(初回スモークテストのフレームを円形切り抜き)
cat_src = Image.open(OUT + r"\punimaru_smoke_00001_.webp").convert("RGB")
cw, chh = cat_src.size
box = (int(cw*0.18), int(chh*0.38), int(cw*0.82), int(chh*0.95))
cat = cat_src.crop(box).resize((240, 214))
mask = Image.new("L", cat.size, 0)
md = ImageDraw.Draw(mask)
md.ellipse([4, 4, cat.size[0]-4, cat.size[1]-4], fill=255)

def radial_bg(t):
    img = Image.new("RGB", (W, H), (255, 150, 20))
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    n = 18
    rot = t * 0.25
    for i in range(n):
        a0 = rot + i * 2 * math.pi / n
        a1 = a0 + math.pi / n
        R = 1200
        d.polygon([(cx, cy), (cx + R*math.cos(a0), cy + R*math.sin(a0)), (cx + R*math.cos(a1), cy + R*math.sin(a1))], fill=(255, 190, 40) if i % 2 else (255, 150, 20))
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

def make_frame(lines, tsukkomi, t, sec_len):
    img = radial_bg(t)
    d = ImageDraw.Draw(img)
    pop = min(1.0, t * 4)  # 文字ポップイン
    base_y = 240
    for i, line in enumerate(lines):
        col = "white" if i % 2 == 0 else (255, 245, 80)
        outlined(d, (W//2, base_y + i * 78), line, font_big, col)
    # ぷにまる+吹き出しツッコミ(後半で出す)
    img.paste(cat, (W//2 - 120, H - 260), mask)
    if tsukkomi and t > sec_len * 0.45:
        bx, by = W//2, H - 300
        d.rounded_rectangle([bx-190, by-26, bx+190, by+26], radius=22, fill="white", outline="black", width=3)
        d.text((bx, by), tsukkomi, font=font_cat, fill="black", anchor="mm")
    return img

out = av.open(OUT + r"\list_sample_final.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "20"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"
audio_all = np.zeros(0, dtype=np.int16)

for wav, lines, tsukkomi in SECTIONS:
    narr = read_wav(STG + "\\" + wav)
    sec_len = len(narr) / SR + 0.35
    total = int(sec_len * FPS)
    seg = np.zeros(total * SR // FPS, dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    for i in range(total):
        img = make_frame(lines, tsukkomi, i / FPS, sec_len)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
    print("section ok:", lines[0], total, "frames")

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
print("FINAL OK  total_sec =", len(audio_all) / SR)
