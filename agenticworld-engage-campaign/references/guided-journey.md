# Guided marketer journey

## Separate decisions from permissions

Let participants own audience strategy and email messaging. Recommend a concrete option with a short reason and wait for their choice. Questions such as which audience or which message to use are business decisions, not approval to run commands. Keep runtime, discovery, CSV, YAML, mapping and API operations automatic. Do not finalize the campaign's audience or copy before the relevant choice unless the participant already supplied it or delegated it.

Start a fresh run with a new campaign and new audience for every new preparation request unless explicit reuse is requested. Preserve previous runs. Within a continuing run, maintain state for identity, audience decision, content decision, revisions, preview and launch. Persist selected criteria and messaging in campaign state. Reuse decisions on continuation; do not repeat completed questions. Continue independent technical discovery while awaiting a business decision, but do not apply undecided settings. Use the available AskQuestion/AskUserQuestion choice tool or a structured equivalent such as request_user_input for discrete business choices. Keep identity intake in ordinary conversation. If the tool is unavailable, use a concise ordinary-message choice question. Never invoke a choice tool for technical permission.

## 1. Add participant

Collect missing identity in one ordinary message. Save the reusable dataset automatically. Explain the fictional purchase profile briefly and show the actual total. Identity collection is the only intake round; later marketing choices are part of the exercise.

## 2. Understand and choose customers

Read audience-insights.md and compute a comparison from the current run dataset before asking for an audience choice. Compare all active, email-consented overdue customers (recommended) with the subset whose propensity_to_churn >= 0.70. Show the same purchase/consent criteria and actual counts for both. Explain that the higher-risk group overlaps the broader group; these are alternative targeting strategies, not additive segments.

Save and display audience-insights.md, including an evidence table, one representative persona hypothesis per option, Northstar relevance, messaging implications and limitations. A file link alone is not presentation. Explain why the recommendation fits the participant's goal and the observed data; never substitute a generic persona for the analysis. Use only verified fields and brand assets. Keep delivery-address filtering separate from the business comparison.

After displaying the report, open the structured audience choice with these two options:
- All overdue customers (Recommended): Reach the full eligible overdue group for an initial win-back exercise.
- Higher-risk overdue customers: Focus on its subset with a workshop churn score of at least 0.70.

Include each option's computed business-cohort count in its description. Offer only nonempty, evaluable strategies. If data is unavailable or required fields cannot be evaluated, disclose the limitation and retain a provisional strategy rather than inventing a report or count. Do not ask the participant to approve analysis commands.

Wait for the choice. If no data exists, explain the options without inventing counts. If a chosen cohort is empty, explain and offer a meaningful alternative. Never silently relax its criteria.

Separate the business cohort from workshop delivery. The reusable CSV stays intact; retain the selected-cohort artifact for analysis, then intersect with verified delivery addresses. Explain: “This is the business audience for your campaign. During the workshop, eligible sample delivery uses the Amazon SES success simulator; your personalized email goes to your own address.” Show both counts in the preview. If participant is outside the chosen cohort, do not change their attributes or add them silently; explain why and let them choose a fitting cohort or revise their explicitly fictional profile.

## 3. Choose the message

Recommend one coherent direction, not a blank questionnaire. Use the established fictional workshop offer and existing three products. Show subject and opening copy, explain the recommendation, and offer one alternative tone.

> I recommend “Alex, enjoy 20% off your next home refresh” because the discount is immediately clear. The body will focus on refreshing your home and feature the sofa, rug and lamp. Would you like this direction, or a warmer welcome-back message?

Wait for the choice. Treat a clear “Use that recommendation” or “looks good” at this stage as adoption of the recommended message, never launch authorization. Support free-text edits. Do not invent extra discounts, scarcity, prices or catalog facts to make the alternative persuasive. Keep the subject's discount opportunity and body's deal size and 2–3 products required by the brief. Default to the supplied three cards. If participant requests two, adapt only the personal copy and explain the resulting composition; do not modify shared originals.

## 4. Show choice → change → preview

Implement the selected strategy and message automatically. Briefly connect the choice to its concrete effect, e.g. “You chose the welcome-back direction, so I changed the opening to a warmer greeting. The discount and all three product recommendations remain.”

Present the four-section completed campaign review report in launch-review.md with the full rendered email, personalization examples, verified audience and sender/settings. Include selected audience criteria, business-cohort count, actual delivery count and selected message direction. Invite content edits: “You can request changes to any wording. When you are ready to send, say “Launch this campaign.”” Only show launch availability when all gates pass.

On revision, change only affected decisions and regenerate/revalidate the preview. Preserve unrelated choices. A fresh preview is required for material changes; never ask permission to perform its YAML/API updates.

## 5. Launch and result

Execute once after explicit approval to launch the current completed review report. Retain all existing launch gates and reporting rules. After observed delivery completion, ask once whether to show the performance report using the business-choice tool. Follow performance-report.md for the delivery-event query and presentation; if reporting was already requested, generate it directly. Refresh requests re-query and update the same campaign report.

## Shortcut and explicit requests

If the participant says “Use your recommendations for everything” or explicitly delegates audience and content, display the audience insight report, choose the recommended audience and message, explain them briefly, configure automatically and show the preview without intermediate choice questions. Still wait for the final launch instruction.

If the initial prompt already selects audience or message, skip only that decision. If both are selected, display the audience insight report with the supplied selection marked, then proceed to automatic configuration and preview. Do not reopen completed decisions. A request to add a row only should update the CSV and stop there; do not force the campaign journey.

## Structured message-direction choice

Before presenting the choice tool, show the proposed subject and a concise opening preview for each direction. Use the same established 20% offer and three products. Do not call an offer exclusive unless the workshop brief establishes exclusivity.

Ask: “Which direction should your email use?”
- Home refresh (Recommended): Lead with the discount and refreshing the customer's space.
- Welcome back: Use a warmer greeting that emphasizes the relationship while keeping the same offer.

Map the selected option to the content decision and continue automatic configuration. Do not ask the same question again in prose after receiving a tool selection. Allow a custom response where the tool supports it. If no answer is returned, keep the recommended direction provisional, prepare a draft, and expose it in the preview rather than repeatedly asking the same tool question.
