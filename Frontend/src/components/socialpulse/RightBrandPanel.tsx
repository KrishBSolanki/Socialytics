import React, { useState } from "react";
import {
  ArrowDownRight,
  ArrowUpRight,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Download,
  FileText,
  Menu,
  Plus,
  Share2,
  TrendingUp,
  User,
  Users,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { cn } from "@/lib/utils";

interface RightBrandPanelProps {
  selectedBrand: string;
  onSelectBrand: (brandId: string) => void;
  brandList: any[];
}

export function RightBrandPanel({
  selectedBrand,
  onSelectBrand,
  brandList,
}: RightBrandPanelProps) {
  const [activeTab, setActiveTab] = useState<"statistics" | "common" | "compare">("statistics");
  const [selectionName, setSelectionName] = useState("");
  const [isAnalyzedOpen, setIsAnalyzedOpen] = useState(true);

  // Active brand data
  const currentBrand =
    brandList.find((b) => b.id === selectedBrand) || brandList[0] || {
      id: "apple",
      name: "Apple",
      followers: 12668074,
      postCount: 142,
      engagement: { total: 421800, likes: 350000, comments: 71800, ratePerThousand: 33.2 },
    };

  // Sample or API-backed chart data matching Reference Image 2
  const daysOfWeekTrend = [
    { day: "Mon", posts: 14, engagement: 22, sentiment: 68 },
    { day: "Tue", posts: 18, engagement: 34, sentiment: 72 },
    { day: "Wed", posts: 24, engagement: 45, sentiment: 81 },
    { day: "Thu", posts: 21, engagement: 38, sentiment: 65 },
    { day: "Fri", posts: 29, engagement: 56, sentiment: 84 },
    { day: "Sat", posts: 35, engagement: 62, sentiment: 88 },
    { day: "Sun", posts: 31, engagement: 48, sentiment: 79 },
  ];

  const daysOfWeekMini = [
    { label: "M", val: 35 },
    { label: "T", val: 55 },
    { label: "W", val: 85 },
    { label: "T", val: 45 },
    { label: "F", val: 95 },
    { label: "S", val: 70 },
    { label: "S", val: 50 },
  ];

  const timeOfDayMini = [
    { label: "00", val: 20 },
    { label: "04", val: 10 },
    { label: "08", val: 65 },
    { label: "12", val: 90 },
    { label: "16", val: 80 },
    { label: "20", val: 95 },
    { label: "23", val: 40 },
  ];

  const erDaysMini = [
    { label: "M", val: 2.1 },
    { label: "T", val: 3.4 },
    { label: "W", val: 4.8 },
    { label: "T", val: 2.9 },
    { label: "F", val: 5.2 },
    { label: "S", val: 4.1 },
    { label: "S", val: 3.2 },
  ];

  const erHoursMini = [
    { label: "6a", val: 1.5 },
    { label: "9a", val: 3.8 },
    { label: "12p", val: 4.9 },
    { label: "3p", val: 4.2 },
    { label: "6p", val: 5.8 },
    { label: "9p", val: 4.5 },
    { label: "12a", val: 2.1 },
  ];

  const relActivityDays = [
    { label: "M", val: 40 },
    { label: "T", val: 60 },
    { label: "W", val: 90 },
    { label: "T", val: 75 },
    { label: "F", val: 100 },
    { label: "S", val: 85 },
    { label: "S", val: 65 },
  ];

  const relActivityHours = [
    { label: "4a", val: 15 },
    { label: "8a", val: 70 },
    { label: "12p", val: 95 },
    { label: "4p", val: 85 },
    { label: "8p", val: 90 },
    { label: "11p", val: 35 },
  ];

  const commonTopics = [
    { name: "Earthquake Relief Aid", count: 1420, pos: 88, neg: 12 },
    { name: "Emergency Search & Rescue", count: 1180, pos: 76, neg: 24 },
    { name: "Donations & Food Delivery", count: 940, pos: 92, neg: 8 },
    { name: "Temporary Shelter & Heating", count: 850, pos: 84, neg: 16 },
    { name: "Telecommunications & Cell", count: 730, pos: 35, neg: 65 },
    { name: "Logistics & Cargo Transport", count: 610, pos: 82, neg: 18 },
  ];

  const defaultAnalyzedPages = [
    { id: "apple", name: "Apple", followers: "12 668 074", icon: "A", color: "from-zinc-500 to-zinc-800" },
    { id: "pepsi", name: "Pepsi", followers: "36 743 290", icon: "P", color: "from-blue-600 to-red-600" },
    { id: "mercedes-amg", name: "Mercedes-AMG Petronas Formula One Team", followers: "36 743 290", icon: "M", color: "from-teal-600 to-zinc-900" },
    { id: "starbucks", name: "Starbucks", followers: "18 240 100", icon: "S", color: "from-emerald-700 to-emerald-900" },
  ];

  return (
    <aside
      className="hidden xl:flex flex-col w-80 2xl:w-96 h-screen border-l border-[#EAE7F0] select-none shrink-0 overflow-y-auto"
      style={{ backgroundColor: "#F7F5FC" }}
    >
      {/* Top Header Row (Reference Image 2) */}
      <div className="flex items-center justify-between px-4 py-3.5 border-b border-[#EAE7F0] bg-white/70 backdrop-blur-md sticky top-0 z-20">
        <button className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#EF4444] text-white text-xs font-semibold shadow-sm hover:bg-red-600 transition-colors">
          <Download className="size-3.5" />
          <span>Reports</span>
        </button>

        <div className="flex items-center gap-2">
          <div className="flex items-center text-xs font-semibold text-zinc-500 bg-white px-2 py-1 rounded-lg border border-[#EAE7F0]">
            <button className="px-1 hover:text-zinc-900">‹</button>
            <span className="px-1 text-zinc-700">0</span>
            <button className="px-1 hover:text-zinc-900">›</button>
          </div>

          <button className="size-7.5 rounded-full bg-violet-100 text-violet-700 flex items-center justify-center font-bold text-xs hover:bg-violet-200 transition-colors">
            <User className="size-4" />
          </button>
          <button className="p-1 text-zinc-500 hover:text-zinc-900">
            <Menu className="size-4" />
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Analyzed pages Header Section (Reference Image 2) */}
        <div className="bg-white rounded-2xl p-3.5 border border-[#EAE7F0] shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 cursor-pointer" onClick={() => setIsAnalyzedOpen(!isAnalyzedOpen)}>
              <ChevronDown className={cn("size-4 text-zinc-500 transition-transform", isAnalyzedOpen ? "rotate-0" : "-rotate-90")} />
              <span className="text-xs font-bold text-zinc-800">Analyzed pages</span>
            </div>
            <div className="text-[10px] text-zinc-400 font-medium text-right">
              <div>Today 5:35 AM</div>
              <div>Period: 12/10/2019 - 30/11/2020</div>
            </div>
          </div>

          {isAnalyzedOpen && (
            <div className="mt-3 space-y-2">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={selectionName}
                  onChange={(e) => setSelectionName(e.target.value)}
                  placeholder="Create name for selection..."
                  className="flex-1 bg-zinc-50 border border-zinc-200 rounded-lg px-2.5 py-1.5 text-xs text-zinc-700 placeholder:text-zinc-400 focus:outline-none focus:border-violet-500"
                />
                <button className="bg-zinc-900 text-white text-[11px] font-semibold px-2.5 py-1.5 rounded-lg hover:bg-zinc-800 transition-colors shrink-0">
                  + Favorites
                </button>
              </div>

              {/* Brand list with follower counts */}
              <div className="space-y-1.5 pt-1">
                {defaultAnalyzedPages.map((page) => (
                  <div
                    key={page.id}
                    onClick={() => onSelectBrand(page.id)}
                    className={cn(
                      "flex items-center justify-between p-2 rounded-xl transition-all cursor-pointer",
                      selectedBrand === page.id
                        ? "bg-violet-50 border border-violet-200"
                        : "hover:bg-zinc-50 border border-transparent"
                    )}
                  >
                    <div className="flex items-center gap-2 overflow-hidden">
                      <div className={cn("size-6 rounded-lg bg-gradient-to-br flex items-center justify-center text-[10px] font-bold text-white shrink-0", page.color)}>
                        {page.icon}
                      </div>
                      <div className="truncate">
                        <span className="text-xs font-semibold text-zinc-800 block truncate">{page.name}</span>
                        <span className="text-[10px] text-zinc-400">{page.followers} Followers</span>
                      </div>
                    </div>
                    <button className="size-5 rounded-full border border-zinc-200 flex items-center justify-center text-zinc-400 hover:text-violet-600 hover:border-violet-400">
                      <Plus className="size-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Tab Buttons: [STATISTICS] [COMMON] [COMPARE] (Reference Image 2) */}
        <div className="grid grid-cols-3 p-1 bg-zinc-200/70 rounded-xl text-xs font-semibold text-zinc-600">
          <button
            onClick={() => setActiveTab("statistics")}
            className={cn(
              "py-1.5 rounded-lg transition-all text-center",
              activeTab === "statistics"
                ? "bg-[#6047B5] text-white shadow-sm"
                : "hover:text-zinc-900"
            )}
          >
            STATISTICS
          </button>
          <button
            onClick={() => setActiveTab("common")}
            className={cn(
              "py-1.5 rounded-lg transition-all text-center",
              activeTab === "common"
                ? "bg-[#6047B5] text-white shadow-sm"
                : "hover:text-zinc-900"
            )}
          >
            COMMON
          </button>
          <button
            onClick={() => setActiveTab("compare")}
            className={cn(
              "py-1.5 rounded-lg transition-all text-center",
              activeTab === "compare"
                ? "bg-[#6047B5] text-white shadow-sm"
                : "hover:text-zinc-900"
            )}
          >
            COMPARE
          </button>
        </div>

        {/* Tab 1: STATISTICS */}
        {activeTab === "statistics" && (
          <div className="space-y-4">
            {/* Days of Week Line/Spline Chart (Reference Image 2 top right chart) */}
            <div className="bg-white rounded-2xl p-3.5 border border-[#EAE7F0] shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-zinc-800 tracking-wide uppercase">DAYS OF WEEK</span>
                <div className="flex items-center gap-1.5 text-[10px] text-zinc-400">
                  <span className="inline-block size-2 rounded-full bg-violet-600" /> Posts
                  <span className="inline-block size-2 rounded-full bg-pink-500 ml-1" /> Engagement
                </div>
              </div>
              <div className="h-32 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={daysOfWeekTrend} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                    <defs>
                      <linearGradient id="gradViolet" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="gradPink" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#EC4899" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#EC4899" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F0F5" />
                    <XAxis dataKey="day" tick={{ fontSize: 10, fill: "#9CA3AF" }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fontSize: 10, fill: "#9CA3AF" }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1E1B2E", borderRadius: "8px", border: "none", color: "#FFF", fontSize: "11px" }}
                    />
                    <Area type="monotone" dataKey="engagement" stroke="#8B5CF6" strokeWidth={2} fillOpacity={1} fill="url(#gradViolet)" />
                    <Area type="monotone" dataKey="posts" stroke="#EC4899" strokeWidth={2} fillOpacity={1} fill="url(#gradPink)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* 6 Mini Charts Grid (Reference Image 2) */}
            <div className="grid grid-cols-2 gap-2.5">
              {/* Mini 1: Days of week */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">Days of week</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={daysOfWeekMini} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#8B5CF6" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Mini 2: Time of day */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">Time of day</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={timeOfDayMini} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#A78BFA" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Mini 3: ERpost by days of week */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">ERpost by days</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={erDaysMini} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#C084FC" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Mini 4: ERpost by time of day */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">ERpost by time</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={erHoursMini} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#E879C5" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Mini 5: Relative activity by day */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">Relative day activity</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={relActivityDays} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#7C3AED" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Mini 6: Relative activity by time */}
              <div className="bg-white rounded-xl p-2.5 border border-[#EAE7F0] shadow-sm">
                <span className="text-[10px] font-bold text-zinc-700 block truncate">Relative time activity</span>
                <div className="h-16 w-full mt-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={relActivityHours} margin={{ top: 2, right: 2, left: 2, bottom: 0 }}>
                      <Bar dataKey="val" fill="#9333EA" radius={[2, 2, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: COMMON */}
        {activeTab === "common" && (
          <div className="bg-white rounded-2xl p-3.5 border border-[#EAE7F0] shadow-sm space-y-3">
            <span className="text-xs font-bold text-zinc-800 uppercase tracking-wide block">
              Frequently Discussed Topics
            </span>
            <div className="space-y-2.5">
              {commonTopics.map((top, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-zinc-700">{top.name}</span>
                    <span className="text-zinc-400 tabular-nums">{top.count} mentions</span>
                  </div>
                  <div className="h-1.5 w-full bg-zinc-100 rounded-full overflow-hidden flex">
                    <div style={{ width: `${top.pos}%` }} className="bg-emerald-500 h-full" title={`Positive: ${top.pos}%`} />
                    <div style={{ width: `${top.neg}%` }} className="bg-rose-500 h-full" title={`Negative: ${top.neg}%`} />
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-zinc-100">
              <span className="text-[11px] font-semibold text-zinc-500 uppercase tracking-wider block mb-2">
                Popular Keywords
              </span>
              <div className="flex flex-wrap gap-1.5">
                {["yardım", "destek", "deprem", "bölge", "ulaşım", "iletişim", "teşekkür", "seferberlik"].map((kw, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-violet-50 text-violet-700 border border-violet-100"
                  >
                    #{kw}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: COMPARE */}
        {activeTab === "compare" && (
          <div className="bg-white rounded-2xl p-3.5 border border-[#EAE7F0] shadow-sm space-y-3">
            <span className="text-xs font-bold text-zinc-800 uppercase tracking-wide block">
              Multi-Brand Comparison
            </span>
            <div className="space-y-2">
              {defaultAnalyzedPages.map((page) => (
                <div key={page.id} className="p-2.5 rounded-xl border border-zinc-100 bg-zinc-50/50 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-zinc-800">{page.name}</span>
                    <span className="text-[11px] font-semibold text-violet-700">ER 3.4%</span>
                  </div>
                  <div className="grid grid-cols-3 gap-1 text-[10px] text-zinc-500">
                    <div>
                      <span className="block text-zinc-400">Followers</span>
                      <span className="font-semibold text-zinc-700">{page.followers}</span>
                    </div>
                    <div>
                      <span className="block text-zinc-400">Perception</span>
                      <span className="font-semibold text-emerald-600">+0.68</span>
                    </div>
                    <div>
                      <span className="block text-zinc-400">CSR Posts</span>
                      <span className="font-semibold text-zinc-700">84</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}

