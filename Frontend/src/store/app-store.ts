import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { DataSourceMode } from "@/types";
import { API_CONFIG } from "@/services/api/config";

export type Theme = "dark" | "light";

interface AppState {
  theme: Theme;
  sidebarCollapsed: boolean;
  mobileNavOpen: boolean;
  searchOpen: boolean;
  dataSource: DataSourceMode;
  apiBaseUrl: string;
  reducedMotion: boolean;
  feedView: "grid" | "list";
  pageSize: number;
  readNotifications: string[];
  setTheme: (t: Theme) => void;
  toggleTheme: () => void;
  toggleSidebar: () => void;
  setMobileNavOpen: (v: boolean) => void;
  setSearchOpen: (v: boolean) => void;
  setDataSource: (m: DataSourceMode) => void;
  setApiBaseUrl: (u: string) => void;
  setReducedMotion: (v: boolean) => void;
  setFeedView: (v: "grid" | "list") => void;
  setPageSize: (n: number) => void;
  markNotificationsRead: (ids: string[]) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: "dark",
      sidebarCollapsed: false,
      mobileNavOpen: false,
      searchOpen: false,
      dataSource: "dataset",
      apiBaseUrl: API_CONFIG.baseUrl,
      reducedMotion: false,
      feedView: "grid",
      pageSize: 12,
      readNotifications: [],
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((s) => ({ theme: s.theme === "dark" ? "light" : "dark" })),
      toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
      setMobileNavOpen: (mobileNavOpen) => set({ mobileNavOpen }),
      setSearchOpen: (searchOpen) => set({ searchOpen }),
      setDataSource: (dataSource) => set({ dataSource }),
      setApiBaseUrl: (apiBaseUrl) => set({ apiBaseUrl }),
      setReducedMotion: (reducedMotion) => set({ reducedMotion }),
      setFeedView: (feedView) => set({ feedView }),
      setPageSize: (pageSize) => set({ pageSize }),
      markNotificationsRead: (ids) =>
        set((s) => ({ readNotifications: Array.from(new Set([...s.readNotifications, ...ids])) })),
    }),
    {
      name: "socialpulse-settings",
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
      partialize: (s) => ({
        theme: s.theme,
        sidebarCollapsed: s.sidebarCollapsed,
        dataSource: s.dataSource,
        apiBaseUrl: s.apiBaseUrl,
        reducedMotion: s.reducedMotion,
        feedView: s.feedView,
        pageSize: s.pageSize,
        readNotifications: s.readNotifications,
      }),
    },
  ),
);
