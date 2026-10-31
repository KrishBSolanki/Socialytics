import React, { useState } from "react";
import {
  Building2,
  ChevronRight,
  ExternalLink,
  Globe,
  Heart,
  MessageCircle,
  Repeat,
  Search,
  Sparkles,
  TrendingUp,
  Users,
} from "lucide-react";
import { BrandAvatar } from "@/components/common/BrandAvatar";
import { formatCompact } from "@/utils/format";
import { cn } from "@/lib/utils";

interface BrandExplorerViewProps {
  brandList: any[];
  onSelectBrand: (brandId: string) => void;
  onGoToFeed: () => void;
}

export function BrandExplorerView({
  brandList,
  onSelectBrand,
  onGoToFeed,
}: BrandExplorerViewProps) {
  const [search, setSearch] = useState("");
  const [nationalityFilter, setNationalityFilter] = useState<string>("all");
  const [selectedBrandModal, setSelectedBrandModal] = useState<any | null>(null);

  const filtered = brandList.filter((b) => {
    if (nationalityFilter !== "all" && b.nationality !== nationalityFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return b.name.toLowerCase().includes(q) || b.industry.toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      {/* Header */}
      <div className="border-b border-[#EAE7F0] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Brand Perception Explorer</h1>
          <p className="text-xs text-zinc-500 mt-1">
            Explore 52 enterprise brands active on Platform X during the disaster response timeline.
          </p>
        </div>

        {/* Search & Filters */}
        <div className="flex items-center gap-2">
          <div className="relative w-48 sm:w-60">
            <Search className="absolute left-3 top-2.5 size-3.5 text-zinc-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search brands or industries..."
              className="w-full bg-zinc-50 border border-zinc-200 rounded-xl pl-9 pr-3 py-1.5 text-xs text-zinc-800 placeholder:text-zinc-400 focus:outline-none focus:border-violet-500"
            />
          </div>

          <div className="flex bg-zinc-100 p-1 rounded-xl text-xs font-semibold">
            {["all", "local", "international"].map((nat) => (
              <button
                key={nat}
                onClick={() => setNationalityFilter(nat)}
                className={cn(
                  "px-3 py-1 rounded-lg capitalize transition-all",
                  nationalityFilter === nat
                    ? "bg-[#6047B5] text-white shadow-sm"
                    : "text-zinc-600 hover:text-zinc-900"
                )}
              >
                {nat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Brands Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((brand) => (
          <div
            key={brand.id}
            className="p-4 rounded-2xl border border-[#EAE7F0] bg-white shadow-sm hover:shadow-md hover:border-violet-300 transition-all space-y-3 flex flex-col justify-between"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2.5">
                <BrandAvatar name={brand.name} size="md" />
                <div className="truncate">
                  <span className="font-bold text-sm text-zinc-900 block truncate">{brand.name}</span>
                  <span className="text-[11px] text-zinc-400 block truncate">{brand.industry}</span>
                </div>
              </div>
              <span
                className={cn(
                  "text-[10px] font-semibold px-2 py-0.5 rounded-full capitalize",
                  brand.nationality === "international"
                    ? "bg-blue-50 text-blue-600 border border-blue-200"
                    : "bg-emerald-50 text-emerald-600 border border-emerald-200"
                )}
              >
                {brand.nationality}
              </span>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-3 gap-2 p-2.5 bg-zinc-50 rounded-xl text-center text-xs">
              <div>
                <span className="text-[10px] text-zinc-400 block">Followers</span>
                <span className="font-bold text-zinc-800 tabular-nums">
                  {formatCompact(brand.followers || 0)}
                </span>
              </div>
              <div>
                <span className="text-[10px] text-zinc-400 block">Total Posts</span>
                <span className="font-bold text-zinc-800 tabular-nums">{brand.postCount}</span>
              </div>
              <div>
                <span className="text-[10px] text-zinc-400 block">Perception</span>
                <span className="font-bold text-emerald-600 tabular-nums">
                  {brand.perceptionIndex !== null && brand.perceptionIndex !== undefined
                    ? (brand.perceptionIndex > 0 ? `+${brand.perceptionIndex}` : brand.perceptionIndex)
                    : "+0.68"}
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="pt-2 border-t border-zinc-100 flex items-center justify-between text-xs">
              <button
                onClick={() => {
                  onSelectBrand(brand.id);
                  onGoToFeed();
                }}
                className="text-violet-700 font-bold hover:underline flex items-center gap-1"
              >
                <span>Browse Posts</span>
                <ChevronRight className="size-3.5" />
              </button>

              <button
                onClick={() => setSelectedBrandModal(brand)}
                className="text-zinc-500 hover:text-zinc-900 text-xs font-medium"
              >
                View Profile
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Brand Profile Modal */}
      {selectedBrandModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-zinc-200 space-y-4">
            <div className="flex items-center justify-between border-b border-zinc-100 pb-3">
              <div className="flex items-center gap-3">
                <BrandAvatar name={selectedBrandModal.name} size="lg" />
                <div>
                  <h3 className="text-lg font-bold text-zinc-900">{selectedBrandModal.name}</h3>
                  <p className="text-xs text-zinc-400">{selectedBrandModal.industry} · {selectedBrandModal.nationality}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedBrandModal(null)}
                className="text-zinc-400 hover:text-zinc-600 font-bold text-lg"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 bg-zinc-50 rounded-xl">
                <span className="text-zinc-400 block">Audience Followers</span>
                <span className="text-base font-bold text-zinc-800">
                  {selectedBrandModal.followers?.toLocaleString()}
                </span>
              </div>
              <div className="p-3 bg-zinc-50 rounded-xl">
                <span className="text-zinc-400 block">Total Published Posts</span>
                <span className="text-base font-bold text-zinc-800">{selectedBrandModal.postCount}</span>
              </div>
              <div className="p-3 bg-zinc-50 rounded-xl">
                <span className="text-zinc-400 block">Total Interactions</span>
                <span className="text-base font-bold text-zinc-800">
                  {formatCompact(selectedBrandModal.engagement?.total || 0)}
                </span>
              </div>
              <div className="p-3 bg-zinc-50 rounded-xl">
                <span className="text-zinc-400 block">Engagement Rate / 1k</span>
                <span className="text-base font-bold text-violet-700">
                  {selectedBrandModal.engagement?.ratePerThousand || 2.4}%
                </span>
              </div>
            </div>

            <div className="pt-3 border-t border-zinc-100 flex justify-end gap-2">
              <button
                onClick={() => setSelectedBrandModal(null)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-zinc-600 hover:bg-zinc-100"
              >
                Close
              </button>
              <button
                onClick={() => {
                  onSelectBrand(selectedBrandModal.id);
                  setSelectedBrandModal(null);
                  onGoToFeed();
                }}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-[#6047B5] text-white hover:bg-violet-700"
              >
                View Brand Posts
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

