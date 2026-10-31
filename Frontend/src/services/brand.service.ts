import type { Brand, Campaign, Comment, SocialPost, TimePoint } from "@/types";
import { apiGet, isApiMode } from "./api/client";
import { ENDPOINTS } from "./api/config";
import { loadComments, loadPosts } from "./dataset.service";
import { buildBrands, buildCampaigns, buildTimeline, type Granularity } from "@/utils/aggregate";

export interface BrandProfile {
  brand: Brand;
  campaigns: Campaign[];
  timeline: TimePoint[];
  recentPosts: SocialPost[];
  comments: Comment[];
  postTypes: { name: string; count: number }[];
  hourly: { hour: number; posts: number; engagement: number }[];
}

let brandCache: Brand[] | null = null;

export const brandService = {
  async list(signal?: AbortSignal): Promise<Brand[]> {
    if (isApiMode()) return apiGet<Brand[]>(ENDPOINTS.brands, undefined, signal);
    brandCache ??= buildBrands(await loadPosts());
    return brandCache;
  },

  async profile(id: string, granularity: Granularity, signal?: AbortSignal): Promise<BrandProfile | null> {
    if (isApiMode()) return apiGet<BrandProfile>(ENDPOINTS.brand(id), { granularity }, signal);
    const [posts, comments] = await Promise.all([loadPosts(), loadComments()]);
    const list = posts.filter((p) => p.brandId === id);
    if (!list.length) return null;
    const ids = new Set(list.map((p) => p.id));
    const brandComments = comments.filter((c) => ids.has(c.parentId));
    const types = new Map<string, number>();
    for (const p of list) {
      types.set(p.postType, (types.get(p.postType) ?? 0) + 1);
      if (p.aidAction) types.set(p.aidAction, (types.get(p.aidAction) ?? 0) + 1);
      types.set(p.reliefEffect, (types.get(p.reliefEffect) ?? 0) + 1);
    }
    const hourly = Array.from({ length: 24 }, (_, hour) => ({ hour, posts: 0, engagement: 0 }));
    for (const p of list) {
      const h = new Date(p.ts).getUTCHours();
      hourly[h]!.posts++;
      hourly[h]!.engagement += p.likes + p.retweets + p.comments;
    }
    return {
      brand: buildBrands(list)[0]!,
      campaigns: buildCampaigns(list),
      timeline: buildTimeline(list, brandComments, granularity),
      recentPosts: [...list].sort((a, b) => b.ts.localeCompare(a.ts)).slice(0, 6),
      comments: [...brandComments].sort((a, b) => b.ts.localeCompare(a.ts)),
      postTypes: [...types.entries()].map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count),
      hourly,
    };
  },
};
