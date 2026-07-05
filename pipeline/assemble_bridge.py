# -*- coding: utf-8 -*-
# 橋動画の模写: 4ショット+ナレーション+テロップ → 完成mp4
import av
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS = 480, 832, 16
SR = 22050  # SAPI wav sample rate

# (映像, ナレーションwav, 字幕リスト[(開始秒, テキスト)], 矢印を出すか)
SHOTS = [
    (OUT + r"\bridge_s1_00001_.mp4", STG + r"\narr1.wav", [(0.0, "両岸から同時に"), (1.8, "作られていた、この橋。")], False),
    (OUT + r"\bridge_s2_00001_.mp4", STG + r"\narr2.wav", [(0.0, "しかし完成直前、"), (2.0, "中央で大きなズレが発覚")], True),
    (OUT + r"\bridge_s3_00001_.mp4", STG + r"\narr3.wav", [(0.0, "原因は、両国で"), (1.8, "「海抜ゼロ」の基準が違ったこと"), (4.6, "その差、54センチ。")], False),
    (OUT + r"\bridge_s4_00001_.mp4", STG + r"\narr4.wav", [(0.0, "設計は完璧でも、"), (2.2, "前提が違えば、橋はつながらない。")], False),
]
TITLE1 = "完成直前に大きなズレ!?"
TITLE2 = "橋建設の意外な真実"

font_title = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 32)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 28)

def outlined(d, xy, text, font, fill, outline, ow=3, anchor="ma"):
    x, y = xy
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx or dy:
                d.text((x + dx, y + dy), text, font=font, fill=outline, anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getframerate() == SR, w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            data = data[::2]
    return data

def annotate(img, subs, t, arrow):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 92], fill="white")
    d.text((W // 2, 10), TITLE1, font=font_title, fill="black", anchor="ma")
    d.text((W // 2, 50), TITLE2, font=font_title, fill=(200, 30, 30), anchor="ma")
    active = [s for (st, s) in subs if t >= st]
    for i, line in enumerate(active[-2:]):
        outlined(d, (W // 2, H - 240 + i * 44), line, font_sub, "white", (90, 30, 140))
    if arrow and t > 1.0:
        ax, ay = W // 2, H // 2 - 40
        d.line([ax + 60, ay - 90, ax + 8, ay - 8], fill="red", width=10)
        d.polygon([(ax, ay), (ax + 34, ay - 10), (ax + 6, ay - 36)], fill="red")
    return img

out = av.open(OUT + r"\bridge_replica_final.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "20"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"

audio_all = np.zeros(0, dtype=np.int16)

for path, wav, subs, arrow in SHOTS:
    c = av.open(path)
    frames = [f.to_image() for f in c.decode(video=0)]
    c.close()
    narr = read_wav(wav)
    need_sec = max(len(frames) / FPS, len(narr) / SR + 0.3)
    total_frames = int(need_sec * FPS)
    while len(frames) < total_frames:
        frames.append(frames[-1].copy())  # 音声が長い分は最終フレームで静止
    seg = np.zeros(total_frames * SR // FPS, dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    for i, img in enumerate(frames):
        img = annotate(img.convert("RGB").resize((W, H)), subs, i / FPS, arrow)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
    print("shot ok:", path.split("\\")[-1], total_frames, "frames")

chunk = 1024
for i in range(0, len(audio_all), chunk):
    seg = audio_all[i : i + chunk]
    af = av.AudioFrame.from_ndarray(seg.reshape(1, -1), format="s16", layout="mono")
    af.sample_rate = SR
    for pkt in asr.encode(af):
        out.mux(pkt)
for pkt in vs.encode():
    out.mux(pkt)
for pkt in asr.encode():
    out.mux(pkt)
out.close()
print("FINAL OK: bridge_replica_final.mp4  total_sec =", len(audio_all) / SR)
