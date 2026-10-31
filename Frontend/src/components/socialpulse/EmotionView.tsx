import React, { useState } from "react";
import { AlertCircle, Heart, MessageSquare, Smile, TrendingUp } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { EmotionBadge, PolarityBadge } from "@/components/common/Badges";
import { EMOTION_META } from "@/utils/emotion";

export function EmotionView() {
  const [selectedEmotion, setSelectedEmotion] = useState<string>("happy");

  const emotionData = [
    { emotion: "happy", label: "Happy", count: 12450, percentage: 45.2, emoji: "😊", polarity: "Positive", color: "#10B981" },
    { emotion: "neutral", label: "Neutral", count: 6620, percentage: 24.1, emoji: "😐", polarity: "Neutral", color: "#8B5CF6" },
    { emotion: "surprise", label: "Surprise", count: 2480, percentage: 9.0, emoji: "😮", polarity: "Neutral", color: "#06B6D4" },
    { emotion: "sad", label: "Sad", count: 2150, percentage: 7.8, emoji: "😢", polarity: "Negative", color: "#6366F1" },
    { emotion: "anger", label: "Anger", count: 1840, percentage: 6.7, emoji: "😠", polarity: "Negative", color: "#EF4444" },
    { emotion: "fear", label: "Fear", count: 1260, percentage: 4.6, emoji: "😨", polarity: "Negative", color: "#F59E0B" },
    { emotion: "disgust", label: "Disgust", count: 730, percentage: 2.6, emoji: "🤢", polarity: "Negative", color: "#EC4899" },
  ];

  const radarData = emotionData.map((e) => ({
    subject: e.label,
    A: e.percentage,
    fullMark: 100,
  }));

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Public Emotion Intelligence</h1>
        <p className="text-xs text-zinc-500 mt-1">
          7-class granular emotion modeling derived from the Zenodo disaster engagement dataset.
        </p>
      </div>

      {/* Grid of 7 Emotions */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {emotionData.map((e) => (
          <button
            key={e.emotion}
            onClick={() => setSelectedEmotion(e.emotion)}
            className={`p-3 rounded-2xl border text-center transition-all ${
              selectedEmotion === e.emotion
                ? "bg-violet-50 border-violet-400 shadow-sm"
                : "bg-zinc-50/60 border-zinc-200/80 hover:bg-zinc-100"
            }`}
          >
            <span className="text-2xl block">{e.emoji}</span>
            <span className="text-xs font-bold text-zinc-800 block mt-1">{e.label}</span>
            <span className="text-[11px] font-semibold block" style={{ color: e.color }}>
              {e.percentage}%
            </span>
          </button>
        ))}
      </div>

      {/* Radar & Bar Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
          <h3 className="text-sm font-bold text-zinc-800 mb-1">Emotion Spectrum Polygon</h3>
          <p className="text-xs text-zinc-400 mb-4">Relative frequency across 27,530 public reactions</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#E5E7EB" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: "#4B5563" }} />
                <PolarRadiusAxis angle={30} domain={[0, 50]} tick={{ fontSize: 10, fill: "#9CA3AF" }} />
                <Radar name="Public Emotion %" dataKey="A" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.4} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="bg-white rounded-2xl p-5 border border-[#EAE7F0] shadow-sm">
          <h3 className="text-sm font-bold text-zinc-800 mb-1">Emotion Distribution Ranking</h3>
          <p className="text-xs text-zinc-400 mb-4">Frequency count and share of total audience responses</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={emotionData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F1F0F5" />
                <XAxis type="number" tick={{ fontSize: 10, fill: "#9CA3AF" }} unit="%" />
                <YAxis dataKey="label" type="category" tick={{ fontSize: 11, fill: "#4B5563" }} />
                <Tooltip />
                <Bar dataKey="percentage" fill="#6047B5" radius={[0, 4, 4, 0]}>
                  {emotionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

