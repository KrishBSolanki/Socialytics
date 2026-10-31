import type { Comment, Paginated, PostQuery, SocialPost } from "@/types";
import { apiGet, isApiMode } from "./api/client";
import { ENDPOINTS } from "./api/config";
import { loadComments, loadPosts } from "./dataset.service";
import { campaignIdOf, engagementOf } from "@/utils/aggregate";
import { dominantPolarity, emotionsToPolarity } from "@/utils/emotion";

export function filterPosts(posts: SocialPost[], q: PostQuery): SocialPost[] {
  const s = q.search?.trim().toLocaleLowerCase("tr");
  let out = posts.filter((p) => {
    if (q.brandId && q.brandId !== "all" && p.brandId !== q.brandId) return false;
    if (q.campaign && q.campaign !== "all" && campaignIdOf(p) !== q.campaign) return false;
    if (q.polarity && q.polarity !== "all") {
      if (!p.emotions) return false;
      if (dominantPolarity(emotionsToPolarity(p.emotions)) !== q.polarity) return false;
    }
    if (s) {
      const hay = `${p.brand} ${p.industry} ${p.postType} ${p.aidAction ?? ""} ${p.reliefEffect} ${p.period} ${p.id} ${p.text ?? ""}`.toLocaleLowerCase("tr");
      if (!hay.includes(s)) return false;
    }
    return true;
  });
  const sort = q.sort ?? "newest";
  out = [...out].sort((a, b) =>
    sort === "engagement"
      ? engagementOf(b) - engagementOf(a)
      : sort === "oldest"
        ? a.ts.localeCompare(b.ts)
        : b.ts.localeCompare(a.ts),
  );
  return out;
}

export const postService = {
  async list(q: PostQuery, signal?: AbortSignal): Promise<Paginated<SocialPost>> {
    const page = q.page ?? 1;
    const pageSize = q.pageSize ?? 12;
    if (isApiMode()) return apiGet<Paginated<SocialPost>>(ENDPOINTS.posts, { ...q, page, pageSize }, signal);
    const all = filterPosts(await loadPosts(), q);
    return { items: all.slice((page - 1) * pageSize, page * pageSize), total: all.length, page, pageSize };
  },

  async get(id: string, signal?: AbortSignal): Promise<SocialPost | null> {
    if (isApiMode()) return apiGet<SocialPost>(ENDPOINTS.post(id), undefined, signal);
    return (await loadPosts()).find((p) => p.id === id) ?? null;
  },

  async comments(postId: string, signal?: AbortSignal): Promise<Comment[]> {
    if (isApiMode()) return apiGet<Comment[]>(ENDPOINTS.postComments(postId), undefined, signal);
    return (await loadComments())
      .filter((c) => c.parentId === postId)
      .sort((a, b) => b.ts.localeCompare(a.ts));
  },

  async recent(limit: number, signal?: AbortSignal): Promise<SocialPost[]> {
    return (await postService.list({ sort: "newest", page: 1, pageSize: limit }, signal)).items;
  },

  async recentComments(limit: number, signal?: AbortSignal): Promise<(Comment & { brand: string; brandId: string })[]> {
    if (isApiMode()) return apiGet(ENDPOINTS.comments, { sort: "newest", limit, withBrand: true }, signal);
    const [comments, posts] = await Promise.all([loadComments(), loadPosts()]);
    const byId = new Map(posts.map((p) => [p.id, p]));
    return [...comments]
      .sort((a, b) => b.ts.localeCompare(a.ts))
      .slice(0, limit)
      .map((c) => ({ ...c, brand: byId.get(c.parentId)?.brand ?? "Unknown", brandId: byId.get(c.parentId)?.brandId ?? "" }));
  },
};
