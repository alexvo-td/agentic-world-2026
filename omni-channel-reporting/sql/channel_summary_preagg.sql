-- Channel × Segment summary query for PRE-AGGREGATED tables
-- Tables that already have spend, revenue, open_rate, click_rate, etc. as columns
-- Placeholders: {{database}}, {{table}}, {{channel_col}}, {{segment_col}}, {{campaign_col}},
--   {{spend_col}}, {{revenue_col}}, {{open_rate_col}}, {{click_rate_col}}, {{conv_rate_col}}

SELECT
  {{channel_col}} AS channel,
  {{segment_col}} AS segment_name,
  COUNT(DISTINCT {{campaign_col}}) AS campaign_count,
  SUM({{spend_col}}) AS total_spend,
  SUM({{revenue_col}}) AS total_revenue,
  CASE WHEN SUM({{spend_col}}) > 0 THEN ROUND(CAST(SUM({{revenue_col}}) AS DOUBLE) / SUM({{spend_col}}), 2) ELSE 0 END AS roas,
  ROUND(AVG({{open_rate_col}}), 2) AS avg_open_rate,
  ROUND(AVG({{click_rate_col}}), 2) AS avg_click_rate,
  ROUND(AVG({{conv_rate_col}}), 2) AS avg_conversion_rate
FROM {{database}}.{{table}}
GROUP BY {{channel_col}}, {{segment_col}}
ORDER BY total_revenue DESC
