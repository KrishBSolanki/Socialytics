import React from "react";
import { Award, Heart, MessageSquare, Repeat, ShieldCheck, Target, TrendingUp } from "lucide-react";
import { formatCompact } from "@/utils/format";

interface CampaignViewProps {
  onGoToFeed: () => void;
}

export function CampaignView({ onGoToFeed }: CampaignViewProps) {
  const campaigns = [
    {
      name: "Corporate Giving & Donations",
      description: "Financial grants, supply trucks, food, water, and direct humanitarian funding announced by brands.",
      posts: 940,
      engagement: 382000,
      sentiment: 92.4,
      tag: "Top Response",
      color: "from-emerald-500 to-teal-700",
    },
    {
      name: "Emergency Search & Rescue Support",
      description: "Heavy machinery, rescue team deployment, logistics, and ground equipment provisions.",
      posts: 680,
      engagement: 295000,
      sentiment: 88.1,
      tag: "Critical Aid",
      color: "from-blue-600 to-indigo-700",
    },
    {
      name: "Sympathy & National Solidarity",
      description: "Public condolence messages, blackout avatars, and national mourning declarations.",
      posts: 1120,
      engagement: 410000,
      sentiment: 82.5,
      tag: "Highest Volume",
      color: "from-violet-600 to-purple-800",
    },
    {
      name: "Technical & Telecommunications Support",
      description: "Mobile base stations, free cellular packages, generator power, and connectivity restoration.",
      posts: 540,
      engagement: 215000,
      sentiment: 61.2,
      tag: "Controversial",
      color: "from-amber-500 to-rose-600",
    },
    {
      name: "Shelter & Heating Relief",
      description: "Tents, container homes, blankets, heaters, and temporary accommodation centers.",
      posts: 490,
      engagement: 198000,
      sentiment: 89.6,
      tag: "High Praise",
      color: "from-pink-500 to-rose-700",
    },
    {
      name: "Employee Volunteering & Mobilization",
      description: "Corporate employee blood drives, warehouse packing, and direct on-site support.",
      posts: 380,
      engagement: 142000,
      sentiment: 86.4,
      tag: "Grassroots",
      color: "from-teal-600 to-emerald-800",
    },
  ];

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Campaign &amp; Action Intelligence</h1>
        <p className="text-xs text-zinc-500 mt-1">
          Detailed performance breakdown of coded CSR and disaster relief initiatives across corporate sectors.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {campaigns.map((c, i) => (
          <div
            key={i}
            className="p-5 rounded-2xl border border-[#EAE7F0] bg-white shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between space-y-4"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-violet-100 text-violet-700">
                  {c.tag}
                </span>
                <span className="text-xs font-bold text-emerald-600">
                  {c.sentiment}% Positive
                </span>
              </div>
              <h3 className="font-bold text-sm text-zinc-900 leading-snug">{c.name}</h3>
              <p className="text-xs text-zinc-500 leading-relaxed">{c.description}</p>
            </div>

            <div className="grid grid-cols-2 gap-2 p-3 bg-zinc-50 rounded-xl text-xs">
              <div>
                <span className="text-[10px] text-zinc-400 block">Total Posts</span>
                <span className="font-bold text-zinc-800 tabular-nums">{c.posts}</span>
              </div>
              <div>
                <span className="text-[10px] text-zinc-400 block">Public Interactions</span>
                <span className="font-bold text-zinc-800 tabular-nums">{formatCompact(c.engagement)}</span>
              </div>
            </div>

            <button
              onClick={onGoToFeed}
              className="w-full py-2 rounded-xl text-xs font-bold text-violet-700 bg-violet-50 hover:bg-violet-100 transition-colors"
            >
              Filter Feed by this Action
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

