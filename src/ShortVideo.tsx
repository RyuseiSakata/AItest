import { AbsoluteFill, Img, interpolate, Sequence, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { dialogueData } from './data/news-data';
import { FONT_FAMILY } from './constants';

const ShortSoloScene: React.FC<{ character: string; text: string; bg: string }> = ({ character, text, bg }) => {
    const frame = useCurrentFrame();

    const scale = interpolate(frame, [0, 100], [1, 1.1]);
    const charTranslateY = interpolate(frame, [0, 10], [50, 0], { extrapolateRight: 'clamp' });

    const charImg = character === 'Ai' ? staticFile('char_ai.png') : staticFile('char_mai.png');

    return (
        <AbsoluteFill>
            {/* Background */}
            <Img src={bg} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})` }} />
            <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.3)' }} />

            {/* Character */}
            <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
                <Img
                    src={charImg}
                    style={{
                        width: '120%',
                        height: 'auto',
                        marginBottom: -100, // Close up
                        transform: `translateY(${charTranslateY}px)`,
                    }}
                />
            </AbsoluteFill>

            {/* Text Bubble - Top or Middle to not cover face? Or bottom overlay? 
               For shorts, usually center or top is good, but let's stick to bottom overlay for readability */}
            <div style={{
                position: 'absolute',
                top: 200, // Top placement for Shorts often works better to avoid UI
                left: 40,
                right: 40,
            }}>
                <div style={{
                    backgroundColor: 'rgba(255,255,255,0.95)',
                    padding: 40,
                    borderRadius: 30,
                    border: `8px solid ${character === 'Ai' ? '#4dabf7' : '#ff8787'}`,
                    boxShadow: '0 8px 16px rgba(0,0,0,0.3)'
                }}>
                    <h2 style={{
                        fontFamily: FONT_FAMILY,
                        fontSize: 50,
                        color: character === 'Ai' ? '#4dabf7' : '#ff8787',
                        margin: 0,
                        marginBottom: 10,
                        textAlign: 'left'
                    }}>
                        {character === 'Ai' ? 'Ai 先生' : 'Mai'}
                    </h2>
                    <p style={{
                        fontFamily: FONT_FAMILY,
                        fontSize: 65,
                        color: '#222',
                        margin: 0,
                        fontWeight: 'bold',
                        lineHeight: 1.3,
                        textAlign: 'left'
                    }}>
                        {text}
                    </p>
                </div>
            </div>
        </AbsoluteFill>
    );
};

export const ShortVideo: React.FC = () => {
    const { fps } = useVideoConfig(); // 30fps
    const SLIDE_DURATION_FRAMES = 5 * fps;

    return (
        <AbsoluteFill style={{ backgroundColor: 'black' }}>
            {dialogueData.map((item, index) => {
                const bg = item.background || staticFile('agentic_ai.png');
                return (
                    <Sequence key={item.id} from={index * SLIDE_DURATION_FRAMES} durationInFrames={SLIDE_DURATION_FRAMES}>
                        <ShortSoloScene
                            character={item.character}
                            text={item.text}
                            bg={bg}
                        />
                    </Sequence>
                );
            })}
        </AbsoluteFill>
    );
};
