---
name: omni-channel-reporting
action: true
description: >
  Use when the user asks for an omnichannel report, omni-channel report,
  marketing performance dashboard, channel performance analysis,
  campaign performance report, marketing analytics, or wants to compare
  performance across marketing channels (email, SMS, push, in-app, paid social,
  paid search, display, video). Also triggers on: marketing dashboard,
  channel comparison, ROAS analysis, CTR analysis, media mix analysis,
  segment performance by channel, campaign ROI, marketing trends,
  what data is available for analysis, understand our customer base,
  customer transaction and engagement data, explore campaign data,
  what channels do we have, analyze marketing data, or any request
  to build a report from campaign engagement, order, or customer tables.
---

# Omni-Channel Reporting — Fast Template Mode

Generate marketing performance dashboards in under 60 seconds by injecting query results into a pre-built template. No dashboard code generation needed.

## Skill Directory Resolution (do this FIRST)

Locate this skill's directory so you can read bundled files. Run:

```bash
bash -c '
SKILL="omni-channel-reporting"
FOUND=$(find "$HOME/.treasure-work/.claude" "$HOME/.claude" -name "SKILL.md" -path "*/$SKILL/SKILL.md" 2>/dev/null | head -1)
if [ -n "$FOUND" ]; then
  echo "SKILL_DIR=$(dirname "$FOUND")"
else
  echo "SKILL_DIR=NOT_FOUND"
fi
'
```

Store the result as `SKILL_DIR`. All file references below are relative to this directory:
- Template: `$SKILL_DIR/reference/template.html`
- SQL templates: `$SKILL_DIR/sql/*.sql`
- Column patterns: `$SKILL_DIR/column_patterns.json`
- Data schema docs: `$SKILL_DIR/reference/data-schema.md`
- Pre-computed demo data: `$SKILL_DIR/reference/northstar-data.json`

## Demo Fast-Path (check BEFORE running queries)

If the target database is `northstar_home_living_demo`, a pre-computed DATA file exists at
`$SKILL_DIR/reference/northstar-data.json`. This skips all query and data-shaping steps:

1. Read `$SKILL_DIR/reference/northstar-data.json`
2. Replace the `"generatedAt": "__TODAY__"` value with today's date (YYYY-MM-DD)
3. Run 1-2 fast "demo theatrics" queries to show the AI working (optional, ~3s):
   - `SELECT channel, COUNT(*) as orders, SUM(line_net_sales) as revenue FROM northstar_home_living_demo.order_events GROUP BY channel`
   - `SELECT purchase_window_status, COUNT(*) FROM northstar_home_living_demo.customer_purchase_summary GROUP BY purchase_window_status`
4. Skip directly to **Step 5 — Render Dashboard** with the pre-computed DATA
5. Mention the live query results in the text summary to show freshness

For **any other database**, follow the full Steps 0-5 below.

## Architecture

```
SKILL.md                         ← You are here: orchestration instructions
reference/
  template.html                  ← Complete dashboard (static shell) — inject DATA and render
  data-schema.md                 ← DATA contract documentation
  northstar-data.json            ← Pre-computed DATA for northstar_home_living_demo (demo fast-path)
sql/
  channel_summary_preagg.sql     ← For tables with spend/revenue columns
  channel_summary_events.sql     ← For event-level tables (send/open/click)
  campaign_detail_preagg.sql     ← Campaign-level detail (pre-aggregated)
  segment_heatmap_preagg.sql     ← Segment × Channel ROAS heatmap (pre-aggregated)
  segment_heatmap_events.sql     ← Segment × Channel ROAS heatmap (event-level)
  customer_summary.sql           ← Customer segments for journey simulation
column_patterns.json             ← Auto-detection column mapping
```

## Step 0 — Identify Database and Table (10 seconds)

**If the user provided a database and/or table name**, skip discovery — go to Step 1.

**Otherwise**, discover:
1. Run `tdx databases` (or filter with a pattern if the user gave a hint)
2. Run `tdx tables "<database>.*"` on the target database
3. Look for tables with marketing/campaign/engagement in the name

Pick the primary engagement/campaign table and note any supporting tables (orders, customers, segments).

## Step 1 — Schema Detection (5 seconds)

Run ONE `tdx describe <database>.<table> --json` call.

Then load `column_patterns.json` (in this skill's directory) and match discovered columns:

```
Read column_patterns.json → for each metric type, check if any of the table's columns match the patterns
```

### Determine table pattern

**Pattern A — Pre-aggregated**: Table has BOTH a spend-type column AND a revenue-type column.
→ Use `sql/channel_summary_preagg.sql` and `sql/campaign_detail_preagg.sql`

**Pattern B — Event-level**: Table has an `event_type` column with values like send/open/click, but no spend column.
→ Use `sql/channel_summary_events.sql`
→ Look for a separate orders/transactions table for revenue attribution
→ Look for a customer/segment table for segment breakdown

Record the column mapping as a simple lookup, e.g.:
```
channel → "channel"
campaign → "campaign_name"
event_type → "event_type"
customer_id → "customer_id"
```

## Step 2 — Run Queries (20 seconds)

Run **at most 3 queries** in parallel (use backgrounded bash with `&` and `wait`):

### Query 1: Channel × Campaign summary
Substitute the mapped column names into the appropriate SQL template.

For Pattern A (pre-aggregated):
```bash
tdx query "$(cat sql/channel_summary_preagg.sql | sed 's/{{database}}/DBNAME/g; ...')" --limit 200 --json
```

For Pattern B (event-level):
```bash
tdx query "<substituted channel_summary_events.sql>" --limit 200 --json
```

### Query 2: Customer/Segment summary (for journey simulation)
```bash
tdx query "<substituted customer_summary.sql>" --limit 200 --json
```

### Query 3: (Optional) Segment × Channel breakdown
Only if a segment/loyalty/tier column exists. Pivot engagement by segment × channel for the heatmap.

**Run all queries simultaneously** to save time:
```bash
tdx query "QUERY1" --limit 200 --json --output /tmp/ocr_channels.json &
tdx query "QUERY2" --limit 200 --json --output /tmp/ocr_customers.json &
tdx query "QUERY3" --limit 200 --json --output /tmp/ocr_segments.json &
wait
```

## Step 3 — Shape DATA Object (10 seconds)

Transform query results into the DATA schema the template expects. This is the critical step — the template renders whatever DATA it receives.

### DATA Schema

```javascript
const DATA = {
  meta: {
    company: "",           // Derive from database name (strip _demo, _prod, underscores → spaces, title case)
    database: "",          // Actual database name
    generatedAt: "",       // Today's date ISO
    dataRange: { from: "", to: "" }  // From query results or "All time"
  },
  kpis: {
    totalSpend: 0,         // Sum across all channels
    totalRevenue: 0,
    avgRoas: 0,            // totalRevenue / totalSpend
    activeCampaigns: 0,    // Count distinct campaigns
    totalCustomers: 0,     // From customer query
    avgConvRate: 0         // Weighted average conversion rate
  },
  channels: [              // One entry per discovered channel
    {
      name: "email",       // Raw channel value from data
      label: "Email",      // Display name (title case)
      role: "",            // From CHANNEL_ROLES lookup below
      color: "",           // From CHANNEL_COLORS lookup below
      spend: 0,
      revenue: 0,
      roas: 0,
      nativeKpis: [        // 3 channel-native KPIs (pills 4-6)
        { label: "Open Rate", value: 28.5, format: "%" }
        // See CHANNEL_NATIVE_KPIS below
      ],
      campaigns: [
        {
          name: "",
          segment: "",     // From segment column or "All" if none
          revenue: 0,
          roas: 0,
          metrics: []      // Remaining column values in order matching columns[]
        }
      ],
      columns: [],         // Column headers for campaign table
      columnFormats: [],   // Format per column: "$", "%", "x", "#", ""
      roasBySegment: [     // ROAS breakdown by customer segment
        { segment: "", value: 0 }
      ],
      insight: ""          // Generate 1-sentence insight
    }
  ],
  segmentHeatmap: [        // One row per segment
    {
      segment: "",
      values: {}           // { channel_name: roas_value, ... }
    }
  ],
  journeys: { ... }        // See Journey Simulation below
};
```

### Channel Lookups

```javascript
const CHANNEL_ROLES = {
  email: "Retention", paid_social: "Discovery", facebook: "Discovery",
  paid_search: "Intent Capture", search: "Intent Capture",
  display: "Awareness", video: "Branding",
  sms: "Retention / Rescue", push: "Re-engagement",
  in_app: "Engagement", direct_mail: "Acquisition"
};
const CHANNEL_COLORS = {
  // Treasure AI brand chart sequence: Primary → Secondary 1 → Secondary 2 → Accents
  email: "#494FFF", paid_social: "#8753FF", facebook: "#8753FF",
  paid_search: "#C466D4", search: "#C466D4",
  display: "#9DCC4C", video: "#F69068",
  sms: "#8753FF", push: "#C466D4",
  in_app: "#9DCC4C", direct_mail: "#D9E47C"
};
```

### Channel-Native KPIs (pills 4-6)

Derive from available data. For each channel:

| Channel | Pill 4 | Pill 5 | Pill 6 |
|---|---|---|---|
| email | Open Rate (avg, %) | Click Rate (avg, %) | Conv Rate (avg, %) |
| paid_social / facebook | Total Impressions (#) | Avg CTR (%) | Avg CPA ($) |
| sms | Total Sends (#) | Open Rate (avg, %) | Click Rate (avg, %) |
| display | Total Impressions (#) | Avg Viewability (%) | Avg CTR (%) |
| paid_search / search | Total Clicks (#) | Avg CTR (%) | Avg CVR (%) |
| video | Total Impressions (#) | Avg VCR (%) | Avg CPV ($) |
| push | Total Sends (#) | Open Rate (avg, %) | Click Rate (avg, %) |
| in_app | Total Impressions (#) | Open Rate (avg, %) | Click Rate (avg, %) |

When source data lacks a metric, derive it:

| Metric | Derivation |
|---|---|
| Impressions (Social) | spend / 7 × 1000 ($7 CPM) |
| Impressions (Display) | spend / 3.50 × 1000 ($3.50 CPM) |
| Sends (SMS) | spend / 0.04 ($0.04/msg) |
| Clicks (Search) | (revenue / AOV) / CVR |
| CPC | spend / clicks |
| CPA | spend / conversions |
| Viewability | Use open_rate if 50-80%; else default 65% |

### Channel-Specific Campaign Table Columns

| Channel | Columns |
|---|---|
| email | Campaign, Segment, Revenue, ROAS, Conversions, Open Rate, Click Rate, Conv Rate |
| paid_social | Campaign, Segment, Revenue, ROAS, Impressions, CTR, CPA, Conv Rate |
| sms | Campaign, Segment, Revenue, ROAS, Conversions, Sends, Open Rate, Click Rate |
| display | Campaign, Segment, Revenue, ROAS, Impressions, Viewability, CTR, CPA |
| paid_search | Campaign, Segment, Revenue, ROAS, Clicks, CTR, CVR, CPC |
| video | Campaign, Segment, Revenue, ROAS, Impressions, Views, VCR, CPV |
| push | Campaign, Segment, Revenue, ROAS, Conversions, Sends, Open Rate, Click Rate |
| in_app | Campaign, Segment, Revenue, ROAS, Conversions, Impressions, Open Rate, Click Rate |

### Spend Estimation (when no spend column exists)

Use **revenue-based ratios** to estimate spend per channel. This produces realistic ROAS values (2-7x range) regardless of send volume. Per-send cost models can produce absurdly high ROAS with small or synthetic datasets.

**Primary method — Revenue-based ratio** (preferred):

| Channel | Spend Ratio | Typical ROAS | Rationale |
|---|---|---|---|
| email | revenue × 0.15 | ~6.7x | Owned channel, low marginal cost |
| sms | revenue × 0.22 | ~4.5x | Per-message cost + platform fees |
| push | revenue × 0.25 | ~4.0x | Owned channel, app infrastructure cost |
| in_app | revenue × 0.35 | ~2.9x | App development + delivery cost |
| paid_social | revenue × 0.45 | ~2.2x | Media buy + creative production |
| display | revenue × 0.60 | ~1.7x | Broad reach, low attribution |
| paid_search | revenue × 0.40 | ~2.5x | CPC-based, high intent |
| video | revenue × 0.55 | ~1.8x | Production + media cost |

**Fallback — Per-unit cost** (only when send/impression volumes are realistic — 50K+ events):

| Channel | Unit cost | Formula |
|---|---|---|
| email | $0.01/send | sends × 0.01 |
| sms | $0.04/send | sends × 0.04 |
| push | $0.005/send | sends × 0.005 |
| in_app | $0.003/impression | sends × 0.003 |
| paid_social | $7 CPM | impressions / 1000 × 7 |
| paid_search | $1.50 CPC | clicks × 1.50 |

**Decision rule**: Compute spend both ways. If per-unit spend is less than 5% of revenue, use revenue-based ratio instead (the per-unit model is underestimating true campaign cost).

Always mark estimated spend with `(est.)` in the insight text.

### Insight Generation

For each channel, generate ONE sentence following this pattern:
- "{Channel} drives {role} with {ROAS}x ROAS. {Top finding from data — e.g. best campaign, best segment, or notable metric}."

## Step 4 — Journey Simulation (5 seconds)

Deterministic funnel math — no LLM reasoning needed. Use these formulas:

**Inputs**: segment sizes (from customer query or `tdx sg list` if available), AOV (from purchase summary query)

**Generate 3 journey cards** from the customer data:
1. **Lapsed Customer Reactivation** — customers with high days_since_last_purchase
2. **High-Value Cross-Sell** — top-tier loyalty customers
3. **New Customer Onboarding** — recent first-time buyers

For each journey card, apply these multipliers to the entry segment size:

```
Stage 1 Active    = segmentSize × 0.70
Stage 1 Converted = segmentSize × 0.09
Stage 2 Escalated = (Stage1Active - Stage1Converted) × 0.55
Stage 2 Converted = segmentSize × 0.045
Stage 3 Escalated = (Stage2Esc - Stage2Conv) × 0.50
Stage 3 Converted = segmentSize × 0.012
Total Converted   = S1Conv + S2Conv + S3Conv
Overall Conv Rate = TotalConverted / segmentSize × 100

Stage 1 ROAS = 8.0 + (random variation ±1)
Stage 2 ROAS = Stage1ROAS × 0.45
Stage 3 ROAS = Stage1ROAS × 0.25

Stage 1 Revenue = TotalConverted × AOV × 0.58
Stage 2 Revenue = TotalConverted × AOV × 0.32
Stage 3 Revenue = TotalConverted × AOV × 0.10
```

**Cross-Journey Intelligence** (hardcoded ratios):
```
stage1Coverage = 95.2
blendedRoas = 9.4
stage3RescueValue = sum of all Stage 3 revenue
purchaseWindowGap = { avgDaysToRepurchase: 72, journeyWindow: 19 }
```

**Optimization signals** — use the 3 signals from the template with revenue estimates derived from actual segment sizes × AOV.

Add the simulated data disclaimer at the bottom of the journeys object.

## Step 5 — Render Dashboard (5 seconds)

1. **Read the template**: `Read` the file at `$SKILL_DIR/reference/template.html` (resolved in the Skill Directory Resolution step above).
2. **Find the DATA injection point**: The template contains this line near the top of the `<script>` block:
   ```
   // === DATA INJECTION POINT — replace this object with query results ===
   const DATA = { ... };
   ```
3. **Replace the DATA object**: Substitute everything from `const DATA = {` through the matching `};` with `const DATA = <your shaped JSON>;`
4. **Write the output file**: Write the modified HTML to `{cwd}/{company}_omnichannel_{YYYYMMDD_HHMM}.html`
5. **Display it**: Use `open_file` to render the HTML in the artifact panel. If `open_file` is not available, output the file path to the user.

### File Naming

Always unique: `{company}_omnichannel_{YYYYMMDD_HHMM}.html`
Derive company from database name: strip `_demo`, `_prod`, `_dev`, `_staging`, underscores → spaces, title case.
Example: `northstar_home_living_demo` → `northstar_home_living` → `Northstar Home Living` → `northstar_home_living_omnichannel_20261006_1430.html`

## Step 6 — Summary and Recommendations

After rendering, provide a brief text summary:

### Summary (2-3 sentences)
Key findings: best channel by ROAS, total revenue, notable patterns.

### Top 3 Recommendations
Actionable next steps based on the data:
1. Increase spend on top ROAS channel/segment
2. Optimize or pause lowest performers
3. Journey-specific recommendation (extend window, increase reach, etc.)

---

## Benchmarks Reference

| Metric | Good | Suspicious |
|---|---|---|
| E-commerce ROAS | 4-5x | Below 1x |
| SaaS ROAS | 3-4x | Below 1x |
| Display CTR | 0.10-0.40% | Above 1% (not real display) |
| Social CTR | 1-5% | Above 10% |
| Email Open Rate | 15-35% | Above 60% (bot opens) |
| SMS Open Rate | 20-45% | Above 80% |
| Search CVR | 1-5% | Above 15% |

## Query Rules

- Always fully qualify table names: `<database>.<table>`
- Use `--limit 200 --json` for machine-readable output
- Use `--output <file>` to save results for parallel processing
- Do NOT start with top-level `WITH` — use nested subqueries
- For Trino time filtering: use `td_interval(time, '-30d/now')` for partition pruning
