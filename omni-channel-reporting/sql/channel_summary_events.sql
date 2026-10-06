-- Channel × Segment summary for EVENT-LEVEL tables
-- Used when engagement data is stored as individual events (send, open, click)
-- with a separate orders table for revenue attribution.
-- Placeholders: {{database}}, {{engagement_table}}, {{order_table}},
--   {{channel_col}}, {{campaign_col}}, {{event_type_col}}, {{customer_id_col}},
--   {{order_revenue_col}}, {{order_status_filter}} (e.g. "= 'completed'")
-- Optional: {{segment_table}}, {{segment_col}} — if a segment/decisioning table exists

SELECT
  eng.channel,
  eng.campaign_name,
  eng.sends,
  eng.opens,
  eng.clicks,
  eng.unique_customers,
  CASE WHEN eng.sends > 0 THEN ROUND(eng.opens * 100.0 / eng.sends, 2) ELSE 0 END AS open_rate,
  CASE WHEN eng.opens > 0 THEN ROUND(eng.clicks * 100.0 / eng.opens, 2) ELSE 0 END AS click_rate,
  COALESCE(rev.conversions, 0) AS conversions,
  COALESCE(rev.revenue, 0) AS revenue,
  CASE WHEN eng.clicks > 0 THEN ROUND(COALESCE(rev.conversions, 0) * 100.0 / eng.clicks, 2) ELSE 0 END AS conversion_rate
FROM (
  SELECT
    {{channel_col}} AS channel,
    {{campaign_col}} AS campaign_name,
    COUNT(DISTINCT {{customer_id_col}}) AS unique_customers,
    SUM(CASE WHEN {{event_type_col}} = 'send' THEN 1 ELSE 0 END) AS sends,
    SUM(CASE WHEN {{event_type_col}} = 'open' THEN 1 ELSE 0 END) AS opens,
    SUM(CASE WHEN {{event_type_col}} = 'click' THEN 1 ELSE 0 END) AS clicks
  FROM {{database}}.{{engagement_table}}
  GROUP BY {{channel_col}}, {{campaign_col}}
) eng
LEFT JOIN (
  SELECT
    clk.channel,
    clk.campaign_name,
    COUNT(DISTINCT o.{{customer_id_col}}) AS conversions,
    SUM(o.{{order_revenue_col}}) AS revenue
  FROM (
    SELECT {{customer_id_col}}, {{channel_col}} AS channel, {{campaign_col}} AS campaign_name, MAX(event_time) AS last_click
    FROM {{database}}.{{engagement_table}}
    WHERE {{event_type_col}} = 'click'
    GROUP BY {{customer_id_col}}, {{channel_col}}, {{campaign_col}}
  ) clk
  INNER JOIN {{database}}.{{order_table}} o
    ON clk.{{customer_id_col}} = o.{{customer_id_col}}
    AND o.event_time >= clk.last_click
  GROUP BY clk.channel, clk.campaign_name
) rev
  ON eng.channel = rev.channel AND eng.campaign_name = rev.campaign_name
ORDER BY eng.channel, revenue DESC
