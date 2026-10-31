/**
 * TanStack Query hooks over the service layer. The data-source mode is part
 * of every query key so switching between the dataset snapshot and the live
 * backend refetches everything. Queries run client-side only (the snapshot is
 * a static file and the backend URL is a browser setting).
 */
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/store/app-store";
import { analyticsService, type RangeQuery } from "@/services/analytics.service";
import { brandService } from "@/services/brand.service";
import { datasetService } from "@/services/dataset.service";
import { forecastService } from "@/services/forecast.service";
import { postService } from "@/services/post.service";
import { sentimentService } from "@/services/sentiment.service";
import type { Emotion, Polarity, PostQuery } from "@/types";
import type { Granularity } from "@/utils/aggregate";

const useMode = () => {
  const mode = useAppStore((s) => s.dataSource);
  const base = useAppStore((s) => s.apiBaseUrl);
  return mode === "api" ? `api:${base}` : "dataset";
};

const common = { staleTime: 5 * 60_000, retry: 1 } as const;

export function useDatasetMeta() {
  const m = useMode();
  return useQuery({ queryKey: [m, "meta"], queryFn: ({ signal }) => datasetService.getMeta(signal), ...common });
}

export function useRawPosts() {
  const m = useMode();
  return useQuery({ queryKey: [m, "raw-posts"], queryFn: ({ signal }) => datasetService.getRawPosts(signal), ...common });
}

export function useRawComments(enabled = true) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "raw-comments"],
    queryFn: ({ signal }) => datasetService.getRawComments(signal),
    enabled,
    ...common,
  });
}

export function useOverview(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({ queryKey: [m, "overview", q], queryFn: ({ signal }) => analyticsService.overview(q, signal), ...common });
}

export function useTimeline(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "timeline", q],
    queryFn: ({ signal }) => analyticsService.timeline(q, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function useCampaigns(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({ queryKey: [m, "campaigns", q], queryFn: ({ signal }) => analyticsService.campaigns(q, signal), ...common });
}

export function useCampaignTimelines(ids: string[], granularity: Granularity) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "campaign-timelines", ids, granularity],
    queryFn: ({ signal }) => analyticsService.campaignTimelines(ids, granularity, signal),
    enabled: ids.length > 0,
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function useAudience(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({ queryKey: [m, "audience", q], queryFn: ({ signal }) => analyticsService.audience(q, signal), ...common });
}

export function useBrands() {
  const m = useMode();
  return useQuery({ queryKey: [m, "brands"], queryFn: ({ signal }) => brandService.list(signal), ...common });
}

export function useBrandProfile(id: string, granularity: Granularity) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "brand", id, granularity],
    queryFn: ({ signal }) => brandService.profile(id, granularity, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function usePosts(q: PostQuery) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "posts", q],
    queryFn: ({ signal }) => postService.list(q, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function usePostComments(id: string, enabled: boolean) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "post-comments", id],
    queryFn: ({ signal }) => postService.comments(id, signal),
    enabled,
    ...common,
  });
}

export function useRecentPosts(limit: number) {
  const m = useMode();
  return useQuery({ queryKey: [m, "recent-posts", limit], queryFn: ({ signal }) => postService.recent(limit, signal), ...common });
}

export function useRecentComments(limit: number) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "recent-comments", limit],
    queryFn: ({ signal }) => postService.recentComments(limit, signal),
    ...common,
  });
}

export function useSentimentSummary(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "sentiment", q],
    queryFn: ({ signal }) => sentimentService.summary(q, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function useEmotionByBrand(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({ queryKey: [m, "emo-brand", q], queryFn: ({ signal }) => sentimentService.byBrand(q, signal), ...common });
}

export function useEmotionByCampaign(q: RangeQuery = {}) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "emo-campaign", q],
    queryFn: ({ signal }) => sentimentService.byCampaign(q, signal),
    ...common,
  });
}

export function useEmotionTimeline(q: RangeQuery & { granularity: Granularity }) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "emo-timeline", q],
    queryFn: ({ signal }) => sentimentService.emotionTimeline(q, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function useLabelledComments(
  q: RangeQuery & { emotion?: Emotion | "all"; polarity?: Polarity | "all"; page: number; pageSize: number },
) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "labelled-comments", q],
    queryFn: ({ signal }) => sentimentService.comments(q, signal),
    placeholderData: keepPreviousData,
    ...common,
  });
}

export function useForecast(q: { brandId?: string; horizonDays: number }) {
  const m = useMode();
  return useQuery({
    queryKey: [m, "forecast", q],
    queryFn: ({ signal }) => forecastService.get(q, signal),
    ...common,
    retry: 0,
  });
}

export function useBackendHealth(enabled: boolean) {
  const base = useAppStore((s) => s.apiBaseUrl);
  return useQuery({
    queryKey: ["health", base],
    queryFn: ({ signal }) => datasetService.health(signal),
    enabled,
    retry: 0,
    refetchInterval: 60_000,
  });
}
