import React, { useState } from "react";
import { Database, Download, ExternalLink, FileSpreadsheet, Filter, Search } from "lucide-react";
import { formatCompact, formatDate } from "@/utils/format";

interface DatasetExplorerViewProps {
  posts: any[];
  meta: any;
}

export function DatasetExplorerView({ posts, meta }: DatasetExplorerViewProps) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const pageSize = 15;

  const filtered = posts.filter((p) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      p.brand.toLowerCase().includes(q) ||
      p.industry.toLowerCase().includes(q) ||
      (p.aidAction && p.aidAction.toLowerCase().includes(q))
    );
  });

  const totalPages = Math.ceil(filtered.length / pageSize) || 1;
  const currentItems = filtered.slice((page - 1) * pageSize, page * pageSize);

  const handleExportCSV = () => {
    const headers = [
      "Tweet ID",
      "Brand",
      "Industry",
      "Nationality",
      "Followers",
      "Likes",
      "Comments",
      "Retweets",
      "Post Type",
      "Aid Action",
      "Relief Effect",
      "Timestamp",
    ];
    const rows = filtered.map((p) => [
      p.id,
      `"${p.brand}"`,
      `"${p.industry}"`,
      p.nationality,
      p.followers,
      p.likes || 0,
      p.comments || 0,
      p.retweets || 0,
      `"${p.postType}"`,
      `"${p.aidAction || ""}"`,
      `"${p.reliefEffect}"`,
      p.ts,
    ]);

    const csvContent =
      "data:text/csv;charset=utf-8," +
      [headers.join(","), ...rows.map((e) => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "socialpulse_zenodo_dataset.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Dataset Explorer &amp; Metadata</h1>
          <p className="text-xs text-zinc-500 mt-1">
            Zenodo Record 22042887: CSR Brand Posts &amp; Public Engagement during Türkiye Earthquakes.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-bold hover:bg-zinc-800 transition-colors shadow-sm"
        >
          <Download className="size-3.5" />
          <span>Export Filtered CSV</span>
        </button>
      </div>

      {/* Dataset Metadata Box */}
      <div className="p-5 rounded-2xl bg-zinc-50 border border-zinc-200/80 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-sm text-zinc-800">
            <FileSpreadsheet className="size-4 text-violet-600" />
            <span>{meta?.title || "CSR Brand Posts Dataset"}</span>
          </div>
          <a
            href={meta?.url || "https://zenodo.org/records/22042887"}
            target="_blank"
            rel="noreferrer"
            className="text-xs text-violet-700 hover:underline flex items-center gap-1 font-semibold"
          >
            <span>Zenodo Record</span>
            <ExternalLink className="size-3" />
          </a>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 text-xs">
          <div>
            <span className="text-zinc-400 block">Digital Object Identifier (DOI)</span>
            <span className="font-semibold text-zinc-700">{meta?.doi || "10.5281/zenodo.22042887"}</span>
          </div>
          <div>
            <span className="text-zinc-400 block">License</span>
            <span className="font-semibold text-zinc-700">{meta?.license || "CC BY 4.0"}</span>
          </div>
          <div>
            <span className="text-zinc-400 block">Total Post Observations</span>
            <span className="font-semibold text-zinc-700 tabular-nums">
              {posts.length.toLocaleString()} rows
            </span>
          </div>
          <div>
            <span className="text-zinc-400 block">Date Coverage</span>
            <span className="font-semibold text-zinc-700">
              {meta?.coverage?.start || "2023-01-01"} to {meta?.coverage?.end || "2023-03-30"}
            </span>
          </div>
        </div>
      </div>

      {/* Search Toolbar */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative w-64 sm:w-80">
          <Search className="absolute left-3 top-2.5 size-3.5 text-zinc-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search brand, industry or action type..."
            className="w-full bg-zinc-50 border border-zinc-200 rounded-xl pl-9 pr-3 py-1.5 text-xs text-zinc-800 focus:outline-none focus:border-violet-500"
          />
        </div>

        <span className="text-xs text-zinc-500 font-medium">
          Showing {currentItems.length} of {filtered.length} matching rows
        </span>
      </div>

      {/* Data Table */}
      <div className="border border-zinc-200 rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-left text-xs">
            <thead className="bg-zinc-50 text-zinc-500 font-semibold border-b border-zinc-200 sticky top-0 z-10">
              <tr>
                <th className="p-3">Brand</th>
                <th className="p-3">Industry</th>
                <th className="p-3">Nationality</th>
                <th className="p-3">Followers</th>
                <th className="p-3">Likes</th>
                <th className="p-3">Comments</th>
                <th className="p-3">Post Type</th>
                <th className="p-3">Action Type</th>
                <th className="p-3">Relief Effect</th>
                <th className="p-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {currentItems.map((p) => (
                <tr key={p.id} className="hover:bg-zinc-50/50">
                  <td className="p-3 font-bold text-zinc-800">{p.brand}</td>
                  <td className="p-3 text-zinc-600">{p.industry}</td>
                  <td className="p-3 capitalize text-zinc-500">{p.nationality}</td>
                  <td className="p-3 font-medium text-zinc-700 tabular-nums">
                    {formatCompact(p.followers || 0)}
                  </td>
                  <td className="p-3 font-medium text-zinc-700 tabular-nums">{p.likes || 0}</td>
                  <td className="p-3 font-medium text-zinc-700 tabular-nums">{p.comments || 0}</td>
                  <td className="p-3 text-zinc-600">{p.postType}</td>
                  <td className="p-3 text-violet-700 font-medium">{p.aidAction || "—"}</td>
                  <td className="p-3 text-zinc-600">{p.reliefEffect}</td>
                  <td className="p-3 text-zinc-400 font-mono text-[11px] whitespace-nowrap">
                    {formatDate(p.ts)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-zinc-50 px-4 py-3 border-t border-zinc-200 flex items-center justify-between text-xs">
          <span className="text-zinc-500">
            Page {page} of {totalPages}
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="px-3 py-1 bg-white border border-zinc-200 rounded-lg text-zinc-700 disabled:opacity-40"
            >
              Previous
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="px-3 py-1 bg-white border border-zinc-200 rounded-lg text-zinc-700 disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

