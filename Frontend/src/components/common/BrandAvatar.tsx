import { cn } from "@/lib/utils";
import { hashHue, initials } from "@/utils/format";

const PAIRS = [
  ["var(--violet)", "var(--pink)"],
  ["var(--pink)", "var(--rose)"],
  ["var(--info)", "var(--violet)"],
  ["var(--success)", "var(--info)"],
  ["var(--warning)", "var(--rose)"],
  ["var(--rose)", "var(--violet)"],
] as const;

/** Instagram-style ring avatar. Brand logos aren't in the dataset, so initials are used. */
export function BrandAvatar({ name, size = "md", ring = true }: { name: string; size?: "sm" | "md" | "lg" | "xl"; ring?: boolean }) {
  const [a, b] = PAIRS[hashHue(name) % PAIRS.length]!;
  const dim = { sm: "size-8 text-[11px]", md: "size-10 text-xs", lg: "size-14 text-base", xl: "size-20 text-xl" }[size];
  return (
    <span className={cn("relative inline-grid shrink-0 place-items-center rounded-full p-[2px]", ring && "bg-gradient-brand")}>
      <span className="grid place-items-center rounded-full bg-card p-[2px]">
        <span
          className={cn("grid place-items-center rounded-full font-bold text-primary-foreground", dim)}
          style={{ backgroundImage: `linear-gradient(135deg, ${a}, ${b})` }}
          aria-hidden
        >
          {initials(name)}
        </span>
      </span>
    </span>
  );
}
