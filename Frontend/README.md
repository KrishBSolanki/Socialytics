# SocialPulse Brand Intelligence

# MASTER BUILD PROMPT — SOCIALPULSE
## Premium Social Media Brand Intelligence Frontend

Act as a Senior UI/UX Designer, Principal React Engineer and Frontend Architect. Build a complete, production-quality frontend for **SOCIALPULSE — Social Media Sentiment Analysis & Brand Perception Forecasting**.

This is a Semester 7 Data Science and Computing project intended to demonstrate industry-level engineering, modern frontend design, data visualization and intelligent social media analytics.

Your immediate responsibility is to build the **entire frontend first**. Do not implement the Python backend or ML pipeline in this phase. However, design the frontend architecture so it can seamlessly integrate with the future Python backend.

---

## 1. Product Vision

SOCIALPULSE is a social media intelligence platform that helps companies understand how audiences react to their social media communications, corporate campaigns and brand initiatives.

The application should allow users to:
- Monitor brand-related social media posts.
- Explore audience comments and interactions.
- Understand positive, negative and neutral sentiment.
- Identify emotions and recurring discussion topics.
- Compare brand and campaign performance.
- Visualize engagement and brand perception trends.
- Explore future sentiment forecasts once backend models become available.

The selected research dataset is the Zenodo CSR Brand Posts and Public Engagement Dataset (52 brands, X/Twitter, campaign-related communications).

Dataset source:
https://zenodo.org/records/22042887

Important: Inspect the actual dataset schema before making assumptions about available fields. Its selected release includes Turkish-language material. Preserve original text and language metadata. Never represent Turkish data as English or invent translations.

---

## 2. Mandatory Technology Stack

Use the following stack:

- React 19 with TypeScript.
- Vite for development and optimized builds.
- Tailwind CSS for styling.
- Framer Motion for premium animations and transitions.
- React Router for navigation.
- Recharts for charts and data visualizations.
- Lucide React for consistent icons.
- TanStack Query for asynchronous data management.
- Zustand for lightweight global application state.
- React Hook Form and Zod for forms and validation.

Use reusable components, modular architecture, strong TypeScript typing and clean separation of concerns.

Do not build a single oversized component.

---

## 3. Visual Identity — Extremely Important

Create an original, premium, Instagram-inspired social analytics interface.

The application must NOT resemble an ordinary college project dashboard or a generic Bootstrap admin panel.

### Design direction

Use:
- Instagram-inspired social feed aesthetics.
- Modern SaaS dashboard layouts.
- Beautiful typography and spacing.
- Rounded cards and subtle shadows.
- Carefully balanced gradients.
- Premium glass effects where appropriate.
- Minimal borders and elegant separators.
- Smooth micro-interactions.

### Colour palette

Build a cohesive visual system around:

Primary background (dark): #0B1020  
Secondary background: #11182A  
Card background: #161F33  
Primary accent: #8B5CF6  
Secondary accent: #EC4899  
Highlight: #FB7185  
Information accent: #22D3EE  
Success: #34D399  
Warning: #FBBF24  
Main text: #F8FAFC  
Secondary text: #94A3B8  

Use restrained violet-to-pink gradients for important highlights, brand identity and selected interactive states.

Implement both:
- Premium dark mode (default).
- Clean light mode.

Provide a functioning theme toggle.

### Typography

Use Inter or Geist.

Create a clear hierarchy with:
- Strong page headings.
- Readable analytical labels.
- Compact chart annotations.
- Consistent font weights.

---

## 4. Application Layout

### Sidebar navigation

Build a beautiful collapsible sidebar with:

1. Overview
2. Social Feed
3. Brand Explorer
4. Campaign Analytics
5. Sentiment Intelligence
6. Emotion Analysis
7. Audience Insights
8. Forecasting
9. Data Explorer
10. Settings

Include:
- Custom SOCIALPULSE logo.
- Navigation icons.
- Active route indicator.
- Collapsed and expanded states.
- Tooltips.
- Smooth navigation animations.

### Top navigation bar

Include:
- Dynamic page title and breadcrumbs.
- Global search.
- Notification icon.
- Dataset status indicator.
- Theme toggle.
- User profile menu.

Make the overall layout responsive, with an elegant mobile navigation drawer.

---

## 5. Build These Core Screens

### A. Overview Dashboard

Create a premium executive analytics dashboard.

Display KPI cards for:
- Total brands monitored.
- Total social posts.
- Total audience comments.
- Average engagement.
- Positive sentiment percentage.
- Negative sentiment percentage.

Include:
- Sentiment distribution doughnut chart.
- Sentiment trend line chart.
- Brand comparison bar chart.
- Campaign engagement chart.
- Emotion distribution chart.
- Recent social media activity.
- Top-performing brands.
- Latest audience reactions.

Every KPI and chart must be connected to the frontend data layer.

Show genuine API values when available. In demo mode, clearly identify illustrative fixture data instead of presenting it as measured research results.

### B. Social Feed — Instagram-inspired experience

This screen is particularly important.

Build a visually engaging feed with individual post cards.

Each card should support:
- Brand avatar and brand name.
- Platform indicator.
- Campaign or post content.
- Original publication timestamp.
- Likes, comments, shares and available engagement metrics.
- Sentiment indicator.
- Emotion tags when available.
- Expandable comments section.
- View details interaction.

Add:
- Grid and list views.
- Search posts.
- Filter by brand.
- Filter by sentiment.
- Filter by campaign.
- Sort by date and engagement.
- Pagination or efficient infinite loading.

Make the feed feel like a modern social media product, not a plain table.

### C. Brand Explorer

Create a brand discovery interface.

Display brands as attractive cards containing:
- Brand identity.
- Total posts.
- Engagement metrics.
- Sentiment distribution.
- Recent activity.
- Brand perception indicator.

On selecting a brand, open a dedicated brand profile with:
- Brand overview.
- Campaign history.
- Sentiment timeline.
- Engagement patterns.
- Most discussed topics.
- Representative audience comments.

### D. Campaign Analytics

Build a dedicated campaign analysis screen.

Include:
- Campaign comparison.
- Campaign engagement trends.
- Positive/negative sentiment comparison.
- Emotion distribution.
- Audience reaction summaries.
- Campaign performance timeline.

Allow users to compare multiple campaigns interactively.

### E. Sentiment Intelligence

Create an analytical workspace featuring:
- Positive, negative and neutral sentiment.
- Sentiment trend over time.
- Brand-wise sentiment comparison.
- Campaign-wise sentiment breakdown.
- Sentiment changes over selected periods.
- Representative comments for each sentiment.

### F. Emotion Analysis

Create an emotion intelligence screen.

Visualize available emotion categories using:
- Interactive charts.
- Emotion distribution.
- Brand-wise emotion comparison.
- Campaign-wise emotional responses.
- Comment-level emotion exploration.

Only display emotion categories actually supported by the dataset or future backend response.

### G. Audience Insights

Provide:
- Comment frequency.
- Engagement patterns.
- Most discussed topics.
- Frequently occurring terms.
- Brand-related discussion comparisons.
- Positive and negative topic clusters.

Clearly distinguish observed audience reactions from inferred demographic information. Never invent audience demographics.

### H. Forecasting

Build a sophisticated forecasting interface ready for future ML integration.

Include UI sections for:
- Historical sentiment trends.
- Predicted sentiment trends.
- Forecast confidence intervals.
- Next 7-day prediction.
- Long-term trend visualization.
- Brand perception changes.
- Forecast model performance.

Display suitable empty states until actual predictions are provided by the backend. Never generate fake predictions that appear scientifically valid.

### I. Data Explorer

Create an interactive data examination workspace.

Include:
- Dataset overview.
- Record counts.
- Available columns.
- Data preview table.
- Search and filtering.
- Missing-value indicators.
- Date range filtering.
- Data source information.
- Export controls for supported formats.

---

## 6. Animations and Interaction Quality

Use Framer Motion intelligently.

Implement:
- Smooth page transitions.
- Sidebar expansion animations.
- Card hover effects.
- Animated KPI counters.
- Chart entry animations.
- Modal transitions.
- Dropdown animations.
- Skeleton loading states.
- Subtle gradient movement.
- Animated active navigation indicators.

Avoid excessive animations that harm performance.

Prioritize 60 FPS interactions and reduced-motion accessibility.

---

## 7. Data Architecture and Backend Readiness

Build a dedicated API integration layer.

Suggested architecture:

src/
  app/
  components/
    common/
    layout/
    dashboard/
    social-feed/
    analytics/
    charts/
  pages/
  hooks/
  services/
    api/
    brand.service.ts
    post.service.ts
    analytics.service.ts
    sentiment.service.ts
    forecast.service.ts
  store/
  types/
  utils/
  data/
    demo/
  assets/

Create strongly typed interfaces for:
- Brand
- SocialPost
- Comment
- Campaign
- EngagementMetrics
- SentimentResult
- EmotionResult
- ForecastResult

Centralize API configuration using environment variables.

Example:

VITE_API_BASE_URL=http://localhost:8000/api/v1

Use a service abstraction so demo fixtures can later be replaced by actual backend responses without rewriting the UI.

Include:
- Loading states.
- Empty states.
- Error handling.
- Retry mechanisms.
- Pagination.
- Request cancellation where appropriate.

Do not hardcode API responses inside page components.

---

## 8. Functional Requirements

Every visible interaction must work.

Implement:
- Routing.
- Sidebar navigation.
- Global search.
- Theme switching.
- Filter combinations.
- Sorting.
- Date selection.
- Interactive chart tooltips.
- Expandable post comments.
- Brand profile navigation.
- Campaign comparison.
- Data table pagination.
- Working settings controls.
- Export actions where meaningful.

Do not leave decorative buttons that do nothing.

Use deterministic demo fixtures only where backend connectivity is not yet available, and visibly distinguish demo mode from actual dataset mode.

---

## 9. Quality and Performance

The application must:
- Work on desktop, tablet and mobile.
- Maintain consistent responsive layouts.
- Avoid unnecessary component re-renders.
- Lazy-load page modules where practical.
- Optimize chart rendering.
- Use reusable design tokens.
- Maintain accessible contrast.
- Support keyboard navigation.
- Have no TypeScript errors.
- Have no browser console errors.

Do not compromise application functionality for visual effects.

---

## 10. Final Execution Instructions

Follow this execution sequence:

1. Inspect the existing repository and preserve useful existing configurations.
2. Establish the frontend architecture.
3. Implement the design system and application shell.
4. Build the responsive sidebar and top navigation.
5. Build all nine application screens.
6. Implement reusable chart, card, table and feed components.
7. Connect all screens to the centralized demo/API data layer.
8. Implement animations, loading states, filters and interactions.
9. Test all navigation routes and user interactions.
10. Run the production build and resolve all errors.

Do not stop after creating a dashboard mockup.

Do not provide just a design proposal or code snippets. Actually implement the complete frontend in the working repository.

At completion, provide:
- Implemented screens.
- Project folder structure.
- Installed dependencies.
- Features implemented.
- Commands to run locally.
- Any remaining frontend limitations.
- Backend integration requirements.

### FINAL DESIGN EXPECTATION

SOCIALPULSE must look and feel like a premium commercial social media intelligence SaaS platform.

Its defining visual character should be:

**Instagram-inspired social feed + premium SaaS analytics + smooth modern interactions + powerful data visualization.**

Prioritize visual excellence, functional completeness, clean architecture and future backend compatibility.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/9e9c8649-c6c2-56ea-b3ff-29ed69213d1e).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
