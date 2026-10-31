import React, { useState } from "react";
import {
  Calendar,
  Camera,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Eye,
  Filter,
  Heart,
  Image as ImageIcon,
  MessageCircle,
  Repeat,
  Search,
  Share2,
  Sparkles,
  Tag,
  Video,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { BrandAvatar } from "@/components/common/BrandAvatar";
import { EmotionBadge, PolarityBadge } from "@/components/common/Badges";
import { formatCompact, formatDate } from "@/utils/format";
import type { SocialPost } from "@/types";

interface CenterFeedProps {
  posts: SocialPost[];
  commentsByPostId: Record<string, any[]>;
  onAnalyzeText?: (text: string) => void;
  selectedBrand?: string;
}

export function CenterFeed({
  posts,
  commentsByPostId,
  onAnalyzeText,
  selectedBrand,
}: CenterFeedProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"likes" | "comments" | "reposts" | "er" | "newest">("likes");
  const [filterMedia, setFilterMedia] = useState<"all" | "image" | "video">("all");
  const [expandedCommentsPostId, setExpandedCommentsPostId] = useState<string | null>(null);
  const [commentPolarityFilter, setCommentPolarityFilter] = useState<string>("all");

  // Filtering
  const filteredPosts = posts.filter((p) => {
    if (filterMedia === "image" && !p.image) return false;
    if (filterMedia === "video" && !p.video) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const match =
        p.brand.toLowerCase().includes(q) ||
        p.industry.toLowerCase().includes(q) ||
        (p.aidAction && p.aidAction.toLowerCase().includes(q)) ||
        p.postType.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  // Sorting
  const sortedPosts = [...filteredPosts].sort((a, b) => {
    if (sortBy === "likes") return (b.likes || 0) - (a.likes || 0);
    if (sortBy === "comments") return (b.comments || 0) - (a.comments || 0);
    if (sortBy === "reposts") return (b.retweets || 0) - (a.retweets || 0);
    if (sortBy === "er") {
      const erA = a.followers ? (((a.likes || 0) + (a.comments || 0) + (a.retweets || 0)) / a.followers) * 100 : 0;
      const erB = b.followers ? (((b.likes || 0) + (b.comments || 0) + (b.retweets || 0)) / b.followers) * 100 : 0;
      return erB - erA;
    }
    return b.ts.localeCompare(a.ts);
  });

  const toggleComments = (postId: string) => {
    if (expandedCommentsPostId === postId) {
      setExpandedCommentsPostId(null);
    } else {
      setExpandedCommentsPostId(postId);
    }
  };

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto border-r border-[#EAE7F0]">
      {/* Feed Header (Reference Image 2) */}
      <div className="sticky top-0 z-20 bg-white/95 backdrop-blur-md px-6 py-4 border-b border-[#EAE7F0] space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold text-zinc-900 tracking-tight">Feed</h1>
            {/* Search in feed input */}
            <div className="relative w-48 sm:w-64">
              <Search className="absolute left-3 top-2.5 size-3.5 text-zinc-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search in feed..."
                className="w-full bg-zinc-100/80 border border-zinc-200/80 rounded-full pl-9 pr-3 py-1.5 text-xs text-zinc-800 placeholder:text-zinc-400 focus:outline-none focus:border-violet-500 focus:bg-white transition-all"
              />
            </div>
          </div>

          {/* Date range display */}
          <div className="flex items-center gap-2 bg-zinc-100 px-3 py-1.5 rounded-full border border-zinc-200 text-xs text-zinc-600 font-medium">
            <Calendar className="size-3.5 text-zinc-500" />
            <span>05/10/2023 - 10/10/2023</span>
          </div>
        </div>

        {/* Sorting & Filtering Toolbar (Reference Image 2) */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
          {/* Sorting Buttons */}
          <div className="flex items-center gap-1 overflow-x-auto text-xs">
            <span className="text-[11px] font-semibold text-zinc-400 mr-1">Sorting:</span>
            {[
              { id: "likes", label: "Likes" },
              { id: "reposts", label: "Reposts" },
              { id: "comments", label: "Comments" },
              { id: "er", label: "ER" },
              { id: "newest", label: "Newest" },
            ].map((s) => (
              <button
                key={s.id}
                onClick={() => setSortBy(s.id as any)}
                className={cn(
                  "px-3 py-1 rounded-lg font-medium transition-all",
                  sortBy === s.id
                    ? "bg-[#6047B5] text-white shadow-sm"
                    : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70"
                )}
              >
                {s.label}
              </button>
            ))}
          </div>

          {/* Filtering Icons */}
          <div className="flex items-center gap-1.5 text-xs">
            <span className="text-[11px] font-semibold text-zinc-400 mr-1">Filtering:</span>
            <button
              onClick={() => setFilterMedia("all")}
              title="All posts"
              className={cn(
                "p-1.5 rounded-lg transition-colors border",
                filterMedia === "all" ? "bg-violet-50 border-violet-300 text-violet-700" : "border-zinc-200 text-zinc-500 hover:bg-zinc-100"
              )}
            >
              <Filter className="size-3.5" />
            </button>
            <button
              onClick={() => setFilterMedia("image")}
              title="Filter photos"
              className={cn(
                "p-1.5 rounded-lg transition-colors border",
                filterMedia === "image" ? "bg-violet-50 border-violet-300 text-violet-700" : "border-zinc-200 text-zinc-500 hover:bg-zinc-100"
              )}
            >
              <Camera className="size-3.5" />
            </button>
            <button
              onClick={() => setFilterMedia("video")}
              title="Filter videos"
              className={cn(
                "p-1.5 rounded-lg transition-colors border",
                filterMedia === "video" ? "bg-violet-50 border-violet-300 text-violet-700" : "border-zinc-200 text-zinc-500 hover:bg-zinc-100"
              )}
            >
              <Video className="size-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Posts Stream */}
      <div className="p-6 space-y-6 max-w-3xl mx-auto">
        {sortedPosts.slice(0, 25).map((post) => {
          const postComments = commentsByPostId[post.id] || [];
          const isExpanded = expandedCommentsPostId === post.id;
          const erPercent = post.followers
            ? ((((post.likes || 0) + (post.comments || 0) + (post.retweets || 0)) / post.followers) * 100).toFixed(2)
            : "2.24";

          // Calculate predominant polarity if emotions exist
          let dominantSentiment: "positive" | "negative" | "neutral" = "neutral";
          if (post.emotions) {
            const pos = post.emotions.happy || 0;
            const neg = (post.emotions.anger || 0) + (post.emotions.disgust || 0) + (post.emotions.fear || 0) + (post.emotions.sad || 0);
            dominantSentiment = pos > neg ? "positive" : neg > pos ? "negative" : "neutral";
          }

          return (
            <article
              key={post.id}
              className="bg-white rounded-2xl border border-[#EAE7F0] overflow-hidden shadow-sm hover:shadow-md transition-shadow"
            >
              {/* Post Header: Avatar, Brand, Timestamp */}
              <div className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <BrandAvatar name={post.brand} size="md" />
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="font-bold text-sm text-zinc-900">{post.brand}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-zinc-100 text-zinc-600 font-medium">
                        {post.industry}
                      </span>
                      {post.nationality === "international" && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-blue-50 text-blue-600 font-medium">
                          Global
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-zinc-400 block mt-0.5">
                      {formatDate(post.ts)} · X (Twitter)
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <PolarityBadge polarity={dominantSentiment} />
                </div>
              </div>

              {/* Engagement Metrics Row (Reference Image 2 style) */}
              <div className="px-4 py-2 border-t border-b border-zinc-100 bg-zinc-50/60 flex items-center gap-4 text-xs font-semibold text-zinc-600">
                <span className="text-violet-700 bg-violet-100/80 px-2 py-0.5 rounded-md text-[11px]">
                  ERpost {erPercent}%
                </span>
                <span className="flex items-center gap-1 text-rose-600">
                  <Heart className="size-3.5 fill-rose-500/20" />
                  {formatCompact(post.likes || 0)}
                </span>
                <span className="flex items-center gap-1 text-blue-600">
                  <MessageCircle className="size-3.5" />
                  {formatCompact(post.comments || 0)}
                </span>
                <span className="flex items-center gap-1 text-emerald-600">
                  <Repeat className="size-3.5" />
                  {formatCompact(post.retweets || 0)}
                </span>
              </div>

              {/* Media Card Preview (Reference Image 2 center image showcase) */}
              {(post.image || post.video) && (
                <div className="relative w-full aspect-video bg-gradient-to-tr from-violet-950 via-purple-900 to-indigo-900 overflow-hidden flex items-center justify-center p-8">
                  {/* Stylized visual graphic simulating post media */}
                  <div className="text-center space-y-2 z-10 max-w-md">
                    <div className="inline-block p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-xl">
                      {post.video ? <Video className="size-8 text-pink-400 mx-auto" /> : <ImageIcon className="size-8 text-violet-300 mx-auto" />}
                    </div>
                    <h3 className="text-lg font-bold text-white tracking-tight">
                      {post.brand} CSR Communication Campaign
                    </h3>
                    <p className="text-xs text-purple-200/80 line-clamp-2">
                      {post.aidAction ? `Action: ${post.aidAction}` : "Emergency Relief Operations & Community Support"}
                    </p>
                  </div>
                  <div className="absolute inset-0 bg-radial-gradient from-transparent to-black/40 pointer-events-none" />
                </div>
              )}

              {/* Post Content & Context */}
              <div className="p-4 space-y-3">
                <p className="text-sm text-zinc-800 font-medium leading-relaxed">
                  {post.text || `Official CSR post by ${post.brand} regarding ${post.aidAction || "emergency relief operations"} during the ${post.period} period. Relief classification: ${post.reliefEffect}.`}
                </p>

                {/* Hashtags and Meta Tags */}
                <div className="flex flex-wrap gap-1.5 text-xs">
                  <span className="text-violet-600 font-semibold hover:underline cursor-pointer">
                    #{post.brand.toLowerCase().replace(/[^a-z0-9]/g, "")}
                  </span>
                  {post.aidAction && (
                    <span className="text-violet-600 font-semibold hover:underline cursor-pointer">
                      #{post.aidAction.toLowerCase().replace(/[^a-z0-9]/g, "")}
                    </span>
                  )}
                  <span className="text-pink-600 font-semibold hover:underline cursor-pointer">#socialpulse</span>
                  <span className="text-blue-600 font-semibold hover:underline cursor-pointer">#csr</span>
                </div>

                {/* Emotion Distribution Chips */}
                {post.emotions && (
                  <div className="pt-2 border-t border-zinc-100 flex flex-wrap gap-1.5 items-center">
                    <span className="text-[11px] font-semibold text-zinc-400 mr-1">Audience Emotions:</span>
                    {Object.entries(post.emotions).map(([emo, count]) => {
                      if (count <= 0) return null;
                      return <EmotionBadge key={emo} emotion={emo as any} count={count} />;
                    })}
                  </div>
                )}

                {/* Actions Row */}
                <div className="pt-2 flex items-center justify-between border-t border-zinc-100 text-xs">
                  <button
                    onClick={() => toggleComments(post.id)}
                    className="inline-flex items-center gap-1.5 text-violet-700 font-semibold hover:text-violet-900 transition-colors"
                  >
                    <MessageCircle className="size-4" />
                    <span>
                      {isExpanded
                        ? "Hide Audience Comments"
                        : `View Audience Comments (${postComments.length || post.sampledComments || 0})`}
                    </span>
                    {isExpanded ? <ChevronUp className="size-3.5" /> : <ChevronDown className="size-3.5" />}
                  </button>

                  {onAnalyzeText && (
                    <button
                      onClick={() => onAnalyzeText(post.text || `${post.brand} ${post.aidAction || "relief"}`)}
                      className="inline-flex items-center gap-1 text-zinc-500 hover:text-zinc-800 transition-colors"
                    >
                      <Sparkles className="size-3.5 text-amber-500" />
                      <span>Analyze in ML Engine</span>
                    </button>
                  )}
                </div>

                {/* Expandable Comments Drawer */}
                {isExpanded && (
                  <div className="mt-3 p-3.5 rounded-xl bg-zinc-50 border border-zinc-200/80 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-zinc-800">
                        Audience Comments &amp; Reactions
                      </span>
                      {/* Sentiment filter */}
                      <div className="flex gap-1 text-[11px]">
                        {["all", "positive", "neutral", "negative"].map((pol) => (
                          <button
                            key={pol}
                            onClick={() => setCommentPolarityFilter(pol)}
                            className={cn(
                              "px-2 py-0.5 rounded-md font-medium capitalize",
                              commentPolarityFilter === pol
                                ? "bg-violet-600 text-white"
                                : "bg-white text-zinc-600 border border-zinc-200"
                            )}
                          >
                            {pol}
                          </button>
                        ))}
                      </div>
                    </div>

                    {postComments.length === 0 ? (
                      <p className="text-xs text-zinc-400 italic py-2">
                        No individual comment texts available for this post in the sampled release.
                      </p>
                    ) : (
                      <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                        {postComments
                          .filter((c) => commentPolarityFilter === "all" || c.polarity === commentPolarityFilter)
                          .slice(0, 15)
                          .map((comm) => (
                            <div
                              key={comm.id}
                              className="bg-white p-2.5 rounded-lg border border-zinc-200/70 space-y-1 text-xs"
                            >
                              <div className="flex items-center justify-between">
                                <span className="font-semibold text-zinc-700">Comment #{comm.id}</span>
                                <div className="flex items-center gap-1.5">
                                  <EmotionBadge emotion={comm.emotion} />
                                  <PolarityBadge polarity={comm.polarity} />
                                </div>
                              </div>
                              <p className="text-zinc-600 text-xs">
                                {comm.text || `Public response during disaster recovery operations (${formatDate(comm.ts)})`}
                              </p>
                            </div>
                          ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}

