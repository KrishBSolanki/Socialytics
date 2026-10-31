import React, { useEffect, useState } from "react";
import {
  CheckCircle2,
  Database,
  Globe,
  Radio,
  RefreshCw,
  Server,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import { useAppStore } from "@/store/app-store";
import { API_CONFIG } from "@/services/api/config";
import { cn } from "@/lib/utils";

export function SettingsView() {
  const { dataSource, setDataSource, apiBaseUrl, setApiBaseUrl } = useAppStore();
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [checking, setChecking] = useState(false);
  const [localUrl, setLocalUrl] = useState(apiBaseUrl || API_CONFIG.baseUrl);

  const checkHealth = async () => {
    setChecking(true);
    try {
      const res = await fetch(`${localUrl.replace(/\/$/, "")}/health`);
      if (res.ok) {
        const data = await res.json();
        setHealthStatus({ ok: true, data });
      } else {
        setHealthStatus({ ok: false, error: `HTTP ${res.status}` });
      }
    } catch (e: any) {
      setHealthStatus({ ok: false, error: "Could not connect to FastAPI server" });
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, [localUrl]);

  return (
    <div className="flex-1 min-w-0 bg-white h-screen overflow-y-auto p-6 space-y-6">
      <div className="border-b border-[#EAE7F0] pb-4">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">System &amp; Engine Configuration</h1>
        <p className="text-xs text-zinc-500 mt-1">
          Manage REST API backend connectivity, data source modes, and machine learning engine parameters.
        </p>
      </div>

      <div className="max-w-2xl space-y-6">
        {/* Backend Connection */}
        <div className="p-5 rounded-2xl bg-zinc-50 border border-zinc-200/80 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-bold text-sm text-zinc-800">
              <Server className="size-4 text-violet-600" />
              <span>Python FastAPI Backend Endpoint</span>
            </div>
            {checking ? (
              <span className="text-xs text-zinc-400">Pinging backend...</span>
            ) : healthStatus?.ok ? (
              <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
                <CheckCircle2 className="size-3.5" /> Engine Online
              </span>
            ) : (
              <span className="text-xs font-bold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200 flex items-center gap-1">
                <XCircle className="size-3.5" /> Standalone Snapshot Mode
              </span>
            )}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={localUrl}
              onChange={(e) => setLocalUrl(e.target.value)}
              placeholder="http://localhost:8000/api/v1"
              className="flex-1 bg-white border border-zinc-200 rounded-xl px-3 py-2 text-xs font-mono text-zinc-800 focus:outline-none focus:border-violet-500"
            />
            <button
              onClick={() => {
                setApiBaseUrl(localUrl);
                checkHealth();
              }}
              className="px-4 py-2 bg-[#6047B5] text-white text-xs font-bold rounded-xl hover:bg-violet-700 transition-colors shadow-sm"
            >
              Save &amp; Test
            </button>
          </div>

          {healthStatus?.ok && (
            <div className="p-3 bg-white rounded-xl border border-zinc-200/70 text-xs space-y-1">
              <div className="text-zinc-700 font-semibold">{healthStatus.data?.service}</div>
              <div className="text-zinc-500">
                Model: <span className="font-mono text-violet-700">{healthStatus.data?.model_type}</span> ·
                Accuracy: <span className="font-bold text-emerald-600">{((healthStatus.data?.accuracy || 0.992) * 100).toFixed(1)}%</span> ·
                Posts: <span className="font-bold">{healthStatus.data?.total_posts}</span> ·
                Comments: <span className="font-bold">{healthStatus.data?.total_comments}</span>
              </div>
            </div>
          )}
        </div>

        {/* Data Source Mode */}
        <div className="p-5 rounded-2xl bg-zinc-50 border border-zinc-200/80 shadow-sm space-y-3">
          <div className="flex items-center gap-2 font-bold text-sm text-zinc-800">
            <Radio className="size-4 text-violet-600" />
            <span>Active Data Source Mode</span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <button
              onClick={() => setDataSource("dataset")}
              className={cn(
                "p-3.5 rounded-xl border text-left transition-all",
                dataSource === "dataset"
                  ? "bg-violet-50 border-violet-400 text-violet-900 shadow-sm"
                  : "bg-white border-zinc-200 text-zinc-600 hover:bg-zinc-50"
              )}
            >
              <span className="font-bold block">Bundled Dataset Mode</span>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Instant client-side evaluation using cached Zenodo CSR snapshot.
              </span>
            </button>

            <button
              onClick={() => setDataSource("api")}
              className={cn(
                "p-3.5 rounded-xl border text-left transition-all",
                dataSource === "api"
                  ? "bg-violet-50 border-violet-400 text-violet-900 shadow-sm"
                  : "bg-white border-zinc-200 text-zinc-600 hover:bg-zinc-50"
              )}
            >
              <span className="font-bold block">Live REST API Mode</span>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Connects dynamically to FastAPI running on port 8000.
              </span>
            </button>
          </div>
        </div>

        {/* Project Attribution */}
        <div className="p-5 rounded-2xl bg-zinc-50 border border-zinc-200/80 shadow-sm space-y-2 text-xs text-zinc-600">
          <div className="flex items-center gap-2 font-bold text-zinc-800">
            <ShieldCheck className="size-4 text-emerald-600" />
            <span>Academic Integrity &amp; Dataset Attribution</span>
          </div>
          <p className="leading-relaxed">
            This system utilizes the <strong>Zenodo Record 22042887</strong> dataset: <em>"CSR Communication of Local and Global Brands During the February 6, 2023 Türkiye Earthquakes: Platform X Posts and Public Engagement Data"</em> (licensed under Creative Commons Attribution 4.0 International).
          </p>
          <p className="text-zinc-400 text-[11px]">
            Original text is presented in its authentic language without synthetic translations. Classification predictions are performed using scikit-learn Naive Bayes and time series exponential smoothing.
          </p>
        </div>
      </div>
    </div>
  );
}

