# プロンプト知見集(Wan 2.1 1.3B 実測ベース)

2026-07-05〜06の実生成で得た知見。全て実際の成功/失敗から。

## 画風の制御(最重要)
- **素の指示 → 3Dアニメ調に寄る**(Wanのデフォルトバイアス)。かわいいマスコット系には逆に好適
- **実写にしたい場合**: `Smartphone home video / documentary pet video style / handheld camera shake / realistic detailed fur with individual strands` を正方向に、`anime, cartoon, 3d render, cgi, illustration, stylized` をネガティブに入れる。これだけで別モデル級に変わる(実証済み)
- **アニメ調を活かす場合**: `Cute 3D animated cartoon style, chibi mascot style, soft pastel colors` — ぷにまるの演技クリップはこれ

## 人物(美少女系)の制御
- **素の指示 → 中国系の顔・スタイリングに寄る**(学習データバイアス)。`Japanese` の明示+`natural cute makeup` で日本寄りに補正
- **「かわいい」の水準はキーワードで階級が変わる**: 素人っぽい子=`casual, amateur video` / アイドル級=`K-pop idol fancam, professional idol makeup, dewy glowing skin, big sparkling eyes with aegyo-sal, glossy gradient lips, broadcast quality`。後者で顔の造形が激変(実証済み)
- **要注意の単語**: `wolf cut`(髪型)→ **本物の獣耳が生える**。動物名を含む髪型名は使わず `shaggy layered haircut with choppy face-framing layers and wispy bangs` のように記述で指定
- インナーカラーは位置まで書く: `black hair with vivid blue peeking through the under-layers at the nape`(単に blue inner color だと髪全体が青くなる)

## キャラ固定(ぷにまる)の学び
- 共通ヘッダ: 「真っ白で異常にまん丸(ほぼ球体)、短足、小さい耳、半目のジト目、小さいピンクの鼻、もちもちの毛」
- 「半目のジト目」は `sleepy half-closed deadpan eyes` でも**閉じ目になりがち**(未解決・要チューニング)
- **ショット間の一貫性が最大の課題**: 同プロンプトでも毛色・小物が変わる。対策=i2v方式(決め画像から動かす)か上位モデルのキャラ参照機能(未実施)
- 静止推奨キャラ(動かない設定)は生成破綻が少ない=弱いモデルと相性が良い

## 動きの制御
- 激しいダンス等の速い全身運動は1.3Bの最弱点(手指・関節の破綻リスク)。`simple cute hand-gesture dance with small rhythmic steps` のように**小さい動き**に限定すると歩留まりが上がる
- 顔のクローズアップ(ファンカム構図)は全身より破綻しにくい

## ネガティブプロンプトの定番セット
```
extra fingers, deformed hands, extra limbs, blurry face,
色调艳丽，过曝，细节模糊不清，最差质量，低质量，畸形的，多余的手指，
画得不好的手部，画得不好的脸部，形态畸形的肢体，手指融合，三条腿
```
(Wanは中国製のため中国語ネガティブが効く。公式テンプレ由来)

## 歩留まり実績(参考)
- 猫・風景・静止気味の人物: ほぼ1発OK
- 手と物の相互作用(仮面をかぶせる等): 1発OKもあったが本来は2〜4回想定
- 顔が光の塊で潰れる等の大破綻: 体感1〜2割で発生。品質足切りで再生成
