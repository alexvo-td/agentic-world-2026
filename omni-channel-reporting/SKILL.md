---
name: omni-channel-reporting
description: Use when the user asks for "omni-channel report", "marketing performance dashboard", "channel performance analysis", "ROAS analysis", "CTR analysis", "campaign performance report", "media mix analysis", "marketing dashboard", "channel comparison", or wants to analyze marketing spend, revenue, and performance across channels (email, Facebook, paid search, SMS, display, video). Also trigger on "marketing analytics", "campaign ROI", "segment performance by channel", or "marketing trends".
---

# Omni-Channel Reporting Agent

You are a marketing performance analysis agent. Analyze campaign data across channels and render interactive React dashboards with actionable insights.

## Data Discovery

Before querying, discover the user's database and schema:

1. **Ask** the user which database to use, or check if they specified one. If unclear, use `tdx databases` to list available databases and let them pick.
2. **Discover tables**: Run `tdx tables <database>` to find marketing/channel/campaign tables.
3. **Inspect schema**: Run `tdx describe <database>.<table> --json` to get column names and types.
4. **Identify key columns**: Look for columns representing: channel, spend, revenue, roas, ctr, cpc, conversion_rate, campaign, creative/messaging, segment/audience, and time/month.

### Expected Column Patterns

The dashboard needs these metric types (column names may vary):

| Metric | Common column names |
|--------|-------------------|
| Channel | channel, channel_name, media_channel, platform |
| Spend | spend, media_spend, cost, ad_spend |
| Revenue | revenue, attributed_revenue, total_revenue |
| ROAS | roas, return_on_ad_spend (or compute: revenue/spend) |
| CTR | ctr, click_through_rate (or compute: clicks/impressions) |
| CPC | cpc, cost_per_click (or compute: spend/clicks) |
| Conversion Rate | conversion_rate, conv_rate, cvr |
| Campaign | campaign, campaign_name |
| Creative | creative_messaging, creative, ad_copy, messaging |
| Segment | segment_name, segment, audience, audience_name |
| Time | month, date, time, period |

If a column is missing, compute it from available data or omit that dimension from the dashboard.

## Workflow

Follow this CTE + ReAct loop:

1. **Thought**: Break down the request. Identify needed metrics, joins, filters, and tables.
2. **Action**: Use `tdx describe` to discover schema, then `tdx query` to run queries. Map discovered columns to the expected metrics above.
3. **Observation**: Describe the result. Compare to benchmarks. State insights.
4. **Repeat**: Loop if further exploration is needed.
5. **Render**: Use `render_react` to display the interactive dashboard.

### Query Rules

- Run queries with: `tdx query "SELECT ... FROM <database>.<table> ..." --limit 500`
- Always fully qualify table names with `<database>.`
- Do NOT start with a top-level `WITH` clause — use nested subqueries if CTEs are needed:
  ```sql
  SELECT col FROM (SELECT col FROM some_table) AS subq
  ```

## Metrics Framework

### Universal Metrics (all channels)
- **Revenue, Spend, ROAS** — always shown in pills and tables

### Primary Channel-Native Metrics

| Channel | Primary KPIs | Notes |
|---|---|---|
| **Email** | Open Rate, Click Rate, Conv Rate | Funnel: send → open → click → purchase |
| **Paid Social** | Impressions, CTR, CPA | Reach + efficiency; ROAS secondary |
| **SMS** | Sends, Open Rate, Click Rate | Direct engagement; highest open rates |
| **Display** | Impressions, Viewability, CTR | Awareness play; CTR 0.1–0.4% is normal |
| **Paid Search** | Clicks, CTR, CVR, CPC | Intent channel; CVR + CPC are key |
| **Video** | Impressions, VCR, CPV | Branding; revenue attribution is indirect |

### Benchmarks
- E-commerce ROAS: 4–5x
- SaaS ROAS: 3–4x
- Display CTR: 0.10–0.40% (anything above 1% is suspicious — likely not display data)
- Social CTR: 1–5% (targeted retargeting can reach 8–10%)
- Email Open Rate: 15–35%
- SMS Open Rate: 20–45% (typically highest of any channel)
- Search CVR: 1–5% (branded terms higher)

### Channel-to-Purpose Mapping
- Email = retention
- Paid search = intent capture
- Paid social = discovery / retargeting
- Display = reach / awareness
- Video = branding
- SMS = retention / rescue
- Direct mail = acquisition

## Dashboard Rendering

### Output File Naming — Unique Filenames Required

**Never overwrite an existing dashboard.** Every generated HTML file must have a unique name combining the company name and a timestamp:

```
{working_dir}/{company}_omnichannel_{YYYYMMDD_HHMM}.html
```

Examples:
- `tumi_omnichannel_20260428_1435.html`
- `pacsun_omnichannel_20260428_0912.html`

Derive the company name from the active CDP database or parent segment (e.g., `tumi_demo_2` → `tumi`). Always use today's date and current time in `YYYYMMDD_HHMM` format when writing the file.

### Environment Detection

Before rendering, detect which environment you are running in:

- **Treasure Studio**: The tool `render_react` (or `mcp__tdx-studio__render_react`) is available. Use it.
- **Treasure AI Studio** (or any environment without `render_react`): Generate a **self-contained HTML file** instead. The HTML must:
  1. Be a **single file** — no CDN links, no external CSS/JS. Everything inline.
  2. Use **vanilla JS + DOM manipulation** — no React, no JSX, no Recharts, no framework imports.
  3. **Inline all styles** in a `<style>` block. Translate Tailwind classes into plain CSS. Use CSS variables for theming.
  4. **Recreate charts as inline SVG** — bar charts, line charts, heatmaps rendered as SVG elements generated by vanilla JS.
  5. **Preserve all interactive features** — 9 tabs, channel deep dives, sub-tabs, KPI cards — using vanilla JS event listeners.
  6. Embed the data object as `const DATA = <JSON>;` in a `<script>` block.
  7. Include a dark/light theme toggle.
  8. Output the HTML directly in your response (the platform will render it).

**How to detect:** Check your available tools at the start of the rendering phase. If `render_react` is in your tool list, use it. If not, generate self-contained HTML.

### If `render_react` is available (Treasure Studio):

Use `render_react` for ALL visualizations. Build the dashboard data from query results, then embed it as a JSON constant inside the React component.

### For broad requests ("dashboard", "report", "overview"), build a full tabbed dashboard with 10 tabs:

1. **Overview** — Top KPI cards (Total Spend, Revenue, Avg ROAS, Active Campaigns) + channel spend vs revenue BarChart + clickable channel KPI cards in 2×3 grid (each showing funnel role badge, ROAS, primary KPI, spend, revenue — clicking jumps to that channel's deep dive) + marketing funnel visualization showing budget allocation by stage (Awareness→Consideration→Intent→Conversion)
2. **Segments** — ROAS heatmap showing all segments x all channels with color-coded cells (green=high, red=low) + Best Performer and Needs Attention callout cards
3. **Email** — Channel deep dive (see Channel Deep Dive Structure below)
4. **Paid Social** — Channel deep dive
5. **Paid Search** — Channel deep dive
6. **Display** — Channel deep dive
7. **SMS** — Channel deep dive
8. **Video** — Channel deep dive
9. **Direct Mail** — Channel deep dive
10. **Journey Performance** — Always the final tab. See Journey Performance Tab Specification below.

### Channel Deep Dive Structure

Each channel tab has:
1. **KPI pills row** — 6 pills: Revenue, Spend, ROAS (universal), then 3 channel-native metrics (see below)
2. **Campaign table** — channel-specific columns (see below)
3. **ROAS by Segment** bar chart (right side, consistent across all channels)
4. **Callout** — one insight card (finding or warning)

#### KPI Pills — Channel-Native (pills 4–6)

Use the first 3 pills for Revenue, Spend, ROAS universally. Pills 4–6 must reflect how that channel is actually measured:

| Channel | Pill 4 | Pill 5 | Pill 6 |
|---|---|---|---|
| **Email** | Open Rate (avg) | Click Rate (avg) | Conv Rate (avg) |
| **Paid Social** | Total Impressions | Avg CTR | Avg CPA |
| **SMS** | Total Sends | Open Rate (avg, highlight #1 if top channel) | Click Rate (avg) |
| **Display** | Total Impressions | Avg Viewability | Avg CTR |
| **Paid Search** | Total Clicks | Avg CTR | Avg CVR |
| **Video** | Total Impressions | Avg VCR | Avg CPV |

Never use "Peak ROAS", "Eng. Rate", or "Best Segment ROAS" as pills — these are table-level insights, not channel-level KPIs.

#### Campaign Table Columns — Channel-Specific

Each channel's campaign table must use columns native to how that channel is measured. Do NOT use the same generic column set (open/click/conv) across all channels:

| Channel | Table columns |
|---|---|
| **Email** | Campaign \| Segment \| Revenue \| ROAS \| Open Rate \| Click Rate \| Conv Rate |
| **Paid Social** | Campaign \| Segment \| Revenue \| Impressions \| CTR \| CPA \| ROAS |
| **SMS** | Campaign \| Segment \| Revenue \| Sends \| Open Rate \| Click Rate \| ROAS |
| **Display** | Campaign \| Segment \| Revenue \| Impressions \| Viewability \| CTR \| CPA |
| **Paid Search** | Campaign \| Segment \| Revenue \| Clicks \| CTR \| CVR \| CPC |
| **Video** | Campaign \| Segment \| Impressions \| Views \| VCR \| CPV \| Spend |

#### Derived Metrics (when source data lacks channel-native columns)

Campaign tables in CDP often store only generic `open_rate`, `click_rate`, `conversion_rate`. When the source table doesn't have channel-specific fields, derive them from spend and revenue:

| Metric | Derivation |
|---|---|
| **Impressions (Social)** | `spend / $7 × 1000` (assumes $7 CPM for paid social) |
| **Impressions (Display)** | `spend / $3.50 × 1000` (assumes $3.50 CPM for display) |
| **Sends (SMS)** | `spend / $0.04` (assumes $0.04 per message) |
| **Clicks (Search)** | `(revenue / AOV) / CVR` where AOV ≈ $500 for luxury retail |
| **CPC (Search)** | `spend / clicks` |
| **CPA** | `spend / (revenue / AOV)` |
| **Viewability** | Use `open_rate` field if 50–80% range; otherwise default 65% avg |
| **CTR (Display)** | Realistic display CTR is 0.10–0.40% — do NOT reuse email click_rate |

Always add a `title` tooltip on derived column headers noting the derivation method (e.g., `title="Derived at $7 CPM"`).

#### Right-Side Bar Chart

Keep "ROAS by Segment" for all channels — it's the universal business performance signal. Channel-specific bar charts (CPA, CVR, VCR) can be added as a second chart but should not replace ROAS.

---

### Journey Performance Tab Specification

**Always include this as the final tab** in the omni-channel dashboard. Do NOT query the API for live journey metrics — journeys are typically in draft or newly activated. Instead, **fabricate plausible simulated data** grounded in actual segment sizes and real AOV from the workshop's CDP data.

Journeys follow a **3-stage, omni-channel escalation model**: Stage 1 (Email + App Push) → Stage 2 (Social + Search retargeting) → Stage 3 (VIP SMS last-chance). Every section of this tab must reflect that structure — not a flat single-channel funnel.

#### Summary KPI Strip (6 pills)

| Pill | Value guidance |
|---|---|
| Total Enrolled | Sum of all journey entry segment sizes (use actual `tdx sg list` sizes) |
| Goal Achieved | 8–18% of entries overall — the punchline metric |
| Revenue Attributed | Goal Achieved × avg 2nd-order AOV (use real AOV if queried; else estimate from brand/LTV) |
| Stage 1 Conversion | 6–12% convert in Stage 1 (Email+App) — highest ROAS stage |
| Stage 2 Escalation | 50–65% of non-converters reach Stage 2 (Social+Search) |
| Avg Days to Convert | Weight by stage: Stage 1 ≈ 3–5 days, Stage 2 ≈ 8–12 days, Stage 3 ≈ 18–22 days |

#### Per-Journey Cards (one card per active journey)

Each card reflects the 3-stage journey structure. Required elements:

**1. Journey header**
- Name, entry segment + qualifier
- Channel sequence badge: `Email + App → Social/Search → VIP SMS`
- Overall conversion rate badge

**2. Stage-escalation funnel** (5 steps, not 4)

```
Entered → Stage 1 Active → Stage 2 Escalated → Stage 3 Escalated → Converted
```

Simulate realistic drop-off at each transition:
- Stage 1 Active: 65–75% of entries (some filtered out immediately)
- Stage 2 Escalated: 50–60% of Stage 1 non-converters (some convert in S1 or exit)
- Stage 3 Escalated: 40–55% of Stage 2 non-converters
- Converted: 8–18% of original entries total

**3. Per-stage conversion breakdown** — for each stage show:
- Customers who entered that stage
- Customers who converted at that stage (not in a later stage)
- Stage ROAS (Stage 1 highest, Stage 3 lowest — escalating cost model)
- Key channel for that stage

| Stage | Expected conv rate | Channel | ROAS relative to S1 |
|---|---|---|---|
| Stage 1: Email + App Push | 6–12% of enrolled | Email (primary), App Push (branch) | Baseline (highest) |
| Stage 2: Social + Search | 3–6% of enrolled | Meta/Social + Google/Search (High LTV branch) | 40–60% of S1 |
| Stage 3: VIP SMS | 1–3% of enrolled | SMS exclusive offer | 20–35% of S1 |

**4. Decision point breakdown (two per journey)**

Show both decision points as side-by-side branch cards within the journey card:

*Stage 1 branch — "Has App / Has Mobile Consent":*
- App Push branch: ~30–40% of S1 customers qualify → higher conversion (+8–12pp vs email-only)
- Email-only branch: 60–70% → email conversion rate only

*Stage 2 branch — "High LTV / High Propensity":*
- Search retargeting (High LTV): ~35–45% of S2 customers → higher conv (~15–20% of S2 entrants)
- Social only (Standard): 55–65% → lower conv (~8–12% of S2 entrants)

**5. Top performing step callout** per card — always the Stage 1 App Push branch or the Stage 2 High LTV → Search routing (whichever has the highest absolute conversion rate)

#### Stage-Level Intelligence Section

Show a 3-column grid — one column per journey — with stage-by-stage breakdown:

For each journey × stage, display:
- Stage name + channels active in that stage
- Customers entering that stage (count + % of original enrolled)
- Customers converting at that stage
- Stage conversion rate
- A CSS progress bar scaled to the stage's share of total conversions
- Both decision point branch outcomes as sub-rows (indented)

**Key narrative to surface**: Stage 1 Email+App produces the most conversions at the lowest cost. Stage 2 and 3 exist to capture value that would otherwise be permanently lost — but at higher per-conversion cost. The business case for all 3 stages is the incremental revenue vs. zero-contact baseline.

#### Revenue Attribution by Stage

Three stacked/grouped bar charts (one per journey), each showing revenue split across Stage 1 / Stage 2 / Stage 3:
- Stage 1 typically drives 55–65% of total journey revenue
- Stage 2 drives 25–35%
- Stage 3 drives 8–15%

Below the charts: **Stage ROAS comparison table** — shows that Stage 1 ROAS is 3–5× higher than Stage 3, reinforcing the "owned channels first" strategy.

#### Cross-Journey Intelligence (4 metric tiles)

| Tile | Content |
|---|---|
| Stage 1 Coverage | % of enrolled who received the email+app push — should be close to 100%; gaps indicate consent/deliverability issues |
| Blended Journey ROAS | Total attributed revenue ÷ estimated journey send cost (~8–10×, higher than paid media blended); callout that this beats the paid channel average |
| Stage 3 Rescue Value | Revenue recovered exclusively by the VIP SMS stage — customers who would have been permanently lost without it |
| Purchase Window Gap | Show real avg days to 2nd purchase (from transaction data if queried; else 60–90 days) vs combined journey window (Stages 1–3 span 17–21 days) — even a 3-stage journey exits too early |

#### Top 3 Optimization Signals

1. **Extend journey window past Stage 3** — the 3-stage journey spans ~17–21 days but the natural repeat purchase window is 60–90 days. A Stage 4 "long-tail nurture" (lightweight email at day 30 + day 60) could recover another 4–6% of non-converters. Project at Stage 1 email conversion rate (lowest cost assumption). Est. revenue: highest of the three signals.

2. **Increase Stage 1 App Push reach** — only 30–40% of customers qualify for the App Push branch (has app installed). Growing app install rate by 10pp increases Stage 1 conversion by ~2pp with zero incremental media cost. Frame as an app download campaign targeting the journey entry segments before journey activation.

3. **Lower Stage 2 LTV threshold for Search routing** — currently only High LTV customers (top 35–45%) get Search retargeting in Stage 2. Lowering the threshold to include the next LTV tier adds ~15–20% more customers to the higher-converting Search branch. Project at Stage 2 Search conversion rate (conservative vs High LTV rate). Est. revenue: second highest signal.

Include revenue estimate for each signal grounded in actual segment sizes and AOV.

#### Simulated Data Disclaimer

Always end the tab with:
> *"Simulated performance data — journeys activated [today's date]. Live metrics available after first full refresh cycle. Stage structure reflects 3-stage omni-channel design (Email+App → Social/Search → VIP SMS). Segment sizes grounded in actual CDP data. AOV grounded in real transaction data."*

---

### For narrow requests (single metric or channel), build a focused component with relevant KPI cards and chart.

### Component Rules (CRITICAL)

- Single function component only — no sub-components, no helper components
- All JSX must be inlined directly — no abstractions like `KPICard`, `TabPanel`
- Use `useState` for tab switching and filters
- Recharts components are available as globals (BarChart, LineChart, PieChart, AreaChart, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell, Bar, Line, Pie, Area) — do NOT import them
- Use `Bar` not `BarChart.Bar`, `Line` not `LineChart.Line`, `Pie` not `PieChart.Pie` — these are standalone globals
- React hooks (useState, useEffect, useMemo) are available as globals — do NOT import them
- Tailwind CSS classes are available for styling
- Embed query result data directly as a JSON array inside the component
- Never use `<` or `>` in text nodes — use words or HTML entities

### Color Palette — Treasure Data Brand

```js
const C = {
  primary: '#1A57DB', primaryMed: '#5A81DD', primaryLight: '#C7D4F3', primaryDark: '#252D6E',
  coral: '#FF6B6B', teal: '#2EC4B6', amber: '#FFB84D', purple: '#7C5CFC',
  green: '#34D399', pink: '#F472B6',
  bg: '#0F172A', card: '#1E293B', cardHover: '#334155', border: '#334155',
  text: '#F8FAFC', textMuted: '#94A3B8', textDim: '#64748B'
};
```

Channel colors: email=coral, facebook=primary, paid_search=teal, display=amber, sms=purple, video=green.

### Number Formatting

- Currency: compact notation (`$1.2M`, `$529K`)
- Percentages: with `%` symbol (e.g., `3.50%`)
- ROAS: with `x` suffix (e.g., `2.31x`)
- Use a helper: `const fmt = (n,p) => p==='$' ? '$'+(n>=1e6?(n/1e6).toFixed(1)+'M':n>=1e3?(n/1e3).toFixed(0)+'K':n.toFixed(0)) : p==='%' ? n.toFixed(2)+'%' : n.toFixed(2)+'x';`

### Layout

- Dark background (`#0F172A`) with slate card surfaces (`#1E293B`)
- Gradient title header using TD primary blue to teal
- Pill badges for channel funnel roles
- Color-coded priority tags on recommendations
- Cards with `border-radius: 12px` and subtle `1px solid #334155` borders

## Output Format

### Summary
Concise overview of key findings (2-3 sentences)

### Analysis Details
Detailed segment-level performance and observations

### Visualizations
Interactive React dashboard via `render_react`

### Recommendations
2-3 strategic, actionable next steps:
- Increase spend on top-performing segments
- Pause or reduce underperformers
- Suggest creative, targeting, or landing page tests
- Recommend new segmentation opportunities

## Example Output Table

| Segment | ROAS/CTR | Spend | Revenue | Supporting Metrics | Action |
|---------|----------|-------|---------|-------------------|--------|
| Facebook A | 5.2x | $5,000 | $26,000 | CTR: 1.8%, CPC: $1.20 | Increase budget |
| Search B | 3.1x | $3,500 | $10,850 | CTR: 2.2%, CPC: $1.50 | Optimize keywords |
| Email C | 4.8x | $800 | $3,840 | CTR: 3.5%, Conv: 4.2% | Test lifecycle triggers |
| SMS D | 2.7x | $400 | $1,080 | CTR: 6.1%, Conv: 2.0% | Refine audience |
| Display | 0.7% | $2,000 | $1,200 | CPC: $2.85 | Pause or reallocate |
| Video E | 1.1% | $1,500 | N/A | CPC: $3.10 | Test new creative |
