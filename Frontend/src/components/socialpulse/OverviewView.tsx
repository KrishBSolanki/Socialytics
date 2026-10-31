import React from "react";
import {
  Activity,
  BarChart2,
  Building2,
  Heart,
  MessageSquare,
  Repeat,
  Smile,
  Sparkles,
  TrendingUp,
  Users,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { KpiCard } from "@/components/common/KpiCard";
import { formatCompact, formatPercent } from "@/utils/format";

interface OverviewViewProps {
  overviewData: any;
  timelineData: any[];
  brandRanking: any[];
}

export function OverviewView({
  overviewData,
  timelineData,
  brandRanking,
}: OverviewViewProps) {
  const pieData = [
    { name: "Positive", value: overviewData?.positivePercentage || 64.2, color: "#16B981" },
    { name: "Neutral", value: overviewData?.neutralPercentage || 24.1, color: "#7774E8" },
    { name: "Negative", value: overviewData?.negativePercentage || 11.7, color: "#EF4444" },
  ];

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      {/* View Header */}
      <div className="border-b border-[#EAE7F0] pb-4">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Intelligence Overview</h1>
        <p className="text-xs text-zinc-500 mt-1">
          High-level executive summary of brand perception, engagement volume, and public sentiment during disaster relief communication.
        </p>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Total Tracked Brands"
          value={overviewData?.totalBrands || 52}
          format={(n) => n.toString()}
          icon={Building2}
          tone="violet"
          hint="52 local & global brands"
        />
        <KpiCard
          label="Tracked Posts"
          value={overviewData?.totalPosts || 4617}
          format={formatCompact}
          icon={MessageSquare}
          tone="pink"
          hint="Feb 6 earthquake timeline"
        />
        <KpiCard
          label="Public Comments"
          value={overviewData?.totalComments || 27530}
          format={formatCompact}
          icon={Users}
          tone="info"
          hint="Sampled audience reactions"
        />
        <KpiCard
          label="Positive Sentiment"
          value={overviewData?.positivePercentage || 64.2}
          format={(n) => `${n.toFixed(1)}%`}
          icon={Smile}
          tone="success"
          hint="Predominant public support"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sentiment Distribution Donut Chart */}
        <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-zinc-800">Public Sentiment Distribution</h3>
            <p className="text-xs text-zinc-400 mt-0.5">Aggregated polarity of audience engagement</p>
          </div>

          <div className="h-56 w-full my-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val: any) => [`${val}%`, "Share"]}
                  contentStyle={{ backgroundColor: "#1E1B2E", borderRadius: "8px", border: "none", color: "#FFF", fontSize: "11px" }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-zinc-100 text-center">
            {pieData.map((item) => (
              <div key={item.name}>
                <span className="text-[11px] text-zinc-400 block">{item.name}</span>
                <span className="text-xs font-bold" style={{ color: item.color }}>
                  {item.value}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Daily Sentiment Timeline */}
        <div className="lg:col-span-2 bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-zinc-800">Daily Public Engagement &amp; Sentiment</h3>
              <p className="text-xs text-zinc-400 mt-0.5">Chronological timeline of post volume and positive sentiment</p>
            </div>
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-violet-100 text-violet-700">
              Active Period
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="areaPos" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#16B981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#16B981" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="areaNeg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F0F5" />
                <XAxis dataKey="date" tick={{ fontSize: 10, fill: "#9CA3AF" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: "#9CA3AF" }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#1E1B2E", borderRadius: "8px", border: "none", color: "#FFF", fontSize: "11px" }}
                />
                <Area type="monotone" dataKey="positive" stroke="#16B981" strokeWidth={2} fillOpacity={1} fill="url(#areaPos)" name="Positive" />
                <Area type="monotone" dataKey="negative" stroke="#EF4444" strokeWidth={2} fillOpacity={1} fill="url(#areaNeg)" name="Negative" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Brands Performance Ranking */}
      <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
        <h3 className="text-sm font-bold text-zinc-800 mb-1">Leading Brands by Engagement Volume</h3>
        <p className="text-xs text-zinc-400 mb-4">Brands with highest audience interactions and perception scores</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {brandRanking.slice(0, 8).map((b, i) => (
            <div key={b.id || i} className="p-3 rounded-xl bg-zinc-50 border border-zinc-100 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-zinc-800 truncate">{b.name}</span>
                <span className="text-[10px] font-semibold text-violet-700 bg-violet-100 px-1.5 py-0.2 rounded">
                  #{i + 1}
                </span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-500 text-[11px]">Total Interactions</span>
                <span className="font-semibold text-zinc-700 tabular-nums">
                  {formatCompact(b.engagement?.total || b.totalEngagement || 0)}
                </span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-500 text-[11px]">Perception Index</span>
                <span className="font-bold text-emerald-600 tabular-nums">
                  {b.perceptionIndex ? (b.perceptionIndex > 0 ? `+${b.perceptionIndex}` : b.perceptionIndex) : "+0.72"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

