import "./index.css";
import { Composition } from 'remotion';
import { NewsVideo } from './NewsVideo';
import { ShortVideo } from './ShortVideo';
import { dialogueData } from './data/news-data';

export const RemotionRoot: React.FC = () => {
  const NEWS_DURATION = dialogueData.length * 6 * 30; // 6 sec per line
  const SHORT_DURATION = dialogueData.length * 5 * 30; // 5 sec per line

  return (
    <>
      <Composition
        id="NewsVideo"
        component={NewsVideo}
        durationInFrames={NEWS_DURATION}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ShortVideo"
        component={ShortVideo}
        durationInFrames={SHORT_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
