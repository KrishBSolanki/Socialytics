import React, { useEffect, useState } from "react";
import { SidebarNav, type NavTab } from "./SidebarNav";
import { CenterFeed } from "./CenterFeed";
import { RightBrandPanel } from "./RightBrandPanel";
import { OverviewView } from "./OverviewView";
import { SentimentView } from "./SentimentView";
import { ForecastingView } from "./ForecastingView";
import { ModelEvaluationView } from "./ModelEvaluationView";
import { BrandExplorerView } from "./BrandExplorerView";
import { CampaignView } from "./CampaignView";
import { EmotionView } from "./EmotionView";
import { AudienceView } from "./AudienceView";
import { DatasetExplorerView } from "./DatasetExplorerView";
import { HistoryView } from "./HistoryView";
import { SettingsView } from "./SettingsView";
import { loadComments, loadMeta, loadPosts } from "@/services/dataset.service";
import { brandService } from "@/services/brand.service";
import { analyticsService } from "@/services/analytics.service";
import { Loader2 } from "lucide-react";

export function SocialPulseShell() {
  const [activeTab, setActiveTab] = useState<NavTab>("feed");
  const [selectedBrand, setSelectedBrand] = useState<string>("apple");
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);

  // Loaded data
  const [posts, setPosts] = useState<any[]>([]);
  const [commentsByPostId, setCommentsByPostId] = useState<Record<string, any[]>>({});
  const [brands, setBrands] = useState<any[]>([]);
  const [meta, setMeta] = useState<any>(null);
  const [overview, setOverview] = useState<any>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    document.title = "SocialPulse - Social Media Sentiment & Brand Perception Intelligence";
  }, []);

  useEffect(() => {
    let active = true;

    async function initData() {
      try {
        const [loadedPosts, loadedComments, loadedMeta, loadedBrands, loadedOverview, loadedTimeline] =
          await Promise.all([
            loadPosts().catch(() => []),
            loadComments().catch(() => []),
            loadMeta().catch(() => ({})),
            brandService.list().catch(() => []),
            analyticsService.overview().catch(() => null),
            analyticsService.timeline({ granularity: "day" }).catch(() => []),
          ]);

        if (!active) return;

        setPosts(loadedPosts);
        setMeta(loadedMeta);
        setBrands(loadedBrands);
        setOverview(loadedOverview);
        setTimeline(loadedTimeline);

        // Group comments by parent post id
        const map: Record<string, any[]> = {};
        for (const c of loadedComments) {
          if (!map[c.parentId]) map[c.parentId] = [];
          map[c.parentId].push(c);
        }
        setCommentsByPostId(map);
        setLoading(false);
      } catch (err) {
        console.error("Initialization error:", err);
        if (active) setLoading(false);
      }
    }

    initData();
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="h-screen w-screen flex flex-col items-center justify-center bg-[#F7F5FC] text-zinc-600 space-y-3">
        <div className="size-12 rounded-2xl bg-gradient-to-tr from-violet-600 to-pink-500 grid place-items-center text-white shadow-xl animate-pulse">
          <Loader2 className="size-6 animate-spin" />
        </div>
        <div className="text-center">
          <span className="font-bold text-base text-zinc-800 block">SOCIALPULSE</span>
          <span className="text-xs text-zinc-400">Loading Brand Perception Intelligence...</span>
        </div>
      </div>
    );
  }

  // Filter posts if brand selected
  const displayPosts =
    selectedBrand && selectedBrand !== "all"
      ? posts.filter((p) => p.brandId === selectedBrand || p.brand.toLowerCase() === selectedBrand.toLowerCase())
      : posts;

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#F7F5FC]">
      {/* 1. LEFT COLUMN: Navigation Sidebar (Reference Image 2) */}
      <SidebarNav
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        selectedBrand={selectedBrand}
        onSelectBrand={setSelectedBrand}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* 2. CENTER COLUMN: Social Media Feed / Active Workspace */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden bg-white">
        {activeTab === "feed" && (
          <CenterFeed
            posts={displayPosts.length > 0 ? displayPosts : posts}
            commentsByPostId={commentsByPostId}
            onAnalyzeText={(txt) => {
              setActiveTab("sentiment");
            }}
            selectedBrand={selectedBrand}
          />
        )}

        {activeTab === "overview" && (
          <OverviewView
            overviewData={overview}
            timelineData={timeline}
            brandRanking={brands}
          />
        )}

        {activeTab === "sentiment" && <SentimentView />}

        {activeTab === "forecast" && <ForecastingView selectedBrand={selectedBrand} />}

        {activeTab === "evaluation" && <ModelEvaluationView />}

        {activeTab === "brands" && (
          <BrandExplorerView
            brandList={brands}
            onSelectBrand={(id) => {
              setSelectedBrand(id);
              setActiveTab("feed");
            }}
            onGoToFeed={() => setActiveTab("feed")}
          />
        )}

        {activeTab === "campaigns" && (
          <CampaignView onGoToFeed={() => setActiveTab("feed")} />
        )}

        {activeTab === "emotions" && <EmotionView />}

        {activeTab === "audience" && <AudienceView />}

        {activeTab === "dataset" && <DatasetExplorerView posts={posts} meta={meta} />}

        {activeTab === "history" && <HistoryView />}

        {activeTab === "settings" && <SettingsView />}
      </main>

      {/* 3. RIGHT COLUMN: Live Brand Intelligence Panel (Reference Image 2) */}
      <RightBrandPanel
        selectedBrand={selectedBrand}
        onSelectBrand={setSelectedBrand}
        brandList={brands}
      />
    </div>
  );
}

