-- Segment × Channel ROAS heatmap for PRE-AGGREGATED tables
-- Placeholders: {{database}}, {{table}}, {{channel_col}}, {{segment_col}},
--   {{spend_col}}, {{revenue_col}}

SELECT
  {{segment_col}} AS segment,
  {{channel_col}} AS channel,
  SUM({{spend_col}}) AS total_spend,
  SUM({{revenue_col}}) AS total_revenue,
  CASE WHEN SUM({{spend_col}}) > 0 THEN ROUND(CAST(SUM({{revenue_col}}) AS DOUBLE) / SUM({{spend_col}}), 2) ELSE 0 END AS roas
FROM {{database}}.{{table}}
GROUP BY {{segment_col}}, {{channel_col}}
ORDER BY {{segment_col}}, {{channel_col}}
