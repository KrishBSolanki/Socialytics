/**
 * Pure aggregation over the dataset snapshot. The backend is expected to
 * return the same shapes; these functions are what "dataset mode" uses.
 */
import type {
  Brand,
  Campaign,
  Comment,
  EmotionCounts,
  EngagementMetrics,
  OverviewSummary,
  SocialPost,
  TimePoint,
} from "@/types";
import {
  EMOTION_TO_POLARITY,
  addEmotions,
  emotionsToPolarity,
  emptyEmotions,
  perceptionIndex,
  sumCounts,
} from "./emotion";
import { slugify } from "./format";

export const REGULAR_CAMPAIGN = "regular-communication";

export const CAMPAIGN_DESCRIPTIONS: Record<string, string> = {
  "Corporate Giving": "Donations and financial or in-kind contributions announced by the brand.",
  Sympathy: "Messages of condolence and solidarity with those affected.",
  "Third Party Involvement": "Aid delivered together with NGOs, agencies or partners.",
  "Employee Involvement": "Relief driven by the brand's employees and volunteers.",
  "Information Delivery": "Practical information shared to help people affected.",
  "Technical Support": "Infrastructure, connectivity or technical help provided.",
  Others: "Other coded disaster-aid communication.",
  [REGULAR_CAMPAIGN]: "Posts with no coded disaster-aid action (everyday brand communication).",
};

export const engagementOf = (p: Pick<SocialPost, "likes" | "retweets" | "comments">) =>
  p.likes + p.retweets + p.comments;

export function engagementMetrics(posts: SocialPost[], followers?: number): EngagementMetrics {
  let likes = 0,
    retweets = 0,
    comments = 0,
    rateSum = 0;
  for (const p of posts) {
    likes += p.likes;
    retweets += p.retweets;
    comments += p.comments;
    rateSum += p.followers ? (engagementOf(p) / p.followers) * 1000 : 0;
  }
  const total = likes + retweets + comments;
  const ratePerThousand = followers
    ? posts.length
      ? total / posts.length / (followers / 1000)
      : 0
    : posts.length
      ? rateSum / posts.length
      : 0;
  return { likes, retweets, comments, total, ratePerThousand };
}

export function emotionTotals(posts: SocialPost[]): EmotionCounts {
  const c = emptyEmotions();
  for (const p of posts) addEmotions(c, p.emotions);
  return c;
}

export const campaignIdOf = (p: SocialPost) => (p.aidAction ? slugify(p.aidAction) : REGULAR_CAMPAIGN);

export function buildBrands(posts: SocialPost[]): Brand[] {
  const groups = new Map<string, SocialPost[]>();
  for (const p of posts) {
    const g = groups.get(p.brandId);
    if (g) g.push(p);
    else groups.set(p.brandId, [p]);
  }
  return [...groups.entries()].map(([id, list]) => {
    const sorted = [...list].sort((a, b) => a.ts.localeCompare(b.ts));
    const first = sorted[0]!;
    const followers = Math.max(...list.map((p) => p.followers));
    const emotions = emotionTotals(list);
    const polarity = emotionsToPolarity(emotions);
    return {
      id,
      name: first.brand,
      nationality: first.nationality,
      industry: first.industry,
      followers,
      postCount: list.length,
      firstPost: first.ts,
      lastPost: sorted[sorted.length - 1]!.ts,
      engagement: engagementMetrics(list, followers),
      emotions,
      polarity,
      perceptionIndex: perceptionIndex(polarity),
      csrPostCount: list.filter((p) => p.aidAction).length,
    };
  });
}

export function buildCampaigns(posts: SocialPost[]): Campaign[] {
  const groups = new Map<string, SocialPost[]>();
  for (const p of posts) {
    const id = campaignIdOf(p);
    const g = groups.get(id);
    if (g) g.push(p);
    else groups.set(id, [p]);
  }
  return [...groups.entries()]
    .map(([id, list]) => {
      const name = list[0]!.aidAction ?? "Regular communication";
      const emotions = emotionTotals(list);
      const ts = list.map((p) => p.ts).sort();
      return {
        id,
        name,
        description: CAMPAIGN_DESCRIPTIONS[list[0]!.aidAction ?? REGULAR_CAMPAIGN] ?? "",
        postCount: list.length,
        brandCount: new Set(list.map((p) => p.brandId)).size,
        engagement: engagementMetrics(list),
        emotions,
        polarity: emotionsToPolarity(emotions),
        firstPost: ts[0] ?? null,
        lastPost: ts[ts.length - 1] ?? null,
      };
    })
    .sort((a, b) => b.postCount - a.postCount);
}

export function buildOverview(posts: SocialPost[]): OverviewSummary {
  const emotions = emotionTotals(posts);
  const polarity = emotionsToPolarity(emotions);
  const labelled = sumCounts(emotions);
  const eng = engagementMetrics(posts);
  return {
    brands: new Set(posts.map((p) => p.brandId)).size,
    posts: posts.length,
    commentsReported: eng.comments,
    commentsLabelled: labelled,
    avgEngagement: posts.length ? eng.total / posts.length : 0,
    positiveShare: labelled ? polarity.positive / labelled : 0,
    negativeShare: labelled ? polarity.negative / labelled : 0,
    emotions,
    polarity,
  };
}

export type Granularity = "day" | "week";

export function bucketKey(iso: string, g: Granularity) {
  const d = new Date(iso);
  if (g === "week") {
    const day = (d.getUTCDay() + 6) % 7; // Monday start
    d.setUTCDate(d.getUTCDate() - day);
  }
  return d.toISOString().slice(0, 10);
}

/**
 * Timeline of posts/engagement (by post time) and emotion-derived polarity
 * (by comment time).
 */
export function buildTimeline(posts: SocialPost[], comments: Comment[], g: Granularity): TimePoint[] {
  const map = new Map<string, TimePoint>();
  const get = (k: string) => {
    let t = map.get(k);
    if (!t) {
      t = { date: k, posts: 0, likes: 0, retweets: 0, comments: 0, labelledComments: 0, positive: 0, negative: 0, neutral: 0 };
      map.set(k, t);
    }
    return t;
  };
  for (const p of posts) {
    const t = get(bucketKey(p.ts, g));
    t.posts++;
    t.likes += p.likes;
    t.retweets += p.retweets;
    t.comments += p.comments;
  }
  for (const c of comments) {
    const t = get(bucketKey(c.ts, g));
    t.labelledComments++;
    t[EMOTION_TO_POLARITY[c.emotion]]++;
  }
  return [...map.values()].sort((a, b) => a.date.localeCompare(b.date));
}

export function inRange(iso: string, from?: string, to?: string) {
  const d = iso.slice(0, 10);
  return (!from || d >= from) && (!to || d <= to);
}
