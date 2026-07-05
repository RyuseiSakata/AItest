# ローカル動画生成パイプライン構築手順(再現用)

対象マシン: Windows 11 / NVIDIA GPU(VRAM 8GB以上) / 空きディスク30GB以上
実績環境: RTX 3060 Ti(8GB)+ RAM 32GB — 2026-07-05に構築・動作確認済み

## 1. ComfyUI(ポータブル版)
1. https://github.com/comfyanonymous/ComfyUI/releases から `ComfyUI_windows_portable_nvidia.7z` を取得(実績: v0.27.0、1.94GB)
2. 7-Zip(単体版7zr.exeでも可)で `C:\Users\<user>\Tools\` に展開
3. **起動(重要)**: ログはファイルに直接書き出すこと。パイプ(| head等)に繋ぐとパイプ切断時に以降のジョブが全滅する(実際に起きた事故):
```
cd C:\Users\<user>\Tools\ComfyUI_windows_portable
python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --listen 127.0.0.1 --port 8188 > comfyui.log 2>&1
```

## 2. Wanモデル(Apache系ライセンス・商用可)
huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged の split_files から取得し、ComfyUI/models/ 配下へ:
- diffusion_models/: `wan2.1_t2v_1.3B_fp16.safetensors`(2.9GB・主力)、`wan2.1_t2v_14B_fp8_e4m3fn.safetensors`(14.3GB・高画質用、8GBでは低速)
- text_encoders/: `umt5_xxl_fp8_e4m3fn_scaled.safetensors`(6.7GB)
- vae/: `wan_2.1_vae.safetensors`(254MB)

## 3. 生成(API経由・全自動)
- ジョブテンプレ: `pipeline/wan_t2v_job_template.json`(このリポジトリ)
- 投入: `curl -X POST http://127.0.0.1:8188/prompt -d @job.json`
- 完了確認: `/history/<prompt_id>` または output/ フォルダ監視
- 実測性能(3060 Ti・1.3B・480x832): 33フレーム(2秒)≈2〜3分、81フレーム(5秒)≈7〜8分
- 標準パラメータ: steps 22〜25 / cfg 6.5 / uni_pc / simple

## 4. 音声(TTS)
- 無料・追加インストール不要: Windows内蔵SAPI(Microsoft Haruka Desktop)。PowerShellのSystem.Speechで一括WAV化(pipeline/内のスクリプト参照)。ロボ声感あり
- 本番品質は VOICEVOX(無料・商用可・要クレジット表記)への差し替えを推奨(未実装)

## 5. 編集・組み立て(Python)
ComfyUI同梱のpython_embeded(PyAV/PIL/numpy入り)で完結。ffmpeg不要:
- `pipeline/assemble_list_v4.py` — リスト系動画の完成形(文字送り・脈動・フラッシュ・コメントテロップ・進捗バー・音声mux)
- `pipeline/assemble_bridge.py` — ナレーション解説型(4カット+字幕+矢印+音声)
- `pipeline/assemble.py` — カット結合+テロップの基本形
- カラー絵文字は `seguiemj.ttf` + `embedded_color=True` で描画

## 6. 既知のハマりどころ
- ComfyUI起動のパイプ切断問題(上記)
- 日本語テキストは YuGothB.ttc。「❤」等の絵文字glyphは無いので「♡」を使うかemoji fontで描く
- SaveVideoの出力は output/ 直下(video/サブフォルダではない)
