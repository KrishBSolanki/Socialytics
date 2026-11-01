import { createFileRoute } from "@tanstack/react-router";
import { SocialPulseShell } from "@/components/socialpulse/SocialPulseShell";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SocialPulse - Social Media Sentiment & Brand Perception Intelligence" },
      { property: "og:title", content: "SocialPulse - Brand Perception Intelligence" },
    ],
  }),
  component: Index,
});

function Index() {
  return <SocialPulseShell />;
}
