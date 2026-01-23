import subprocess
import os

# Dialogue Data (Same as before)
dialogue_data = [
  { 'id': 'intro-1', 'char': 'Mai', 'text': 'ねえねえアイ先生！また新しい年が来たけど、AIってどうなったの？' },
  { 'id': 'intro-2', 'char': 'Ai', 'text': 'ふふっ、気になる？2026年はすごいわよ。「エージェンティックAI」が主役の年ね。' },
  { 'id': 'agentic-1', 'char': 'Mai', 'text': 'エージェンティック…？なにそれ、スパイ映画？' },
  { 'id': 'agentic-2', 'char': 'Ai', 'text': '違うわよ。自律的に考えて行動するAIのこと。もうただのツールじゃなくて「同僚」なの。' },
  { 'id': 'agentic-3', 'char': 'Mai', 'text': 'ええっ！じゃあ私の宿題も勝手にやってくれる同僚が欲しい〜！' },
  { 'id': 'physical-1', 'char': 'Ai', 'text': 'それはどうかしら…。でも、工場や街中ではロボットとAIが融合して働いているわ。' },
  { 'id': 'physical-2', 'char': 'Mai', 'text': 'あ！そういえば最近、カフェの店員さんがロボットだったかも！' },
  { 'id': 'science-1', 'char': 'Ai', 'text': 'そう、それが日常になっていくの。さらに科学の世界でも大活躍よ。' },
  { 'id': 'science-2', 'char': 'Ai', 'text': '新薬の開発とか、ものすごいスピードで進んでいるの。数年の実験が数週間に短縮されるのよ。' },
  { 'id': 'science-3', 'char': 'Mai', 'text': 'へぇ〜、病気がすぐ治るようになるなら嬉しいな。' },
  { 'id': 'quantum-1', 'char': 'Ai', 'text': 'そして極めつけは「量子コンピュータ」との融合ね。' },
  { 'id': 'quantum-2', 'char': 'Mai', 'text': 'りょうし…？難しすぎて眠くなってきた…' },
  { 'id': 'quantum-3', 'char': 'Ai', 'text': '簡単に言うと、スーパーコンピュータでも無理な計算を瞬時にやっちゃう最強コンビってこと！' },
  { 'id': 'outro-1', 'char': 'Mai', 'text': 'なるほど！なんかワクワクしてきた！先生、もっと教えて！' },
  { 'id': 'outro-2', 'char': 'Ai', 'text': 'ふふ、じゃあ次はプログラミングを教えようかしら。未来は自分で作るものよ！' },
]

output_dir = "public/audio"
os.makedirs(output_dir, exist_ok=True)

for item in dialogue_data:
    filename = f"{output_dir}/{item['id']}.wav"
    
    # Settings
    voice = "Kyoko"
    rate = "180" if item['char'] == 'Ai' else "220"
    
    # Command: Output as WAVE
    # --data-format=LEI16@44100 is standard PCM WAV
    cmd = ["say", "-v", voice, "-r", rate, item['text'], "-o", filename, "--data-format=LEI16@44100"]
    
    print(f"Generating {item['id']} ({item['char']})...")
    subprocess.run(cmd, check=True)
