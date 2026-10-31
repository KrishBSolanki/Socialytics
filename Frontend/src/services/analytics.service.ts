import type { Campaign, OverviewSummary, SocialPost, TimePoint } from "@/types";
import { apiGet, isApiMode } from "./api/client";
import { ENDPOINTS } from "./api/config";
import { loadComments, loadPosts } from "./dataset.service";
import {
  buildCampaigns,
  buildOverview,
  buildTimeline,
  campaignIdOf,
  inRange,
  type Granularity,
} from "@/utils/aggregate";
import { slugify } from "@/utils/format";

export interface RangeQuery {
  from?: string;
  to?: string;
  granularity?: Granularity;
  brandId?: string;
  campaignId?: string;
}

async function scoped(q: RangeQuery) {
  const [posts, comments] = await Promise.all([loadPosts(), loadComments()]);
  const ps = posts.filter(
    (p) =>
      inRange(p.ts, q.from, q.to) &&
      (!q.brandId || q.brandId === "all" || p.brandId === q.brandId) &&
      (!q.campaignId || q.campaignId === "all" || campaignIdOf(p) === q.campaignId),
  );
  const ids = new Set(ps.map((p) => p.id));
  const cs = comments.filter((c) => ids.has(c.parentId) && inRange(c.ts, q.from, q.to));
  return { posts: ps, comments: cs };
}

export interface Breakdown {
  name: string;
  posts: number;
  likes: number;
  retweets: number;
  comments: number;
  avgEngagement: number;
}

function breakdown(posts: SocialPost[], key: (p: SocialPost) => string): Breakdown[] {
  const m = new Map<string, Breakdown>();
  for (const p of posts) {
    const k = key(p);
    const b = m.get(k) ?? { name: k, posts: 0, likes: 0, retweets: 0, comments: 0, avgEngagement: 0 };
    b.posts++;
    b.likes += p.likes;
    b.retweets += p.retweets;
    b.comments += p.comments;
    m.set(k, b);
  }
  return [...m.values()]
    .map((b) => ({ ...b, avgEngagement: (b.likes + b.retweets + b.comments) / b.posts }))
    .sort((a, b) => b.posts - a.posts);
}

export const analyticsService = {
  async overview(q: RangeQuery = {}, signal?: AbortSignal): Promise<OverviewSummary> {
    if (isApiMode()) return apiGet<OverviewSummary>(ENDPOINTS.overview, { ...q }, signal);
    return buildOverview((await scoped(q)).posts);
  },

  async timeline(q: RangeQuery = {}, signal?: AbortSignal): Promise<TimePoint[]> {
    if (isApiMode()) return apiGet<TimePoint[]>(ENDPOINTS.timeline, { ...q }, signal);
    const { posts, comments } = await scoped(q);
    return buildTimeline(posts, comments, q.granularity ?? "week");
  },

  async campaigns(q: RangeQuery = {}, signal?: AbortSignal): Promise<Campaign[]> {
    if (isApiMode()) return apiGet<Campaign[]>(ENDPOINTS.campaigns, { ...q }, signal);
    return buildCampaigns((await scoped(q)).posts);
  },

  async campaignTimelines(ids: string[], granularity: Granularity, signal?: AbortSignal) {
    if (isApiMode())
      return apiGet<Record<string, TimePoint[]>>(`${ENDPOINTS.campaigns}/timelines`, { ids: ids.join(","), granularity }, signal);
    const out: Record<string, TimePoint[]> = {};
    for (const id of ids) {
      const { posts, comments } = await scoped({ campaignId: id });
      out[id] = buildTimeline(posts, comments, granularity);
    }
    return out;
  },

  /** Engagement & activity breakdowns used by Audience Insights. */
  async audience(q: RangeQuery = {}, signal?: AbortSignal) {
    if (isApiMode()) return apiGet<AudienceInsights>(`${ENDPOINTS.overview}/audience`, { ...q }, signal);
    const { posts, comments } = await scoped(q);
    const hourly = Array.from({ length: 24 }, (_, h) => ({ hour: h, comments: 0, posts: 0 }));
    const weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => ({ day: d, comments: 0, posts: 0 }));
    for (const c of comments) {
      const d = new Date(c.ts);
      hourly[d.getUTCHours()]!.comments++;
      weekday[(d.getUTCDay() + 6) % 7]!.comments++;
    }
    for (const p of posts) {
      const d = new Date(p.ts);
      hourly[d.getUTCHours()]!.posts++;
      weekday[(d.getUTCDay() + 6) % 7]!.posts++;
    }
    const media = breakdown(posts, (p) => (p.video ? "Video" : p.image ? "Image" : "Text only"));
    const format = breakdown(posts, (p) => (p.isRetweet ? "Repost" : p.isReply ? "Reply" : "Original post"));
    return {
      hourly,
      weekday,
      byPeriod: breakdown(posts, (p) => p.period),
      byPostType: breakdown(posts, (p) => p.postType),
      byRelief: breakdown(posts, (p) => p.reliefEffect),
      byIndustry: breakdown(posts, (p) => p.industry),
      byNationality: breakdown(posts, (p) => (p.nationality === "local" ? "Local brands" : "Global brands")),
      byMedia: media,
      byFormat: format,
      hashtagUse: breakdown(posts, (p) => (p.tags === 0 ? "0 hashtags" : p.tags === 1 ? "1 hashtag" : "2+ hashtags")),
      totalComments: comments.length,
    } satisfies AudienceInsights;
  },
};

export interface AudienceInsights {
  hourly: { hour: number; comments: number; posts: number }[];
  weekday: { day: string; comments: number; posts: number }[];
  byPeriod: Breakdown[];
  byPostType: Breakdown[];
  byRelief: Breakdown[];
  byIndustry: Breakdown[];
  byNationality: Breakdown[];
  byMedia: Breakdown[];
  byFormat: Breakdown[];
  hashtagUse: Breakdown[];
  totalComments: number;
}

export { slugify };
