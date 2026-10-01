# Guided marketer journey

## Separate decisions from permissions

Let participants own audience strategy and email messaging. Recommend a concrete option with a short reason and wait for their choice. Questions such as which audience or which message to use are business decisions, not approval to run commands. Keep runtime, discovery, CSV, YAML, mapping and API operations automatic. Do not finalize the campaign's audience or copy before the relevant choice unless the participant already supplied it or delegated it.

Maintain state for identity, audience decision, content decision, revisions, preview and launch. Persist selected criteria and messaging in campaign state. Reuse decisions on continuation; do not repeat completed questions. Continue independent technical discovery while awaiting a business decision, but do not apply undecided settings. Do not use forms or AskUserQuestion.

## 1. Add participant

Collect missing identity in one ordinary message. Save the reusable dataset automatically. Explain the fictional purchase profile briefly and show the actual total. Identity collection is the only intake round; later marketing choices are part of the exercise.

## 2. Understand and choose customers

Inspect actual dataset values and show actual eligible business-cohort counts. Recommend all active, email-consented overdue customers as a simple initial win-back audience. Offer the alternative of higher-risk overdue customers; define high risk explicitly as propensity_to_churn >= 0.70 for this workshop, disclose it, and count against actual data. Keep both options within email consent and overdue criteria. Do not describe fictional data as real purchase history.

Example, with computed counts substituted:

> 再購入の目安を過ぎた顧客に、20% OFFで再訪を促しましょう。「購入間隔を過ぎた顧客全体」がおすすめです。まず広く反応を見ることができます。「離反リスクが高い顧客」に絞ることもできます。今回、どちらを対象にしますか？

Wait for the choice. If no data exists, explain the options without inventing counts. If a chosen cohort is empty, explain and offer a meaningful alternative. Never silently relax its criteria.

Separate the business cohort from workshop delivery. The reusable CSV stays intact; retain the selected-cohort artifact for analysis, then intersect with verified delivery addresses. Explain: “これは施策の対象顧客です。ワークショップでは本人と確認済みテストアドレスにのみ送信します。” Show both counts in the preview. If participant is outside the chosen cohort, do not change their attributes or add them silently; explain why and let them choose a fitting cohort or revise their explicitly fictional profile.

## 3. Choose the message

Recommend one coherent direction, not a blank questionnaire. Use the established fictional workshop offer and existing three products. Show subject and opening copy, explain the recommendation, and offer one alternative tone.

> 割引がすぐ伝わる “Alex, enjoy 20% off your next home refresh” がおすすめです。本文は「お部屋のリフレッシュ」をテーマに、ソファ・ラグ・ランプの3商品を紹介します。この方向で進めますか？ それとも「久しぶりのお客様への特別感」を出しますか？

Wait for the choice. Treat a clear “その案で” or “looks good” at this stage as adoption of the recommended message, never launch authorization. Support free-text edits. Do not invent extra discounts, scarcity, prices or catalog facts to make the alternative persuasive. Keep the subject's discount opportunity and body's deal size and 2–3 products required by the brief. Default to the supplied three cards. If participant requests two, adapt only the personal copy and explain the resulting composition; do not modify shared originals.

## 4. Show choice → change → preview

Implement the selected strategy and message automatically. Briefly connect the choice to its concrete effect, e.g. “特別感を選んだので、冒頭を歓迎する表現に変更しました。割引と3商品の紹介は残しています。”

Show the rendered personalized email and audience/sender/settings summary. Include selected audience criteria, business-cohort count, actual delivery count and selected message direction. Invite content edits: “気になる表現があれば変更できます。送信する場合は『Launch this campaign』と伝えてください。” Only show launch availability when all gates pass.

On revision, change only affected decisions and regenerate/revalidate the preview. Preserve unrelated choices. A fresh preview is required for material changes; never ask permission to perform its YAML/API updates.

## 5. Launch and result

Execute once after explicit launch instruction for the current completed preview. Retain all existing launch gates and reporting rules.

## Shortcut and explicit requests

If the participant says “おすすめで全部進めて” or explicitly delegates audience and content, choose the recommended audience and message, explain them briefly, configure automatically and show the preview without intermediate choice questions. Still wait for the final launch instruction.

If the initial prompt already selects audience or message, skip only that decision. If both are selected, proceed directly to automatic configuration and preview. A request to add a row only should update the CSV and stop there; do not force the campaign journey.
