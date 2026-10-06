# DATA Schema Reference

This document describes the JSON structure that the `template.html` dashboard expects.
The SKILL.md orchestration instructions generate this structure from query results.

## Top-Level Structure

```typescript
interface DashboardData {
  meta: Meta;
  kpis: KPIs;
  channels: Channel[];
  segmentHeatmap: SegmentRow[];
  journeys: JourneyData;
}
```

## Meta
```typescript
interface Meta {
  company: string;       // Display name, e.g. "Northstar Home Living"
  database: string;      // TD database name
  generatedAt: string;   // ISO date: "2026-10-06"
  dataRange: {
    from: string;        // "2026-08-13" or "All time"
    to: string;
  };
}
```

## KPIs (Overview tab)
```typescript
interface KPIs {
  totalSpend: number;       // Sum across all channels
  totalRevenue: number;
  avgRoas: number;          // totalRevenue / totalSpend
  activeCampaigns: number;  // Count distinct campaigns
  totalCustomers: number;   // From customer/master table
  avgConvRate: number;      // Weighted average %
}
```

## Channels (one per discovered channel)
```typescript
interface Channel {
  name: string;        // Raw value: "email", "sms", "push", "in_app", "paid_social", etc.
  label: string;       // Display: "Email", "SMS", "Push", "In-App", "Paid Social"
  role: string;        // "Retention", "Discovery", "Intent Capture", etc.
  color: string;       // Hex color for charts
  spend: number;       // Total spend for this channel
  revenue: number;     // Total revenue attributed
  roas: number;        // revenue / spend

  nativeKpis: NativeKPI[];     // Exactly 3 items — pills 4-6 in the channel tab
  campaigns: CampaignRow[];    // Campaign-level detail rows
  columns: string[];           // Column headers for campaign table
  columnFormats: string[];     // Format per column: "$", "%", "x", "#", ""
  roasBySegment: SegmentROAS[]; // For the bar chart
  insight: string;             // One-sentence insight
}

interface NativeKPI {
  label: string;    // "Open Rate", "Total Sends", etc.
  value: number;
  format: string;   // "%", "$", "x", "#"
}

interface CampaignRow {
  name: string;          // Campaign name
  segment: string;       // Segment name or "All"
  revenue: number;
  roas: number;
  metrics: number[];     // Values for columns[4..N] in order
}

interface SegmentROAS {
  segment: string;
  value: number;   // ROAS value
}
```

## Segment Heatmap
```typescript
interface SegmentRow {
  segment: string;
  values: Record<string, number>;  // { channel_name: roas_value }
}
```
Channel keys must match `channels[i].name`.

## Journey Data
```typescript
interface JourneyData {
  kpis: JourneyKPIs;
  cards: JourneyCard[];
  crossJourney: CrossJourney;
  optimizations: Optimization[];
}

interface JourneyKPIs {
  totalEnrolled: number;
  goalAchieved: number;
  goalAchievedPct: number;
  revenueAttributed: number;
  stage1Conversion: number;   // %
  stage2Escalation: number;   // %
  avgDaysToConvert: number;
}

interface JourneyCard {
  name: string;
  segment: string;
  segmentSize: number;
  overallConversion: number;   // %
  channelBadge: string;
  funnel: FunnelStep[];        // 5 steps
  stageBreakdown: StageRow[];  // 3 stages
  decisions: Decision[];       // 2 decision points
  revenueByStage: RevenueStage[];
}

interface FunnelStep {
  stage: string;   // "Entered", "Stage 1 Active", etc.
  count: number;
  pct: number;     // % of original entries
}

interface StageRow {
  stage: string;
  entered: number;
  converted: number;
  rate: number;     // %
  roas: number;
  channel: string;
}

interface Decision {
  name: string;
  qualifyPct: number;   // % who qualify
  qualifyConv: number;  // Conversion % for qualified
  fallbackConv: number; // Conversion % for non-qualified
}

interface RevenueStage {
  stage: string;
  revenue: number;
  pct: number;   // % of total journey revenue
}

interface CrossJourney {
  stage1Coverage: number;
  blendedRoas: number;
  stage3RescueValue: number;
  purchaseWindowGap: {
    avgDaysToRepurchase: number;
    journeyWindow: number;
  };
}

interface Optimization {
  title: string;
  estRevenue: number;
  description: string;
  priority: "high" | "medium" | "low";
}
```
