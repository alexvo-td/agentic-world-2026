-- Segment × Channel ROAS heatmap for EVENT-LEVEL tables
-- Produces one row per segment × channel with aggregated revenue for ROAS computation
-- Placeholders: {{database}}, {{engagement_table}}, {{order_table}},
--   {{customer_id_col}}, {{channel_col}}, {{event_type_col}},
--   {{segment_table}}, {{segment_col}}, {{segment_join_key}},
--   {{order_revenue_col}}

SELECT
  seg_eng.segment,
  seg_eng.channel,
  seg_eng.unique_customers,
  seg_eng.sends,
  seg_eng.opens,
  seg_eng.clicks,
  COALESCE(seg_rev.revenue, 0) AS revenue,
  COALESCE(seg_rev.conversions, 0) AS conversions
FROM (
  SELECT
    s.{{segment_col}} AS segment,
    e.{{channel_col}} AS channel,
    COUNT(DISTINCT e.{{customer_id_col}}) AS unique_customers,
    SUM(CASE WHEN e.{{event_type_col}} = 'send' THEN 1 ELSE 0 END) AS sends,
    SUM(CASE WHEN e.{{event_type_col}} = 'open' THEN 1 ELSE 0 END) AS opens,
    SUM(CASE WHEN e.{{event_type_col}} = 'click' THEN 1 ELSE 0 END) AS clicks
  FROM {{database}}.{{engagement_table}} e
  LEFT JOIN {{database}}.{{segment_table}} s ON e.{{customer_id_col}} = s.{{segment_join_key}}
  GROUP BY s.{{segment_col}}, e.{{channel_col}}
) seg_eng
LEFT JOIN (
  SELECT
    s.{{segment_col}} AS segment,
    clk.channel,
    COUNT(DISTINCT o.{{customer_id_col}}) AS conversions,
    SUM(o.{{order_revenue_col}}) AS revenue
  FROM (
    SELECT {{customer_id_col}}, {{channel_col}} AS channel, MAX(event_time) AS last_click
    FROM {{database}}.{{engagement_table}}
    WHERE {{event_type_col}} = 'click'
    GROUP BY {{customer_id_col}}, {{channel_col}}
  ) clk
  INNER JOIN {{database}}.{{order_table}} o
    ON clk.{{customer_id_col}} = o.{{customer_id_col}} AND o.event_time >= clk.last_click
  LEFT JOIN {{database}}.{{segment_table}} s ON clk.{{customer_id_col}} = s.{{segment_join_key}}
  GROUP BY s.{{segment_col}}, clk.channel
) seg_rev ON seg_eng.segment = seg_rev.segment AND seg_eng.channel = seg_rev.channel
ORDER BY seg_eng.segment, seg_eng.channel
