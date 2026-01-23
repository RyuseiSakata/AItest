import { staticFile } from 'remotion';

export type CharacterId = 'Ai' | 'Mai' | 'None';

export interface DialogueLine {
  id: string;
  character: CharacterId;
  text: string;
  background?: string; // Optional background override
}

export const dialogueData: DialogueLine[] = [
  // Intro
  {
    id: 'intro-1',
    character: 'Mai',
    text: 'ねえねえアイ先生！また新しい年が来たけど、AIってどうなったの？',
    background: staticFile('agentic_ai.png'),
  },
  {
    id: 'intro-2',
    character: 'Ai',
    text: 'ふふっ、気になる？2026年はすごいわよ。「エージェンティックAI」が主役の年ね。',
    background: staticFile('agentic_ai.png'),
  },

  // Agentic AI
  {
    id: 'agentic-1',
    character: 'Mai',
    text: 'エージェンティック…？なにそれ、スパイ映画？',
    background: staticFile('agentic_ai.png'),
  },
  {
    id: 'agentic-2',
    character: 'Ai',
    text: '違うわよ（笑）。自律的に考えて行動するAIのこと。もうただのツールじゃなくて「同僚」なの。',
    background: staticFile('agentic_ai.png'),
  },
  {
    id: 'agentic-3',
    character: 'Mai',
    text: 'ええっ！じゃあ私の宿題も勝手にやってくれる同僚が欲しい〜！',
    background: staticFile('agentic_ai.png'),
  },

  // Physical AI
  {
    id: 'physical-1',
    character: 'Ai',
    text: 'それはどうかしら…。でも、工場や街中ではロボットとAIが融合して働いているわ。',
    background: staticFile('physical_ai.png'),
  },
  {
    id: 'physical-2',
    character: 'Mai',
    text: 'あ！そういえば最近、カフェの店員さんがロボットだったかも！',
    background: staticFile('physical_ai.png'),
  },

  // Science
  {
    id: 'science-1',
    character: 'Ai',
    text: 'そう、それが日常になっていくの。さらに科学の世界でも大活躍よ。',
    background: staticFile('scifi_ai.png'),
  },
  {
    id: 'science-2',
    character: 'Ai',
    text: '新薬の開発とか、ものすごいスピードで進んでいるの。数年の実験が数週間に短縮されるのよ。',
    background: staticFile('scifi_ai.png'),
  },
  {
    id: 'science-3',
    character: 'Mai',
    text: 'へぇ〜、病気がすぐ治るようになるなら嬉しいな。',
    background: staticFile('scifi_ai.png'),
  },

  // Quantum
  {
    id: 'quantum-1',
    character: 'Ai',
    text: 'そして極めつけは「量子コンピュータ」との融合ね。',
    background: staticFile('quantum_ai.png'),
  },
  {
    id: 'quantum-2',
    character: 'Mai',
    text: 'りょうし…？難しすぎて眠くなってきた…',
    background: staticFile('quantum_ai.png'),
  },
  {
    id: 'quantum-3',
    character: 'Ai',
    text: '簡単に言うと、スーパーコンピュータでも無理な計算を瞬時にやっちゃう最強コンビってこと！',
    background: staticFile('quantum_ai.png'),
  },

  // Outro
  {
    id: 'outro-1',
    character: 'Mai',
    text: 'なるほど！なんかワクワクしてきた！先生、もっと教えて！',
    background: staticFile('quantum_ai.png'),
  },
  {
    id: 'outro-2',
    character: 'Ai',
    text: 'ふふ、じゃあ次はプログラミングを教えようかしら。未来は自分で作るものよ！',
    background: staticFile('agentic_ai.png'),
  },
];

export const TOTAL_DURATION_SEC = dialogueData.length * 6; // Approx duration
