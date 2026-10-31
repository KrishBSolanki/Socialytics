import { CalendarRange } from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { fmtDateShort } from "@/utils/format";

export interface DateRange {
  from?: string;
  to?: string;
}

/** Presets follow the dataset's own disaster_period coding. */
export const PERIOD_PRESETS: { label: string; range: DateRange }[] = [
  { label: "Full coverage", range: {} },
  { label: "Before the earthquake", range: { from: "2023-01-01", to: "2023-02-05" } },
  { label: "Emergency relief", range: { from: "2023-02-06", to: "2023-03-05" } },
  { label: "Early recovery", range: { from: "2023-03-06", to: "2023-03-31" } },
];

export function rangeLabel(r: DateRange) {
  const preset = PERIOD_PRESETS.find((p) => p.range.from === r.from && p.range.to === r.to);
  if (preset) return preset.label;
  return `${r.from ? fmtDateShort(r.from) : "Start"} – ${r.to ? fmtDateShort(r.to) : "End"}`;
}

export function DateRangeFilter({ value, onChange }: { value: DateRange; onChange: (r: DateRange) => void }) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" aria-label="Choose date range">
          <CalendarRange /> {rangeLabel(value)}
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-72 space-y-4">
        <div className="space-y-1">
          {PERIOD_PRESETS.map((p) => (
            <button
              key={p.label}
              type="button"
              onClick={() => onChange(p.range)}
              className="flex w-full items-center justify-between rounded-md px-2 py-1.5 text-left text-sm hover:bg-accent data-[active=true]:bg-accent data-[active=true]:text-accent-foreground"
              data-active={p.range.from === value.from && p.range.to === value.to}
            >
              {p.label}
            </button>
          ))}
        </div>
        <div className="grid grid-cols-2 gap-2 border-t border-border pt-3">
          <div className="space-y-1">
            <Label htmlFor="dr-from" className="text-xs">From</Label>
            <Input id="dr-from" type="date" min="2023-01-01" max="2023-03-31" value={value.from ?? ""} onChange={(e) => onChange({ ...value, from: e.target.value || undefined })} />
          </div>
          <div className="space-y-1">
            <Label htmlFor="dr-to" className="text-xs">To</Label>
            <Input id="dr-to" type="date" min="2023-01-01" max="2023-03-31" value={value.to ?? ""} onChange={(e) => onChange({ ...value, to: e.target.value || undefined })} />
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
