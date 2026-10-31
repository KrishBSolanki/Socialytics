/**
 * Domain types for SOCIALPULSE. Field names mirror the Zenodo CSR Brand Posts
 * dataset (record 22042887) so a Python backend can return the same shapes.
 */

export const EMOTIONS = ["happy", "anger", "sad", "fear", "surprise", "disgust", "neutral"] as const;
export type Emotion = (typeof EMOTIONS)[number];
export type EmotionCounts = Record<Emotion, number>;

export const POLARITIES = ["positive", "neutral", "negative"] as const;
export type Polarity = (typeof POLARITIES)[number];
export type PolarityCounts = Record<Polarity, number>;

export type Nationality = "local" | "international";
export type DisasterPeriod = "Before" | "Emergency Relief" | "Early Recovery";
export type PostType = "Informational" | "Transformational" | "Interactional";
export type ReliefEffect = "No Aid" | "Short Term Aid" | "Long Term Aid";

export interface EngagementMetrics {
  likes: number;
  retweets: number;
  comments: number;
  total: number;
  /** Engagements per 1,000 followers. */
  ratePerThousand: number;
}

/** A brand post on Platform X. The dataset does not include post text. */
export interface SocialPost {
  id: string;
  ts: string;
  brand: string;
  brandId: string;
  nationality: Nationality;
  industry: string;
  followers: number;
  isReply: boolean;
  isRetweet: boolean;
  image: boolean;
  video: boolean;
  postType: PostType;
  aidAction: string | null;
  reliefEffect: ReliefEffect;
  comments: number;
  retweets: number;
  likes: number;
  tags: number;
  mentions: number;
  emojis: number;
  urls: number;
  period: DisasterPeriod;
  /** Counts of NLP-predicted emotions among sampled comments, or null if none were sampled. */
  emotions: EmotionCounts | null;
  sampledComments: number | null;
  /** Optional text — only present if a backend supplies it. Never translated. */
  text?: string;
  language?: string;
}

/** A sampled audience comment. The dataset provides no comment text. */
export interface Comment {
  id: string;
  ts: string;
  parentId: string;
  emotion: Emotion;
  text?: string;
  language?: string;
}

export interface Brand {
  id: string;
  name: string;
  nationality: Nationality;
  industry: string;
  followers: number;
  postCount: number;
  firstPost: string;
  lastPost: string;
  engagement: EngagementMetrics;
  emotions: EmotionCounts;
  polarity: PolarityCounts;
  /** Share of positive minus share of negative among emotion-labelled comments, -1..1. */
  perceptionIndex: number | null;
  csrPostCount: number;
}

/** Campaigns are the dataset's coded CSR / disaster-aid action types. */
export interface Campaign {
  id: string;
  name: string;
  description: string;
  postCount: number;
  brandCount: number;
  engagement: EngagementMetrics;
  emotions: EmotionCounts;
  polarity: PolarityCounts;
  firstPost: string | null;
  lastPost: string | null;
}

export interface SentimentResult {
  polarity: PolarityCounts;
  total: number;
  /** "emotion-derived" = heuristic mapping of emotion labels; "model" = backend sentiment model. */
  method: "emotion-derived" | "model";
}

export interface EmotionResult {
  counts: EmotionCounts;
  total: number;
}

export interface TimePoint {
  date: string;
  posts: number;
  likes: number;
  retweets: number;
  comments: number;
  labelledComments: number;
  positive: number;
  negative: number;
  neutral: number;
}

export interface ForecastPoint {
  date: string;
  predicted: number;
  lower: number;
  upper: number;
}

export interface ForecastResult {
  brandId: string | null;
  horizonDays: number;
  metric: "perception_index";
  points: ForecastPoint[];
  model: { name: string; mae?: number; rmse?: number; mape?: number; trainedAt?: string } | null;
}

export interface OverviewSummary {
  brands: number;
  posts: number;
  commentsReported: number;
  commentsLabelled: number;
  avgEngagement: number;
  positiveShare: number;
  negativeShare: number;
  emotions: EmotionCounts;
  polarity: PolarityCounts;
}

export interface Paginated<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface PostQuery {
  search?: string;
  brandId?: string;
  polarity?: Polarity | "all";
  campaign?: string;
  sort?: "newest" | "oldest" | "engagement";
  page?: number;
  pageSize?: number;
}

export interface DatasetColumn {
  name: string;
  missing: number;
  dtype: string;
}
export interface DatasetMeta {
  title: string;
  doi: string;
  url: string;
  license: string;
  authors: string[];
  publisher: string;
  platform: string;
  coverage: { start: string; end: string };
  eventDate: string;
  files: { name: string; rows: number; columns: DatasetColumn[] }[];
}

export type DataSourceMode = "dataset" | "api";

export interface SinglePrediction {
  id?: number;
  raw_text: string;
  clean_text: string;
  sentiment: string;
  confidence: number;
  probabilities: Record<string, number>;
  warning?: string | null;
  timestamp: string;
}

export interface BulkPredictionResponse {
  filename: string;
  totalRecords: number;
  sentimentCounts: Record<string, number>;
  positivePercentage: number;
  negativePercentage: number;
  neutralPercentage: number;
  results: {
    raw_text: string;
    clean_text: string;
    sentiment: string;
    confidence: number;
    probabilities: Record<string, number>;
  }[];
}

export interface ModelEvaluationData {
  modelType: string;
  pipelineSteps: string[];
  trainingSamples: number;
  testSamples: number;
  classes: string[];
  timestamp?: string;
  naiveBayes: {
    accuracy: number;
    precisionMacro: number;
    recallMacro: number;
    f1Macro: number;
    precisionWeighted?: number;
    recallWeighted?: number;
    f1Weighted?: number;
    confusionMatrix?: number[][];
    labels?: string[];
    classificationReport?: Record<string, any>;
  };
  logisticRegression?: {
    accuracy: number;
    precisionMacro: number;
    recallMacro: number;
    f1Macro: number;
  };
  crossValidation?: {
    mean: number;
    std: number;
    folds: number;
  };
}

export interface HistoryRecord {
  id: number;
  raw_text: string;
  clean_text?: string;
  predicted_sentiment: string;
  prob_positive?: number;
  prob_negative?: number;
  prob_neutral?: number;
  confidence: number;
  source: string;
  created_at: string;
}

export interface TopicItem {
  topic: string;
  mentions: number;
  sentiment: string;
  polarityScore: number;
}
