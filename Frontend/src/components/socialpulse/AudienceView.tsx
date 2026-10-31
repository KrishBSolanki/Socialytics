import React from "react";
import { BarChart3, Clock, Heart, MessageCircle, Repeat, Users } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import { formatCompact } from "@/utils/format";

export function AudienceView() {
  const hourlyActivity = [
    { hour: "00:00", interactions: 4200 },
    { hour: "03:00", interactions: 1800 },
    { hour: "06:00", interactions: 3100 },
    { hour: "09:00", interactions: 12400 },
    { hour: "12:00", interactions: 18600 },
    { hour: "15:00", interactions: 16900 },
    { hour: "18:00", interactions: 24500 },
    { hour: "21:00", interactions: 21800 },
  ];

  const responseDepth = [
    { depth: "1-5 Comments", share: 58 },
    { depth: "6-20 Comments", share: 26 },
    { depth: "21-50 Comments", share: 11 },
    { depth: "50+ Comments", share: 5 },
  ];

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Audience Insights &amp; Engagement Patterns</h1>
        <p className="text-xs text-zinc-500 mt-1">
          Behavioral metrics, peak interaction windows, and audience response velocity across Platform X.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Peak Interaction Timing */}
        <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-zinc-800">Peak Audience Engagement Windows</h3>
              <p className="text-xs text-zinc-400">Total comments, likes, and shares aggregated by hour</p>
            </div>
            <span className="text-[10px] font-semibold text-violet-700 bg-violet-100 px-2 py-0.5 rounded-full">
              Peak: 18:00 - 22:00
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={hourlyActivity}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F0F5" />
                <XAxis dataKey="hour" tick={{ fontSize: 10, fill: "#9CA3AF" }} />
                <YAxis tick={{ fontSize: 10, fill: "#9CA3AF" }} />
                <Tooltip formatter={(v: any) => [formatCompact(v), "Interactions"]} />
                <Bar dataKey="interactions" fill="#6047B5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Post Depth & Response Velocity */}
        <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-zinc-800">Audience Discussion Depth</h3>
              <p className="text-xs text-zinc-400">Distribution of thread comments per individual brand post</p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={responseDepth} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F1F0F5" />
                <XAxis type="number" unit="%" tick={{ fontSize: 10, fill: "#9CA3AF" }} />
                <YAxis dataKey="depth" type="category" tick={{ fontSize: 11, fill: "#4B5563" }} />
                <Tooltip />
                <Bar dataKey="share" fill="#E879C5" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

