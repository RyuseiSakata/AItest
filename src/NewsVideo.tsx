import { AbsoluteFill, Img, interpolate, Sequence, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { dialogueData } from './data/news-data';
import { FONT_FAMILY } from './constants';

const SoloScene: React.FC<{
    character: string;
    text: string;
    bg: string;
    prevBg?: string;
}> = ({ character, text, bg, prevBg }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Smooth transition for background
    // Note: In this simple sequence setup, we only render the current bg. 
    // For smoother transitions between scenes, we rely on the sequence cut itself.

    // Character Entry Animation
    // Fade in and slight slide up
    const charOpacity = interpolate(frame, [0, 10], [0, 1]);
    const charTranslateY = interpolate(frame, [0, 15], [50, 0], { extrapolateRight: 'clamp' });

    // Character Image
    const charImg = character === 'Ai' ? staticFile('char_ai.png') : staticFile('char_mai.png');

    return (
        <AbsoluteFill>
            {/* Background */}
            <Img
                src={bg}
                style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'blur(3px)', // Slight blur to focus on character
                }}
            />

            {/* Character (Centered/Solo) */}
            <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
                <Img
                    src={charImg}
                    style={{
                        height: '90%', // Large portrait
                        width: 'auto',
                        opacity: charOpacity,
                        transform: `translateY(${charTranslateY}px)`,
                        marginBottom: -50 // Anchor to bottom
                    }}
                />
            </AbsoluteFill>

            {/* Message Box */}
            <div style={{
                position: 'absolute',
                bottom: 50,
                left: '5%',
                right: '5%',
                minHeight: 250,
                backgroundColor: 'rgba(255, 255, 255, 0.95)', // White box for cleaner look against blur
                borderRadius: 20,
                boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
                padding: 40,
                display: 'flex',
                flexDirection: 'column',
                borderLeft: `15px solid ${character === 'Ai' ? '#4dabf7' : '#ff8787'}`
            }}>
                <div style={{
                    fontFamily: FONT_FAMILY,
                    fontSize: 45,
                    fontWeight: 'bold',
                    color: '#333',
                    marginBottom: 15,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 15
                }}>
                    <span style={{
                        backgroundColor: character === 'Ai' ? '#4dabf7' : '#ff8787',
                        color: 'white',
                        padding: '5px 15px',
                        borderRadius: 10,
                        fontSize: 30
                    }}>
                        {character === 'Ai' ? 'TEACHER' : 'STUDENT'}
                    </span>
                    {character === 'Ai' ? 'Ai 先生' : 'Mai'}
                </div>
                <div style={{
                    fontFamily: FONT_FAMILY,
                    fontSize: 55,
                    color: '#222',
                    lineHeight: 1.4,
                    fontWeight: 500
                }}>
                    {text}
                </div>
            </div>
        </AbsoluteFill>
    );
};

export const NewsVideo: React.FC = () => {
    const { fps } = useVideoConfig(); // Fixed duration logic assumed in Root
    // We reuse the data logic. ideally we pass duration as prop or calc here.
    const DURATION_PER_LINE = 6 * 30;

    return (
        <AbsoluteFill style={{ backgroundColor: '#000' }}>
            {dialogueData.map((item, index) => {
                const startFrame = index * DURATION_PER_LINE;

                // Fallback bg logic: use current item's or previous known non-null logic (simplified here)
                const bg = item.background || staticFile('agentic_ai.png');

                return (
                    <Sequence key={item.id} from={startFrame} durationInFrames={DURATION_PER_LINE}>
                        <SoloScene
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
