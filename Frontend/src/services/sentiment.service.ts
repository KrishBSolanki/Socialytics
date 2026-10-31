import type { Comment, Emotion, EmotionCounts, EmotionResult, Polarity, SentimentResult } from "@/types";
import { EMOTIONS } from "@/types";
import { apiGet, apiPost, apiPostForm, isApiMode } from "./api/client";
import { API_CONFIG, ENDPOINTS } from "./api/config";
import { useAppStore } from "@/store/app-store";
import { loadComments, loadPosts } from "./dataset.service";
import { campaignIdOf, inRange, type Granularity, bucketKey } from "@/utils/aggregate";
import { EMOTION_TO_POLARITY, emotionsToPolarity, emptyEmotions, sumCounts } from "@/utils/emotion";
import type { RangeQuery } from "./analytics.service";

export interface GroupEmotion {
  id: string;
  name: string;
  counts: EmotionCounts;
  total: number;
}

export interface LabelledComment extends Comment {
  brand: string;
  brandId: string;
  campaign: string;
}

async function scopedComments(q: RangeQuery): Promise<LabelledComment[]> {
  const [posts, comments] = await Promise.all([loadPosts(), loadComments()]);
  const byId = new Map(posts.map((p) => [p.id, p]));
  const out: LabelledComment[] = [];
  for (const c of comments) {
    const p = byId.get(c.parentId);
    if (!p) continue;
    if (!inRange(c.ts, q.from, q.to)) continue;
    if (q.brandId && q.brandId !== "all" && p.brandId !== q.brandId) continue;
    if (q.campaignId && q.campaignId !== "all" && campaignIdOf(p) !== q.campaignId) continue;
    out.push({ ...c, brand: p.brand, brandId: p.brandId, campaign: p.aidAction ?? "Regular communication" });
  }
  return out;
}

function group(comments: LabelledComment[], key: (c: LabelledComment) => [string, string]): GroupEmotion[] {
  const m = new Map<string, GroupEmotion>();
  for (const c of comments) {
    const [id, name] = key(c);
    const g = m.get(id) ?? { id, name, counts: emptyEmotions(), total: 0 };
    g.counts[c.emotion]++;
    g.total++;
    m.set(id, g);
  }
  return [...m.values()].sort((a, b) => b.total - a.total);
}

export const sentimentService = {
  async summary(q: RangeQuery = {}, signal?: AbortSignal): Promise<SentimentResult & { emotions: EmotionResult }> {
    if (isApiMode()) return apiGet(ENDPOINTS.sentiment, { ...q }, signal);
    const cs = await scopedComments(q);
    const counts = emptyEmotions();
    for (const c of cs) counts[c.emotion]++;
    return {
      polarity: emotionsToPolarity(counts),
      total: cs.length,
      method: "emotion-derived",
      emotions: { counts, total: sumCounts(counts) },
    };
  },

  async byBrand(q: RangeQuery = {}, signal?: AbortSignal): Promise<GroupEmotion[]> {
    if (isApiMode()) return apiGet(`${ENDPOINTS.emotions}/by-brand`, { ...q }, signal);
    return group(await scopedComments(q), (c) => [c.brandId, c.brand]);
  },

  async byCampaign(q: RangeQuery = {}, signal?: AbortSignal): Promise<GroupEmotion[]> {
    if (isApiMode()) return apiGet(`${ENDPOINTS.emotions}/by-campaign`, { ...q }, signal);
    return group(await scopedComments(q), (c) => [c.campaign, c.campaign]);
  },

  async emotionTimeline(q: RangeQuery & { granularity: Granularity }, signal?: AbortSignal) {
    if (isApiMode()) return apiGet<({ date: string } & EmotionCounts)[]>(`${ENDPOINTS.emotions}/timeline`, { ...q }, signal);
    const m = new Map<string, { date: string } & EmotionCounts>();
    for (const c of await scopedComments(q)) {
      const k = bucketKey(c.ts, q.granularity);
      const row = m.get(k) ?? { date: k, ...emptyEmotions() };
      row[c.emotion]++;
      m.set(k, row);
    }
    return [...m.values()].sort((a, b) => a.date.localeCompare(b.date));
  },

  /** Comment-level exploration, newest first. */
  async comments(
    q: RangeQuery & { emotion?: Emotion | "all"; polarity?: Polarity | "all"; page: number; pageSize: number },
    signal?: AbortSignal,
  ) {
    if (isApiMode()) return apiGet<{ items: LabelledComment[]; total: number }>(ENDPOINTS.comments, { ...q }, signal);
    const all = (await scopedComments(q))
      .filter((c) => !q.emotion || q.emotion === "all" || c.emotion === q.emotion)
      .filter((c) => !q.polarity || q.polarity === "all" || EMOTION_TO_POLARITY[c.emotion] === q.polarity)
      .sort((a, b) => b.ts.localeCompare(a.ts));
    return { items: all.slice((q.page - 1) * q.pageSize, q.page * q.pageSize), total: all.length };
  },

  /** Compare two periods: share of each polarity in A vs B. */
  async compare(a: RangeQuery, b: RangeQuery, signal?: AbortSignal) {
    const [ra, rb] = await Promise.all([sentimentService.summary(a, signal), sentimentService.summary(b, signal)]);
    return { a: ra, b: rb };
  },

  /** Real-time single text classification via the Python ML Backend. */
  async predictSingle(text: string, category = "General", signal?: AbortSignal) {
    return apiPost<{
      id: number;
      raw_text: string;
      clean_text: string;
      sentiment: string;
      confidence: number;
      probabilities: Record<string, number>;
      warning: string | null;
      timestamp: string;
    }>(ENDPOINTS.predictSingle, { text, category }, signal);
  },

  /** Bulk CSV analysis via Python ML Pipeline. */
  async predictBulk(file: File, signal?: AbortSignal) {
    const form = new FormData();
    form.append("file", file);
    return apiPostForm<any>(ENDPOINTS.predictBulk, form, signal);
  },

  /** Fetch genuine model evaluation metadata and confusion matrix from Python. */
  async getModelEvaluation(signal?: AbortSignal) {
    return apiGet<any>(ENDPOINTS.modelEvaluation, undefined, signal);
  },

  /** Fetch SQLite prediction history. */
  async getHistory(limit = 100, signal?: AbortSignal) {
    return apiGet<{ stats: any; total: number; records: any[] }>(ENDPOINTS.history, { limit }, signal);
  },

  /** Clear prediction history. */
  async clearHistory(signal?: AbortSignal) {
    const base = useAppStore.getState().apiBaseUrl || API_CONFIG.baseUrl;
    const res = await fetch(`${base.replace(/\/$/, "")}${ENDPOINTS.history}`, {
      method: "DELETE",
      signal,
    });
    return res.json();
  },
};

export { EMOTIONS };
