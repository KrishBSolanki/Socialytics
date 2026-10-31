import React, { useState } from "react";
import {
  Activity,
  BarChart3,
  Brain,
  Building2,
  Calendar,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Database,
  Heart,
  History,
  LayoutDashboard,
  MessageSquare,
  Rss,
  Search,
  Settings,
  Smile,
  Sparkles,
  Target,
  TrendingUp,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";

export type NavTab =
  | "overview"
  | "feed"
  | "brands"
  | "campaigns"
  | "sentiment"
  | "emotions"
  | "audience"
  | "forecast"
  | "evaluation"
  | "dataset"
  | "history"
  | "settings";

interface SidebarNavProps {
  activeTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  selectedBrand: string;
  onSelectBrand: (brandId: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export function SidebarNav({
  activeTab,
  onSelectTab,
  selectedBrand,
  onSelectBrand,
  collapsed,
  onToggleCollapse,
}: SidebarNavProps) {
  const [favoritesOpen, setFavoritesOpen] = useState(true);
  const [lastAnalyzedOpen, setLastAnalyzedOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const favoriteBrands = [
    { id: "bmw-groups", name: "BMW Groups", avatar: "B", color: "from-blue-600 to-indigo-700" },
    { id: "mcdonalds-fan-groups", name: "McDonalds fan groups", avatar: "M", color: "from-amber-500 to-red-600" },
    { id: "coffee-groups", name: "Coffee Groups", avatar: "C", color: "from-emerald-600 to-teal-800" },
    { id: "pepsi-fan-groups", name: "Pepsi fan groups", avatar: "P", color: "from-blue-500 to-red-500" },
    { id: "apple-pages", name: "Apple pages", avatar: "A", color: "from-zinc-400 to-zinc-700" },
    { id: "juventus-pages", name: "Juventus pages", avatar: "J", color: "from-zinc-800 to-black" },
    { id: "real-madrid-fan-groups", name: "Real Madrid fan groups", avatar: "R", color: "from-indigo-400 to-amber-500" },
  ];

  const recentBrands = [
    { id: "apple", name: "Apple", platform: "X", color: "from-zinc-500 to-zinc-800" },
    { id: "mercedes-amg", name: "Mercedes-AMG Petronas Form...", platform: "X", color: "from-teal-500 to-zinc-900" },
    { id: "starbucks", name: "Starbucks", platform: "X", color: "from-emerald-700 to-emerald-900" },
  ];

  const navItems: { id: NavTab; label: string; icon: React.ElementType; badge?: string }[] = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "feed", label: "Social Feed", icon: Rss, badge: "Live" },
    { id: "brands", label: "Brand Explorer", icon: Building2 },
    { id: "campaigns", label: "Campaign Intelligence", icon: Target },
    { id: "sentiment", label: "Sentiment Analysis", icon: Sparkles },
    { id: "emotions", label: "Emotion Analysis", icon: Smile },
    { id: "audience", label: "Audience Insights", icon: Users },
    { id: "forecast", label: "Forecasting", icon: TrendingUp },
    { id: "evaluation", label: "Model Evaluation", icon: Activity, badge: "99.2%" },
    { id: "dataset", label: "Dataset Explorer", icon: Database },
    { id: "history", label: "Prediction History", icon: History },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside
      className={cn(
        "relative flex flex-col h-screen select-none transition-all duration-300 z-30 shrink-0",
        collapsed ? "w-18" : "w-64 lg:w-72"
      )}
      style={{
        background: "linear-gradient(180deg, #24212D 0%, #351F38 45%, #512A52 100%)",
        color: "#F8FAFC",
      }}
    >
      {/* Top Header / Brand Logo */}
      <div className="flex items-center justify-between px-4 py-4.5 border-b border-white/10">
        <div className="flex items-center gap-3 overflow-hidden cursor-pointer" onClick={() => onSelectTab("feed")}>
          <div className="relative grid size-9 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-violet-500 to-pink-500 shadow-lg shadow-purple-500/30">
            <Brain className="size-5 text-white animate-pulse" />
          </div>
          {!collapsed && (
            <div className="leading-none">
              <span className="text-base font-bold tracking-tight text-white">
                SOCIAL<span className="text-pink-400">PULSE</span>
              </span>
              <span className="block mt-1 text-[10px] tracking-wider text-purple-200/60 uppercase font-semibold">
                Brand Intelligence
              </span>
            </div>
          )}
        </div>

        <button
          onClick={onToggleCollapse}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="p-1.5 rounded-lg text-white/60 hover:text-white hover:bg-white/10 transition-colors"
        >
          {collapsed ? <ChevronRight className="size-4" /> : <ChevronLeft className="size-4" />}
        </button>
      </div>

      {/* Global Search Input (Reference Image 2) */}
      {!collapsed && (
        <div className="px-3 pt-3 pb-1">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 size-3.5 text-white/40" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search..."
              className="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder:text-white/40 focus:outline-none focus:border-pink-500/50 focus:bg-white/10 transition-all"
            />
          </div>
        </div>
      )}

      {/* Scrollable Navigation Area */}
      <div className="flex-1 overflow-y-auto px-2 py-2 space-y-4 scrollbar-thin scrollbar-thumb-white/10">
        {/* Core Navigation Items */}
        <div className="space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                title={collapsed ? item.label : undefined}
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-all group relative",
                  isActive
                    ? "bg-gradient-to-r from-violet-600/80 to-pink-600/80 text-white shadow-md shadow-purple-900/40"
                    : "text-purple-200/70 hover:text-white hover:bg-white/5"
                )}
              >
                <Icon
                  className={cn(
                    "size-4 shrink-0 transition-transform group-hover:scale-110",
                    isActive ? "text-white" : "text-purple-300/70"
                  )}
                />
                {!collapsed && (
                  <span className="truncate flex-1 text-left">{item.label}</span>
                )}
                {!collapsed && item.badge && (
                  <span
                    className={cn(
                      "text-[10px] font-semibold px-1.5 py-0.5 rounded-full shrink-0",
                      isActive
                        ? "bg-white/20 text-white"
                        : "bg-pink-500/20 text-pink-300 border border-pink-500/30"
                    )}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* FAVORITES Section (from Reference Image 2) */}
        {!collapsed && (
          <div className="pt-2 border-t border-white/10">
            <button
              onClick={() => setFavoritesOpen(!favoritesOpen)}
              className="w-full flex items-center justify-between px-3 py-1.5 text-[11px] font-semibold tracking-wider text-purple-200/50 uppercase hover:text-white transition-colors"
            >
              <span>FAVORITES</span>
              <ChevronDown
                className={cn(
                  "size-3.5 transition-transform text-white/40",
                  favoritesOpen ? "rotate-0" : "-rotate-90"
                )}
              />
            </button>

            {favoritesOpen && (
              <div className="mt-1 space-y-0.5">
                {favoriteBrands.map((brand) => (
                  <button
                    key={brand.id}
                    onClick={() => {
                      onSelectBrand(brand.id);
                      onSelectTab("feed");
                    }}
                    className={cn(
                      "w-full flex items-center gap-2.5 px-3 py-1.5 rounded-xl text-xs transition-colors group",
                      selectedBrand === brand.id
                        ? "bg-white/15 text-white font-medium"
                        : "text-purple-200/70 hover:text-white hover:bg-white/5"
                    )}
                  >
                    <div
                      className={cn(
                        "size-5.5 rounded-lg bg-gradient-to-br flex items-center justify-center text-[10px] font-bold text-white shadow-sm shrink-0",
                        brand.color
                      )}
                    >
                      {brand.avatar}
                    </div>
                    <span className="truncate text-left flex-1">{brand.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* LAST ANALYZED Section (from Reference Image 2) */}
        {!collapsed && (
          <div className="pt-2 border-t border-white/10">
            <button
              onClick={() => setLastAnalyzedOpen(!lastAnalyzedOpen)}
              className="w-full flex items-center justify-between px-3 py-1.5 text-[11px] font-semibold tracking-wider text-purple-200/50 uppercase hover:text-white transition-colors"
            >
              <span>LAST ANALYZED</span>
              <ChevronDown
                className={cn(
                  "size-3.5 transition-transform text-white/40",
                  lastAnalyzedOpen ? "rotate-0" : "-rotate-90"
                )}
              />
            </button>

            {lastAnalyzedOpen && (
              <div className="mt-1 space-y-0.5">
                {recentBrands.map((brand) => (
                  <button
                    key={brand.id}
                    onClick={() => {
                      onSelectBrand(brand.id);
                      onSelectTab("feed");
                    }}
                    className={cn(
                      "w-full flex items-center gap-2.5 px-3 py-1.5 rounded-xl text-xs transition-colors group",
                      selectedBrand === brand.id
                        ? "bg-white/15 text-white font-medium"
                        : "text-purple-200/70 hover:text-white hover:bg-white/5"
                    )}
                  >
                    <div
                      className={cn(
                        "size-5 rounded-md bg-gradient-to-br flex items-center justify-center text-[10px] font-bold text-white shrink-0",
                        brand.color
                      )}
                    >
                      {brand.name[0]}
                    </div>
                    <span className="truncate text-left flex-1">{brand.name}</span>
                    <span className="text-[10px] px-1 py-0.2 rounded bg-blue-500/20 text-blue-300 font-medium">
                      {brand.platform}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Bottom Footer User & Status */}
      <div className="p-3 border-t border-white/10 bg-black/10">
        <div className="flex items-center gap-2.5">
          <div className="size-7 rounded-full bg-gradient-to-tr from-pink-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0">
            DS
          </div>
          {!collapsed && (
            <div className="truncate leading-tight">
              <span className="text-xs font-semibold text-white block truncate">Semester 7 Project</span>
              <span className="text-[10px] text-emerald-400 flex items-center gap-1">
                <span className="size-1.5 rounded-full bg-emerald-400 animate-ping inline-block" />
                Backend Ready
              </span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}

