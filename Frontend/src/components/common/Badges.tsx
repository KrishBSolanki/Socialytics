import type { Emotion, Polarity } from "@/types";
import { EMOTION_META, POLARITY_META } from "@/utils/emotion";
import { cn } from "@/lib/utils";

export function EmotionBadge({ emotion, count, className }: { emotion: Emotion; count?: number; className?: string }) {
  const m = EMOTION_META[emotion];
  return (
    <span
      className={cn("inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-medium", className)}
      style={{ color: m.color, borderColor: `color-mix(in oklab, ${m.color} 35%, transparent)`, background: `color-mix(in oklab, ${m.color} 12%, transparent)` }}
    >
      <span aria-hidden>{m.emoji}</span>
      {m.label}
      {count !== undefined && <span className="opacity-70 tabular-nums">· {count}</span>}
    </span>
  );
}

export function PolarityBadge({ polarity, className }: { polarity: Polarity; className?: string }) {
  const m = POLARITY_META[polarity];
  return (
    <span
      className={cn("inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-[11px] font-semibold", className)}
      style={{ color: m.color, background: `color-mix(in oklab, ${m.color} 14%, transparent)` }}
    >
      <span className="size-1.5 rounded-full" style={{ background: m.color }} />
      {m.label}
    </span>
  );
}

export function Tag({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span className={cn("inline-flex items-center rounded-md bg-muted px-1.5 py-0.5 text-[11px] font-medium text-muted-foreground", className)}>
      {children}
    </span>
  );
}

export function DerivedNote({ children }: { children?: React.ReactNode }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-warning/30 bg-warning/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-warning">
      {children ?? "Emotion-derived"}
    </span>
  );
}
