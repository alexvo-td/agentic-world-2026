# Guided marketer journey

## Separate decisions from permissions

Let participants own audience strategy and email messaging. Recommend a concrete option with a short reason and wait for their choice. Questions such as which audience or which message to use are business decisions, not approval to run commands. Keep runtime, discovery, CSV, YAML, mapping and API operations automatic. Do not finalize the campaign's audience or copy before the relevant choice unless the participant already supplied it or delegated it.

Start a fresh run with a new campaign and new audience for every new preparation request unless explicit reuse is requested. Preserve previous runs. Within a continuing run, maintain state for identity, audience decision, content decision, revisions, preview and launch. Persist selected criteria and messaging in campaign state. Reuse decisions on continuation; do not repeat completed questions. Continue independent technical discovery while awaiting a business decision, but do not apply undecided settings. Use the available AskQuestion/AskUserQuestion choice tool or a structured equivalent such as request_user_input for discrete business choices. Keep identity intake in ordinary conversation. If the tool is unavailable, use a concise ordinary-message choice question. Never invoke a choice tool for technical permission.

## 1. Add participant

Collect missing identity in one ordinary message. Save the reusable dataset automatically. Explain the fictional purchase profile briefly and show the actual total. Identity collection is the only intake round; later marketing choices are part of the exercise.

## 2. Understand and choose customers

Inspect actual dataset values and show actual eligible business-cohort counts. Recommend all active, email-consented overdue customers as a simple initial win-back audience. Offer the alternative of higher-risk overdue customers; define high risk explicitly as propensity_to_churn >= 0.70 for this workshop, disclose it, and count against actual data. Keep both options within email consent and overdue criteria. Do not describe fictional data as real purchase history.

Example, with computed counts substituted:

> Let's encourage overdue customers to return with 20% OFF. I recommend all customers overdue for their next purchase, so you can assess the response across that audience. Alternatively, we can focus on customers at higher risk of churn. Which audience would you like?

Wait for the choice. If no data exists, explain the options without inventing counts. If a chosen cohort is empty, explain and offer a meaningful alternative. Never silently relax its criteria.

Separate the business cohort from workshop delivery. The reusable CSV stays intact; retain the selected-cohort artifact for analysis, then intersect with verified delivery addresses. Explain: “This is the business audience for your campaign. During the workshop, eligible sample delivery uses the Amazon SES success simulator; your personalized email goes to your own address.” Show both counts in the preview. If participant is outside the chosen cohort, do not change their attributes or add them silently; explain why and let them choose a fitting cohort or revise their explicitly fictional profile.

## 3. Choose the message

Recommend one coherent direction, not a blank questionnaire. Use the established fictional workshop offer and existing three products. Show subject and opening copy, explain the recommendation, and offer one alternative tone.

> I recommend “Alex, enjoy 20% off your next home refresh” because the discount is immediately clear. The body will focus on refreshing your home and feature the sofa, rug and lamp. Would you like this direction, or a warmer welcome-back message?

Wait for the choice. Treat a clear “Use that recommendation” or “looks good” at this stage as adoption of the recommended message, never launch authorization. Support free-text edits. Do not invent extra discounts, scarcity, prices or catalog facts to make the alternative persuasive. Keep the subject's discount opportunity and body's deal size and 2–3 products required by the brief. Default to the supplied three cards. If participant requests two, adapt only the personal copy and explain the resulting composition; do not modify shared originals.

## 4. Show choice → change → preview

Implement the selected strategy and message automatically. Briefly connect the choice to its concrete effect, e.g. “You chose the welcome-back direction, so I changed the opening to a warmer greeting. The discount and all three product recommendations remain.”

Show the rendered personalized email and audience/sender/settings summary. Include selected audience criteria, business-cohort count, actual delivery count and selected message direction. Invite content edits: “You can request changes to any wording. When you are ready to send, say “Launch this campaign.”” Only show launch availability when all gates pass.

On revision, change only affected decisions and regenerate/revalidate the preview. Preserve unrelated choices. A fresh preview is required for material changes; never ask permission to perform its YAML/API updates.

## 5. Launch and result

Execute once after explicit launch instruction for the current completed preview. Retain all existing launch gates and reporting rules.

## Shortcut and explicit requests

If the participant says “Use your recommendations for everything” or explicitly delegates audience and content, choose the recommended audience and message, explain them briefly, configure automatically and show the preview without intermediate choice questions. Still wait for the final launch instruction.

If the initial prompt already selects audience or message, skip only that decision. If both are selected, proceed directly to automatic configuration and preview. A request to add a row only should update the CSV and stop there; do not force the campaign journey.

## Structured message-direction choice

Before presenting the choice tool, show the proposed subject and a concise opening preview for each direction. Use the same established 20% offer and three products. Do not call an offer exclusive unless the workshop brief establishes exclusivity.

Ask: “Which direction should your email use?”
- Home refresh (Recommended): Lead with the discount and refreshing the customer's space.
- Welcome back: Use a warmer greeting that emphasizes the relationship while keeping the same offer.

Map the selected option to the content decision and continue automatic configuration. Do not ask the same question again in prose after receiving a tool selection. Allow a custom response where the tool supports it. If no answer is returned, keep the recommended direction provisional, prepare a draft, and expose it in the preview rather than repeatedly asking the same tool question.
