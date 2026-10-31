import React, { useEffect, useState } from "react";
import {
  CheckCircle2,
  Database,
  Download,
  History,
  Loader2,
  RefreshCw,
  Search,
  Trash2,
} from "lucide-react";
import { sentimentService } from "@/services/sentiment.service";
import { cn } from "@/lib/utils";

export function HistoryView() {
  const [historyData, setHistoryData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sentimentFilter, setSentimentFilter] = useState("all");

  const loadHistory = () => {
    setLoading(true);
    sentimentService
      .getHistory(150)
      .then((res) => {
        setHistoryData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.warn("Could not load prediction history:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleClear = async () => {
    if (!confirm("Are you sure you want to clear all prediction history records in the SQLite database?")) return;
    try {
      await sentimentService.clearHistory();
      loadHistory();
    } catch (e) {
      console.error("Clear error:", e);
    }
  };

  const records: any[] = historyData?.records || [];
  const filtered = records.filter((r) => {
    if (sentimentFilter !== "all" && r.predicted_sentiment !== sentimentFilter) return false;
    if (search.trim()) {
      return (r.raw_text || "").toLowerCase().includes(search.toLowerCase());
    }
    return true;
  });

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">SQLite Prediction History</h1>
          <p className="text-xs text-zinc-500 mt-1">
            Audit log of all real-time single and batch predictions recorded in <code className="text-violet-600">database/sentiment.db</code>.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadHistory}
            className="p-2 rounded-xl border border-zinc-200 text-zinc-600 hover:bg-zinc-50"
            title="Refresh history"
          >
            <RefreshCw className="size-4" />
          </button>
          <button
            onClick={handleClear}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-rose-200 text-rose-600 bg-rose-50 hover:bg-rose-100 text-xs font-semibold"
          >
            <Trash2 className="size-3.5" />
            <span>Clear History</span>
          </button>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-3.5 rounded-2xl bg-zinc-50 border border-zinc-200/80">
          <span className="text-[11px] text-zinc-400 block font-bold uppercase">Total Logged</span>
          <span className="text-xl font-bold text-zinc-900 mt-1 block">
            {historyData?.stats?.total ?? records.length}
          </span>
        </div>
        <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200">
          <span className="text-[11px] text-emerald-600 block font-bold uppercase">Positive</span>
          <span className="text-xl font-bold text-emerald-700 mt-1 block">
            {historyData?.stats?.positive ?? 0}
          </span>
        </div>
        <div className="p-3.5 rounded-2xl bg-indigo-50 border border-indigo-200">
          <span className="text-[11px] text-indigo-600 block font-bold uppercase">Neutral</span>
          <span className="text-xl font-bold text-indigo-700 mt-1 block">
            {historyData?.stats?.neutral ?? 0}
          </span>
        </div>
        <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200">
          <span className="text-[11px] text-rose-600 block font-bold uppercase">Negative</span>
          <span className="text-xl font-bold text-rose-700 mt-1 block">
            {historyData?.stats?.negative ?? 0}
          </span>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative w-64 sm:w-80">
          <Search className="absolute left-3 top-2.5 size-3.5 text-zinc-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search prediction texts..."
            className="w-full bg-zinc-50 border border-zinc-200 rounded-xl pl-9 pr-3 py-1.5 text-xs text-zinc-800 focus:outline-none focus:border-violet-500"
          />
        </div>

        <div className="flex bg-zinc-100 p-1 rounded-xl text-xs font-semibold">
          {["all", "Positive", "Neutral", "Negative"].map((s) => (
            <button
              key={s}
              onClick={() => setSentimentFilter(s)}
              className={cn(
                "px-3 py-1 rounded-lg capitalize transition-all",
                sentimentFilter === s
                  ? "bg-[#6047B5] text-white shadow-sm"
                  : "text-zinc-600 hover:text-zinc-900"
              )}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* History Table */}
      <div className="border border-zinc-200 rounded-xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="h-48 flex items-center justify-center text-zinc-400 gap-2">
            <Loader2 className="size-4 animate-spin text-violet-600" />
            <span className="text-xs">Fetching records from SQLite...</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-zinc-400 space-y-1">
            <Database className="size-8 mx-auto text-zinc-300 mb-2" />
            <p className="text-xs font-semibold text-zinc-600">No prediction records found</p>
            <p className="text-[11px]">Run a single or bulk analysis to log records into the SQLite database.</p>
          </div>
        ) : (
          <div className="overflow-x-auto max-h-[480px]">
            <table className="w-full text-left text-xs">
              <thead className="bg-zinc-50 text-zinc-500 font-semibold border-b border-zinc-200 sticky top-0 z-10">
                <tr>
                  <th className="p-3">ID</th>
                  <th className="p-3">Raw Comment Text</th>
                  <th className="p-3">Predicted Sentiment</th>
                  <th className="p-3">Confidence</th>
                  <th className="p-3">Source</th>
                  <th className="p-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {filtered.map((r) => (
                  <tr key={r.id} className="hover:bg-zinc-50/50">
                    <td className="p-3 font-mono text-zinc-400">#{r.id}</td>
                    <td className="p-3 text-zinc-800 max-w-md truncate font-medium">
                      {r.raw_text}
                    </td>
                    <td className="p-3">
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded-full text-[10px] font-bold",
                          r.predicted_sentiment === "Positive"
                            ? "bg-emerald-100 text-emerald-700"
                            : r.predicted_sentiment === "Negative"
                            ? "bg-rose-100 text-rose-700"
                            : "bg-indigo-100 text-indigo-700"
                        )}
                      >
                        {r.predicted_sentiment}
                      </span>
                    </td>
                    <td className="p-3 font-semibold text-zinc-700 tabular-nums">
                      {((Number(r.confidence) || 0) * 100).toFixed(1)}%
                    </td>
                    <td className="p-3 text-zinc-400 font-mono text-[11px]">{r.source}</td>
                    <td className="p-3 text-zinc-400 text-[11px] whitespace-nowrap">
                      {r.created_at}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

