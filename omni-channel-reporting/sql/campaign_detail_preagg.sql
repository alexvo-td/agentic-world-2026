-- Campaign detail query for PRE-AGGREGATED tables
-- Placeholders: {{database}}, {{table}}, {{channel_col}}, {{segment_col}}, {{campaign_col}},
--   {{spend_col}}, {{revenue_col}}, {{open_rate_col}}, {{click_rate_col}}, {{conv_rate_col}}

SELECT
  {{channel_col}} AS channel,
  {{campaign_col}} AS campaign_name,
  {{segment_col}} AS segment_name,
  SUM({{spend_col}}) AS spend,
  SUM({{revenue_col}}) AS revenue,
  CASE WHEN SUM({{spend_col}}) > 0 THEN ROUND(CAST(SUM({{revenue_col}}) AS DOUBLE) / SUM({{spend_col}}), 2) ELSE 0 END AS roas,
  ROUND(AVG({{open_rate_col}}), 2) AS open_rate,
  ROUND(AVG({{click_rate_col}}), 2) AS click_rate,
  ROUND(AVG({{conv_rate_col}}), 2) AS conversion_rate
FROM {{database}}.{{table}}
GROUP BY {{channel_col}}, {{campaign_col}}, {{segment_col}}
ORDER BY {{channel_col}}, revenue DESC
