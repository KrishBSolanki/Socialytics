/** Centralised API configuration. Override with VITE_API_BASE_URL. */
export const API_CONFIG = {
  baseUrl: (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8000/api/v1",
  timeoutMs: 15_000,
  retries: 2,
} as const;

/** Endpoints the future Python backend is expected to expose. */
export const ENDPOINTS = {
  health: "/health",
  meta: "/dataset/meta",
  overview: "/analytics/overview",
  timeline: "/analytics/timeline",
  posts: "/posts",
  post: (id: string) => `/posts/${id}`,
  postComments: (id: string) => `/posts/${id}/comments`,
  comments: "/comments",
  brands: "/brands",
  brand: (id: string) => `/brands/${id}`,
  campaigns: "/campaigns",
  sentiment: "/analytics/sentiment",
  emotions: "/analytics/emotions",
  engagement: "/analytics/engagement",
  topics: "/analytics/topics",
  forecast: "/forecast",
  predictSingle: "/analyze/sentiment",
  predictBulk: "/analyze/bulk",
  modelEvaluation: "/models/evaluation",
  history: "/predictions/history",
} as const;
