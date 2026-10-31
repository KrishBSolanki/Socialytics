import { AlertTriangle, Inbox, RefreshCw } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

export function ChartSkeleton({ height = 260 }: { height?: number }) {
  return (
    <div className="flex w-full items-end gap-2" style={{ height }} aria-busy="true" aria-label="Loading chart">
      {Array.from({ length: 14 }).map((_, i) => (
        <Skeleton key={i} className="flex-1 rounded-md" style={{ height: `${30 + ((i * 37) % 60)}%` }} />
      ))}
    </div>
  );
}

export function ListSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3" aria-busy="true">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center gap-3">
          <Skeleton className="size-9 rounded-full" />
          <div className="flex-1 space-y-1.5">
            <Skeleton className="h-3 w-2/5" />
            <Skeleton className="h-3 w-3/5" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function EmptyState({
  icon: Icon = Inbox,
  title,
  description,
  action,
  className,
}: {
  icon?: LucideIcon;
  title: string;
  description?: ReactNode;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex flex-col items-center justify-center px-6 py-10 text-center", className)}>
      <div className="relative mb-4 grid size-14 place-items-center rounded-2xl bg-gradient-brand-soft ring-1 ring-border">
        <Icon className="size-6 text-primary" />
      </div>
      <h3 className="text-sm font-semibold">{title}</h3>
      {description && <p className="mt-1.5 max-w-md text-xs leading-relaxed text-muted-foreground">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

export function ErrorState({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  return (
    <EmptyState
      icon={AlertTriangle}
      title="Couldn't load this data"
      description={error instanceof Error ? error.message : String(error)}
      action={
        onRetry && (
          <Button variant="outline" size="sm" onClick={onRetry}>
            <RefreshCw /> Try again
          </Button>
        )
      }
    />
  );
}

/** Renders skeleton / error / empty / content for a query. */
export function QueryState<T>({
  query,
  skeleton = <ChartSkeleton />,
  isEmpty,
  empty,
  children,
}: {
  query: { data: T | undefined; isPending: boolean; isError: boolean; error: unknown; refetch: () => unknown };
  skeleton?: ReactNode;
  isEmpty?: (d: T) => boolean;
  empty?: ReactNode;
  children: (data: T) => ReactNode;
}) {
  if (query.isError && query.data === undefined) return <ErrorState error={query.error} onRetry={() => query.refetch()} />;
  if (query.isPending || query.data === undefined) return <>{skeleton}</>;
  if (isEmpty?.(query.data)) return <>{empty ?? <EmptyState title="Nothing to show" description="Try widening your filters." />}</>;
  return <>{children(query.data)}</>;
}
