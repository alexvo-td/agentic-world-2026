-- Customer-level purchase + segment summary for revenue attribution and journey simulation
-- Placeholders: {{database}}, {{purchase_summary_table}}, {{consent_table}}, {{customer_id_col}}
-- Optional: {{decisioning_table}} — for propensity/next-best-channel

SELECT
  ps.{{customer_id_col}},
  ps.net_sales_12m,
  ps.average_order_value_12m AS aov,
  ps.completed_orders_12m AS order_count,
  ps.days_since_last_purchase,
  ps.purchase_window_status,
  cn.loyalty_tier,
  cn.preferred_channel,
  cn.email_consent_status,
  cn.sms_consent_status,
  cn.push_consent_status,
  cn.in_app_consent_status
FROM {{database}}.{{purchase_summary_table}} ps
LEFT JOIN {{database}}.{{consent_table}} cn
  ON ps.{{customer_id_col}} = cn.{{customer_id_col}}
