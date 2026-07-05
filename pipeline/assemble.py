# -*- coding: utf-8 -*-
# 模写チャレンジ: 3ショットをテロップ付き1本のmp4に組み上げる
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
SHOTS = [
    (OUT_DIR + r"\ref_shot1_mp4_00001_.mp4", None),
    (OUT_DIR + r"\ref_shot2_mp4_00001_.mp4", None),
    (OUT_DIR + r"\ref_shot3_mp4_00001_.mp4", ("これ何にゃ!?", "キュン…♡")),
]
TITLE1 = "猫に仮面をかぶせたら…"
TITLE2 = "可愛すぎない!?"
W, H, FPS = 480, 832, 16

font_big = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 34)
font_mid = ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", 30)

def draw_outlined(draw, xy, text, font, fill, outline="black", ow=3, anchor="ma"):
    x, y = xy
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=outline, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def annotate(img, shot_caption, frame_idx, total):
    d = ImageDraw.Draw(img)
    # 上部の白帯+タイトル(元動画の形式)
    d.rectangle([0, 0, W, 96], fill="white")
    d.text((W // 2, 12), TITLE1, font=font_big, fill="black", anchor="ma")
    d.text((W // 2, 52), TITLE2, font=font_big, fill=(200, 120, 0), anchor="ma")
    if shot_caption:
        draw_outlined(d, (W // 2, H - 250), shot_caption[0], font_mid, "white")
        if frame_idx > total * 0.5:
            draw_outlined(d, (W // 2, H - 200), shot_caption[1], font_mid, (255, 150, 180))
    return img

out = av.open(OUT_DIR + r"\replica_final.mp4", "w")
stream = out.add_stream("h264", rate=FPS)
stream.width, stream.height, stream.pix_fmt = W, H, "yuv420p"
stream.options = {"crf": "20"}

for path, caption in SHOTS:
    container = av.open(path)
    frames = [f.to_image() for f in container.decode(video=0)]
    container.close()
    n = len(frames)
    for i, img in enumerate(frames):
        img = img.convert("RGB").resize((W, H))
        img = annotate(img, caption, i, n)
        frame = av.VideoFrame.from_image(img)
        for pkt in stream.encode(frame):
            out.mux(pkt)
    print(f"shot done: {path} ({n} frames)")

for pkt in stream.encode():
    out.mux(pkt)
out.close()
print("FINAL OK:", OUT_DIR + r"\replica_final.mp4")
