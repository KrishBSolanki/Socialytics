import { createFileRoute } from "@tanstack/react-router";
import { SocialPulseShell } from "@/components/socialpulse/SocialPulseShell";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return <SocialPulseShell />;
}
