import { EMOTIONS, type Emotion, type EmotionCounts, type Polarity, type PolarityCounts } from "@/types";

export const EMOTION_META: Record<Emotion, { label: string; color: string; emoji: string }> = {
  happy: { label: "Happy", color: "var(--emo-happy)", emoji: "😊" },
  anger: { label: "Anger", color: "var(--emo-anger)", emoji: "😠" },
  sad: { label: "Sad", color: "var(--emo-sad)", emoji: "😢" },
  fear: { label: "Fear", color: "var(--emo-fear)", emoji: "😨" },
  surprise: { label: "Surprise", color: "var(--emo-surprise)", emoji: "😮" },
  disgust: { label: "Disgust", color: "var(--emo-disgust)", emoji: "🤢" },
  neutral: { label: "Neutral", color: "var(--emo-neutral)", emoji: "😐" },
};

export const POLARITY_META: Record<Polarity, { label: string; color: string }> = {
  positive: { label: "Positive", color: "var(--positive)" },
  neutral: { label: "Neutral", color: "var(--neutral-tone)" },
  negative: { label: "Negative", color: "var(--negative)" },
};

/**
 * Heuristic mapping from the dataset's predicted emotion labels to polarity.
 * This is NOT a sentiment model — it is shown in the UI as "emotion-derived".
 */
export const EMOTION_TO_POLARITY: Record<Emotion, Polarity> = {
  happy: "positive",
  anger: "negative",
  sad: "negative",
  fear: "negative",
  disgust: "negative",
  surprise: "neutral",
  neutral: "neutral",
};

export const emptyEmotions = (): EmotionCounts =>
  Object.fromEntries(EMOTIONS.map((e) => [e, 0])) as EmotionCounts;

export const emptyPolarity = (): PolarityCounts => ({ positive: 0, neutral: 0, negative: 0 });

export function addEmotions(target: EmotionCounts, src: EmotionCounts | null | undefined) {
  if (!src) return target;
  for (const e of EMOTIONS) target[e] += src[e] ?? 0;
  return target;
}

export function emotionsToPolarity(counts: EmotionCounts): PolarityCounts {
  const p = emptyPolarity();
  for (const e of EMOTIONS) p[EMOTION_TO_POLARITY[e]] += counts[e];
  return p;
}

export const sumCounts = (c: Record<string, number>) => Object.values(c).reduce((a, b) => a + b, 0);

/** (positive − negative) / total, or null when nothing is labelled. */
export function perceptionIndex(p: PolarityCounts): number | null {
  const t = p.positive + p.neutral + p.negative;
  return t === 0 ? null : (p.positive - p.negative) / t;
}

export function dominantPolarity(p: PolarityCounts): Polarity | null {
  const t = sumCounts(p);
  if (!t) return null;
  return (Object.entries(p) as [Polarity, number][]).sort((a, b) => b[1] - a[1])[0][0];
}

export function topEmotions(c: EmotionCounts, n = 3): Emotion[] {
  return (Object.entries(c) as [Emotion, number][])
    .filter(([, v]) => v > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([e]) => e);
}
