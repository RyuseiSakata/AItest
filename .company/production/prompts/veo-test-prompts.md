# Veoテスト用プロンプト3本(Flow / Geminiにコピペ)

使い方: labs.google/flow を開く(Google AI Proのアカウントでログイン)→ 新規プロジェクト → 下のプロンプトを1つずつ貼って生成。
各プロンプト**2〜3回ずつ**生成すると、キャラの一貫性(毎回同じ見た目になるか)がわかります。
設定で縦型(9:16)を選択。まずは Fast モードでOK。

---

## テスト1: 基本ビジュアル(ぷにまるの見た目チェック)

A perfectly round, extremely fluffy white cat, almost spherical, short legs, small ears, sleepy half-closed deadpan eyes, tiny pink nose, sitting motionless on a tatami floor in a modern Japanese living room, soft natural light, photorealistic, vertical 9:16. The cat is completely still, only its fur sways slightly.

---

## テスト2: シグネチャ演出(最後の0.5秒だけ崩れる)

A perfectly round fluffy white cat with deadpan half-closed eyes sits completely motionless on a kitchen counter. A tangerine slowly rolls toward it. At the very last moment, the tangerine gently bumps the cat's nose and the cat's eyes suddenly open wide for a split second, then return to deadpan. Photorealistic, vertical 9:16, close-up.

---

## テスト3: もちもち質感(台本B-1「くすぐり検証」用)

Close-up of a human finger gently poking the belly of an extremely fluffy, round white cat. The fur and skin sink softly like mochi. The cat's deadpan face doesn't react at all. Photorealistic, vertical 9:16, soft indoor lighting.

---

## チェックポイント(生成結果を見るときの目)
1. 毛並みが溶けたり不自然に崩れたりしないか
2. 「ジト目・無表情」が守られるか(勝手に目がぱっちり開いたりしないか)
3. 何回生成したら「使える」ものが出るか(歩留まり) → 回数をメモしておいてください
4. テスト2で「最後だけ目を見開く」の演技指示が通るか(これが通るツールは台本の再現力が高い)
