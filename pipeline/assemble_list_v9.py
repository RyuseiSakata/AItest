# -*- coding: utf-8 -*-
# v9: 和モダン編集 + ドーパミン装置3点
#  ①0秒フック(フルスクリーンぷにまる+問いの一撃) ②中間パターン割り込み(朱スラム)
#  ③BGMに前進ビート(和太鼓パルス+ウッドブロック)
import av
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\sakat\Tools\ComfyUI_windows_portable\ComfyUI\output"
STG = r"C:\Users\sakat\Tools\comfy-staging"
W, H, FPS, SR = 720, 1248, 24, 22050
PAPER = (247, 244, 238)
SUMI = (34, 33, 31)
SHU = (196, 64, 52)
FADE_INK = (34, 33, 31, 38)

# (kind, wav, 見出し, num, セリフ, 付箋, アニメ)
SECTIONS = [
    ("hook",      "v9_hook0.wav", ["3つ当てはまったら", "人生、溶けてます。"], "", "", [], "anim_00"),
    ("item",      "v2_1.wav",  ["無限", "スクロール"],      "01", "朝後悔するやつにゃ", ["気づいたら3時", "わかりすぎる"], "anim_01"),
    ("item",      "v2_2.wav",  ["「あとで」の", "在庫化"],   "02", "在庫は腐るにゃ", ["タブ100個ある", "積読も同じ"], "anim_02"),
    ("item",      "v2_3.wav",  ["通知の", "即開封"],        "03", "犬すぎるにゃ", ["既読つけたら負け", "休憩が終わらん"], "anim_03"),
    ("item",      "v2_4.wav",  ["迷ったら", "課金"],        "04", "財布が痩せるにゃ", ["ガチャのことか", "限定に弱い"], "anim_04"),
    ("item",      "v2_5.wav",  ["口癖、", "「疲れた」。"],   "05", "言うほど疲れるにゃ", ["言うと余計疲れる", "口癖になってた"], "anim_05"),
    ("interrupt", "v9_hook1.wav", ["ここまでで2つ、", "もう危ない。"], "", "", [], "anim_05"),
    ("item",      "v2_6.wav",  ["寝溜めで", "休日消滅"],     "06", "猫でも予定あるにゃ", ["起きたら夕方", "休日どこ行った"], "anim_06"),
    ("item",      "v2_7.wav",  ["他人の成功の", "見すぎ"],   "07", "よそのchにゃ", ["比較して病むやつ", "見るだけで満足"], "anim_07"),
    ("item",      "v2_8.wav",  ["「明日から", "本気」更新"], "08", "聞き飽きたにゃ", ["万年明日組w", "通知は消した"], "anim_08"),
    ("item",      "v2_9.wav",  ["完璧な計画で", "満足"],     "09", "やるのは今日にゃ", ["計画だけA評価", "ノートだけ綺麗"], "anim_09"),
    ("item",      "v2_10.wav", ["3つ以上は、", "保存。"],    "",   "数はコメントで晒すにゃ", ["4つだった…", "保存した"], "anim_10"),
]

def gothic(size): return ImageFont.truetype(r"C:\Windows\Fonts\YuGothB.ttc", size)
def mincho(size): return ImageFont.truetype(r"C:\Windows\Fonts\yumindb.ttf", size)
def bizgo(size):  return ImageFont.truetype(r"C:\Windows\Fonts\BIZ-UDGothicB.ttc", size)

def ease_out_expo(x):
    return 1 if x >= 1 else 1 - 2 ** (-10 * max(0.0, x))

def ease_out_back(x, s=1.2):
    x = min(1.0, max(0.0, x))
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2

BG = Image.new("RGBA", (W, H), PAPER + (255,))
rng = np.random.default_rng(3)
noise = Image.fromarray(rng.integers(0, 14, (H//2, W//2), dtype=np.uint8), "L").resize((W, H))
BG.paste((225, 220, 210), (0, 0), noise)

ANIM_SIZE = 500
anim_mask = Image.new("L", (ANIM_SIZE, ANIM_SIZE), 0)
ImageDraw.Draw(anim_mask).rounded_rectangle([0, 0, ANIM_SIZE, ANIM_SIZE], radius=18, fill=255)
CARD_SHADOW = Image.new("RGBA", (ANIM_SIZE + 140, ANIM_SIZE + 140), (0, 0, 0, 0))
ImageDraw.Draw(CARD_SHADOW).rounded_rectangle([70, 84, ANIM_SIZE + 70, ANIM_SIZE + 84], radius=24, fill=(60, 50, 40, 90))
CARD_SHADOW = CARD_SHADOW.filter(ImageFilter.GaussianBlur(22))

def load_clip(prefix, size=ANIM_SIZE):
    c = av.open(OUT + "\\" + prefix + "_00001_.mp4")
    frames = [f.to_image().resize((size, size)) for f in c.decode(video=0)]
    c.close()
    return frames

def read_wav(path):
    with wave.open(path, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            data = data[::2]
    return data

def fade_layer(img, alpha, draw_fn):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer), layer)
    if alpha < 255:
        layer.putalpha(layer.getchannel("A").point(lambda a: a * alpha // 255))
    img.alpha_composite(layer)

def punch_text(img, xy, text, base_size, fill, t, at, font_fn=mincho, dur=0.16):
    """速いパンチイン(1.25→1.0のオーバーシュート)= ドーパミン系の登場"""
    if t < at:
        return
    k = ease_out_back((t - at) / dur, s=2.2)
    size = max(8, int(base_size * (1.3 - 0.3 * k)))
    alpha = int(255 * min(1.0, (t - at) / 0.06))
    fade_layer(img, alpha, lambda ld, ly: ld.text(xy, text, font=font_fn(size), fill=fill, anchor="mm"))

def frame_hook(t, sec_len, clip, progress):
    img = BG.copy()
    # フルスクリーン幅のぷにまる(溶けるアニメ)
    frame_idx = int(t * 16) % len(clip)
    big = clip[frame_idx].resize((W, W))
    img.paste(big, (0, 290))
    # 上下を紙にフェード
    d = ImageDraw.Draw(img)
    punch_text(img, (W//2, 170), "3つ当てはまったら", 66, SUMI, t, 0.02)
    punch_text(img, (W//2, 1105), "人生、溶けてます。", 74, SHU, t, 0.5)
    lk = ease_out_expo((t - 0.75) / 0.3)
    if lk > 0:
        d.line([W//2 - int(170*lk), 1168, W//2 + int(170*lk), 1168], fill=SHU, width=3)
    d.rectangle([0, H-5, int(W * progress), H], fill=SHU)
    return img.convert("RGB")

def frame_interrupt(t, sec_len, progress):
    img = Image.new("RGBA", (W, H), SHU + (255,))
    img.paste((160, 48, 40), (0, 0), noise)
    punch_text(img, (W//2, 520), "ここまでで2つ、", 74, (255, 250, 242), t, 0.02)
    punch_text(img, (W//2, 680), "もう危ない。", 88, (255, 250, 242), t, 0.4)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H-5, int(W * progress), H], fill=(255, 250, 242, 255))
    return img.convert("RGB")

def frame_item(idx, lines, num, gag, fusen, t, sec_len, progress, clip):
    img = BG.copy()
    d = ImageDraw.Draw(img)
    lk = ease_out_expo(t / 0.35)
    if lk > 0:
        fade_layer(img, int(255 * lk), lambda ld, ly: ld.text((60, 66), "人生を溶かす習慣", font=gothic(26), fill=SHU))
        d.line([60, 108, 60 + int(140 * ease_out_expo((t - 0.1) / 0.4)), 108], fill=SHU, width=2)
    for li, line in enumerate(lines):
        delay = 0.06 + li * 0.12
        k = ease_out_expo((t - delay) / 0.45)
        if k <= 0:
            continue
        size = 84 if max(len(l) for l in lines) <= 6 else 66
        y = 190 + li * (size + 22) + int(26 * (1 - k))
        fade_layer(img, int(255 * k), lambda ld, ly, _l=line, _y=y, _s=size: ld.text((48, _y), _l, font=mincho(_s), fill=SUMI))
    if num:
        nk = ease_out_expo((t - 0.12) / 0.5)
        if nk > 0:
            nsize = int(170 * (1.05 - 0.05 * nk))
            fade_layer(img, int(255 * nk), lambda ld, ly: ld.text((W - 70, 210), num, font=mincho(nsize), fill=FADE_INK, anchor="mm"))
            fade_layer(img, int(255 * nk), lambda ld, ly: ld.text((W - 70, 318), "— 09", font=gothic(24), fill=(120, 116, 108), anchor="mm"))
    ck = ease_out_back(t / 0.35, s=0.9)
    size_now = max(2, int(ANIM_SIZE * (0.92 + 0.08 * ck)))
    pad = 14
    cx0 = W//2 - (size_now + pad*2)//2
    cy0 = 430 + (ANIM_SIZE - size_now)//2
    img.alpha_composite(CARD_SHADOW.resize((size_now + 140, size_now + 140)), (cx0 - 70 + pad, cy0 - 70 + pad))
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle([cx0, cy0, cx0 + size_now + pad*2, cy0 + size_now + pad*2], radius=22, fill=(255, 255, 255, 255))
    frame_idx = int(t * 16) % len(clip)
    cf = clip[frame_idx].resize((size_now, size_now))
    m = anim_mask.resize((size_now, size_now))
    img.paste(cf, (cx0 + pad, cy0 + pad), m)
    f_at = [sec_len * 0.22, sec_len * 0.5]
    f_pos = [(56, 1000, 1.5), (330, 1086, -1.2)]
    for fi, text in enumerate(fusen):
        if t < f_at[fi]:
            continue
        age = t - f_at[fi]
        k = ease_out_back(age / 0.26, s=1.0)
        alpha = int(255 * min(1.0, age / 0.12))
        x, y, tilt = f_pos[fi]
        f = bizgo(28)
        tmp = Image.new("RGBA", (460, 100), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        tw = td.textlength(text, font=f)
        sh = Image.new("RGBA", (460, 100), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([12, 18, tw + 52, 88], radius=6, fill=(60, 50, 40, 70))
        tmp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        td.rounded_rectangle([8, 10, tw + 48, 80], radius=6, fill=(255, 252, 240, 255), outline=(210, 200, 180, 255), width=2)
        td.text((28, 45), text, font=f, fill=SUMI, anchor="lm")
        tmp = tmp.rotate(tilt, resample=Image.BICUBIC, expand=False)
        tmp.putalpha(tmp.getchannel("A").point(lambda a: a * alpha // 255))
        img.alpha_composite(tmp, (x, y + int(20 * (1 - k))))
    g_at = min(0.55, sec_len * 0.32)
    if gag and t >= g_at:
        gk = ease_out_expo((t - g_at) / 0.35)
        fade_layer(img, int(255 * gk), lambda ld, ly: ld.text((W//2, 1196), "ぷにまる「" + gag + "」", font=gothic(30), fill=SUMI, anchor="mm"))
    d3 = ImageDraw.Draw(img)
    d3.rectangle([0, H-5, int(W * progress), H], fill=SHU + (255,))
    if t < 0.12:
        dip = (0.12 - t) / 0.12 * 0.7
        paper = Image.new("RGBA", img.size, PAPER + (int(255 * dip),))
        img = Image.alpha_composite(img, paper)
    return img.convert("RGB")

# ===== 効果音(自前合成) =====
def env(n, attack=0.005, release=None):
    e = np.ones(n)
    a = max(1, int(attack * SR))
    e[:a] = np.linspace(0, 1, a)
    r = n - a if release is None else max(1, int(release * SR))
    e[-r:] *= np.linspace(1, 0, r)
    return e

def se_pop():
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = 660 * np.exp(-t * 18) + 240
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002) * 0.5

def se_shu():
    n = int(0.14 * SR)
    x = np.convolve(np.random.default_rng(1).normal(0, 1, n), np.ones(24)/24, mode="same")
    return x * env(n, 0.01) * 0.28

def se_ton():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 130 * t) * np.exp(-t * 30) * 0.6

def se_don():  # フック/割り込み用の強い一撃
    n = int(0.3 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (90 * np.exp(-t * 6) + 55) * t) * np.exp(-t * 9)
    x += np.random.default_rng(4).normal(0, 0.12, n) * np.exp(-t * 40)
    return x * 0.9

def se_swoosh():
    n = int(0.2 * SR)
    x = np.convolve(np.random.default_rng(2).normal(0, 1, n), np.ones(10)/10, mode="same")
    return x * np.linspace(1.0, 0.15, n) * env(n, 0.004) * 0.35

def se_nya():
    n = int(0.1 * SR); t = np.arange(n) / SR
    f = 380 + 480 * t / t[-1]
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.004) * 0.3

def make_bgm(total_sec):
    n = int(total_sec * SR)
    out_a = np.zeros(n)
    chords = [(220.0, 261.63, 329.63), (196.0, 246.94, 293.66), (174.61, 220.0, 261.63), (196.0, 246.94, 329.63)]
    beat = 2.0
    for i in range(int(total_sec / beat) + 1):
        s = int(i * beat * SR); e_ = min(n, int((i + 1) * beat * SR))
        if s >= n: break
        tt = np.arange(e_ - s) / SR
        ev = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.9)
        for f in chords[i % 4]:
            out_a[s:e_] += (np.sin(2*np.pi*f*tt) * 0.5 + np.sin(2*np.pi*f*2*tt) * 0.12) * ev
    out_a *= 0.09
    # 前進ビート: 和太鼓パルス(0.6秒間隔)+ウッドブロック(裏拍)
    pulse = 0.6
    for i in range(int(total_sec / pulse) + 1):
        s = int(i * pulse * SR)
        nn = min(int(0.1 * SR), n - s)
        if nn <= 0: break
        tt = np.arange(nn) / SR
        out_a[s:s+nn] += np.sin(2*np.pi*70*tt) * np.exp(-tt * 42) * 0.24
        # 裏拍ウッドブロック
        s2 = s + int(pulse/2 * SR)
        nn2 = min(int(0.04 * SR), n - s2)
        if nn2 > 0:
            tt2 = np.arange(nn2) / SR
            out_a[s2:s2+nn2] += np.sin(2*np.pi*1150*tt2) * np.exp(-tt2 * 130) * 0.10
    # ヴァイナル
    rng2 = np.random.default_rng(9)
    for p in rng2.integers(0, n, int(total_sec * 6)):
        k = min(60, n - p)
        out_a[p:p+k] += np.linspace(0.5, 0, k) * rng2.normal(0, 0.22) * 0.4
    return out_a

# ===== 組み立て =====
out = av.open(OUT + r"\list_sample_v9.mp4", "w")
vs = out.add_stream("h264", rate=FPS)
vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "19"}
asr = out.add_stream("aac", rate=SR)
asr.layout = "mono"
audio_all = np.zeros(0, dtype=np.int16)

pads = {"hook": 0.45, "interrupt": 0.25, "item": 0.12}
durs = [len(read_wav(STG + "\\" + s[1])) / SR + pads[s[0]] for s in SECTIONS]
total_dur = sum(durs)

se_events = []
_start = 0.0
for i, sec in enumerate(SECTIONS):
    kind = sec[0]; sl = durs[i]
    if kind == "hook":
        se_events += [(_start + 0.02, se_don), (_start + 0.5, se_don)]
    elif kind == "interrupt":
        se_events += [(_start + 0.02, se_don), (_start + 0.4, se_ton)]
    else:
        se_events += [(_start, se_swoosh), (_start + 0.08, se_shu)]
        if sec[3]:
            se_events.append((_start + 0.2, se_ton))
        se_events += [(_start + sl * 0.22, se_pop), (_start + sl * 0.5, se_pop),
                      (_start + min(0.55, sl * 0.32), se_nya)]
    _start += sl

elapsed = 0.0
for idx, (kind, wav, lines, num, gag, fusen, animp) in enumerate(SECTIONS):
    sec_len = durs[idx]
    total = int(sec_len * FPS)
    narr = read_wav(STG + "\\" + wav)
    seg = np.zeros(int(total * SR / FPS), dtype=np.int16)
    seg[: len(narr)] = narr
    audio_all = np.concatenate([audio_all, seg])
    clip = load_clip(animp, W if kind == "hook" else ANIM_SIZE)
    for i in range(total):
        prog = (elapsed + i / FPS) / total_dur
        t = i / FPS
        if kind == "hook":
            img = frame_hook(t, sec_len, clip, prog)
        elif kind == "interrupt":
            img = frame_interrupt(t, sec_len, prog)
        else:
            img = frame_item(idx, lines, num, gag, fusen, t, sec_len, prog, clip)
        for pkt in vs.encode(av.VideoFrame.from_image(img)):
            out.mux(pkt)
    elapsed += sec_len
    print("sec ok:", idx, kind)

mix = audio_all.astype(np.float64)
for (at, fn) in se_events:
    s = int(at * SR)
    x = fn() * 32767
    e_ = min(len(mix), s + len(x))
    if s < len(mix):
        mix[s:e_] += x[: e_ - s]
mix += make_bgm(len(mix) / SR)[: len(mix)] * 32767
mix = np.clip(mix, -32000, 32000).astype(np.int16)

for i in range(0, len(mix), 1024):
    seg = mix[i:i+1024]
    af = av.AudioFrame.from_ndarray(seg.reshape(1, -1), format="s16", layout="mono")
    af.sample_rate = SR
    for pkt in asr.encode(af):
        out.mux(pkt)
for pkt in vs.encode():
    out.mux(pkt)
for pkt in asr.encode():
    out.mux(pkt)
out.close()
print("V9 OK  total_sec =", len(mix) / SR)
