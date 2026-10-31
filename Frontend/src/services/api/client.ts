import { API_CONFIG } from "./config";
import { useAppStore } from "@/store/app-store";

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type Params = Record<string, string | number | boolean | undefined | null>;

/** Typed GET against the configured backend with timeout and cancellation. */
export async function apiGet<T>(path: string, params?: Params, signal?: AbortSignal): Promise<T> {
  const base = useAppStore.getState().apiBaseUrl || API_CONFIG.baseUrl;
  const url = new URL(base.replace(/\/$/, "") + path);
  Object.entries(params ?? {}).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, String(v));
  });
  const timeout = AbortSignal.timeout(API_CONFIG.timeoutMs);
  const combined = signal ? AbortSignal.any([signal, timeout]) : timeout;
  let res: Response;
  try {
    res = await fetch(url, { signal: combined, headers: { Accept: "application/json" } });
  } catch (e) {
    if ((e as Error).name === "AbortError") throw e;
    throw new ApiError(`Could not reach the backend at ${base}. Is it running?`);
  }
  if (!res.ok) throw new ApiError(`Backend responded with ${res.status} for ${path}`, res.status);
  return (await res.json()) as T;
}

/** Fetch a static JSON file bundled with the app (the dataset snapshot). */
export async function staticGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  const res = await fetch(path, { signal });
  if (!res.ok) throw new ApiError(`Could not load ${path} (${res.status})`, res.status);
  return (await res.json()) as T;
}

export const isApiMode = () => useAppStore.getState().dataSource === "api";

/** Typed POST against the configured backend with timeout and cancellation. */
export async function apiPost<T>(path: string, body: unknown, signal?: AbortSignal): Promise<T> {
  const base = useAppStore.getState().apiBaseUrl || API_CONFIG.baseUrl;
  const url = new URL(base.replace(/\/$/, "") + path);
  const timeout = AbortSignal.timeout(API_CONFIG.timeoutMs);
  const combined = signal ? AbortSignal.any([signal, timeout]) : timeout;
  let res: Response;
  try {
    res = await fetch(url, {
      method: "POST",
      signal: combined,
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(body),
    });
  } catch (e) {
    if ((e as Error).name === "AbortError") throw e;
    throw new ApiError(`Could not reach the backend at ${base}. Is it running?`);
  }
  if (!res.ok) {
    const errorText = await res.text().catch(() => "");
    throw new ApiError(`Backend error (${res.status}): ${errorText || res.statusText}`, res.status);
  }
  return (await res.json()) as T;
}

/** Form data / file upload POST against configured backend. */
export async function apiPostForm<T>(path: string, formData: FormData, signal?: AbortSignal): Promise<T> {
  const base = useAppStore.getState().apiBaseUrl || API_CONFIG.baseUrl;
  const url = new URL(base.replace(/\/$/, "") + path);
  const timeout = AbortSignal.timeout(60_000); // 60s timeout for bulk uploads
  const combined = signal ? AbortSignal.any([signal, timeout]) : timeout;
  let res: Response;
  try {
    res = await fetch(url, {
      method: "POST",
      signal: combined,
      headers: { Accept: "application/json" },
      body: formData,
    });
  } catch (e) {
    if ((e as Error).name === "AbortError") throw e;
    throw new ApiError(`Could not reach the backend at ${base}. Is it running?`);
  }
  if (!res.ok) {
    const errorText = await res.text().catch(() => "");
    throw new ApiError(`Backend error (${res.status}): ${errorText || res.statusText}`, res.status);
  }
  return (await res.json()) as T;
}
