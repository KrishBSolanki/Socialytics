import { motion } from "framer-motion";
import type { LucideIcon } from "lucide-react";
import { AnimatedNumber } from "./AnimatedNumber";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

interface KpiCardProps {
  label: string;
  value: number | undefined;
  format: (n: number) => string;
  icon: LucideIcon;
  hint?: string;
  tone?: "violet" | "pink" | "info" | "success" | "rose" | "warning";
  index?: number;
}

const toneClass: Record<NonNullable<KpiCardProps["tone"]>, string> = {
  violet: "text-violet bg-violet/12",
  pink: "text-pink bg-pink/12",
  info: "text-info bg-info/12",
  success: "text-success bg-success/12",
  rose: "text-rose bg-rose/12",
  warning: "text-warning bg-warning/12",
};

export function KpiCard({ label, value, format, icon: Icon, hint, tone = "violet", index = 0 }: KpiCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      whileHover={{ y: -3 }}
      className="group relative overflow-hidden rounded-2xl border border-border bg-card p-4 shadow-card transition-shadow hover:shadow-lift"
    >
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-brand opacity-0 transition-opacity group-hover:opacity-100" />
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground">{label}</span>
        <span className={cn("grid size-8 place-items-center rounded-lg", toneClass[tone])}>
          <Icon className="size-4" />
        </span>
      </div>
      <div className="mt-3 text-2xl font-bold tracking-tight tabular-nums">
        {value === undefined ? <Skeleton className="h-8 w-24" /> : <AnimatedNumber value={value} format={format} />}
      </div>
      {hint && <p className="mt-1 text-[11px] text-muted-foreground">{hint}</p>}
    </motion.div>
  );
}
