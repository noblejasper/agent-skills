# Reply templates

Use as starting points; adapt to each thread. **Match the language reviewers use** (Japanese teams → Japanese replies).

For **KEEP vs DISCARD** rules and severity definitions, see [keep-discard-rubric.md](keep-discard-rubric.md).

---

## 0) KEEP vs DISCARD — structure (English)

Use this shape so the decision is explicit:

```text
**Decision: KEEP** | **DISCARD**

**Reasoning:** <1–3 sentences: factual check, severity, diff relevance, actionability>

**KEEP — next step:** <concrete fix or “already addressed at …”>

**DISCARD — why not acting on code:** <which discard rule: LOW / wrong fact / out of diff / vague / linter territory / …>
```

## 0b) KEEP vs DISCARD — structure (日本語)

```text
**判断: KEEP** | **DISCARD**

**理由:** <事実確認・重要度・差分との関連・具体性>

**KEEP — 対応:** <具体的な修正内容、または「… で既に対応済み」>

**DISCARD — コード変更しない理由:** <該当する基準: 重要度 LOW / 事実誤認 / 本 PR の差分外 / 曖昧 / リンタ領域 など>
```

---

## 1) No code change needed (English)

```text
Thanks for the review.
I checked this point and kept the current implementation intentionally because <reason>.
Evidence:
- Behavior: <what happens today>
- Reference: <spec/link/file>
- Risk of change: <why changing now would be worse>
If you still prefer a change, I can prepare a follow-up patch.
```

## 1b) No code change needed (日本語)

```text
レビューありがとうございます。
こちらは <理由> のため、現行実装のままにしています。
根拠:
- 挙動: <現在の動き>
- 参照: <仕様・リンク・ファイル>
- 変更リスク: <今変えるデメリット>
別方針をご希望であれば、フォローアップで対応します。
```

## 2) Already fixed in this PR (English)

```text
Thanks for the feedback.
Addressed in this PR at <commit-or-file-reference>.
What changed:
- <change 1>
- <change 2>
Please re-check when convenient.
```

## 2b) Already fixed in this PR (日本語)

```text
ご指摘ありがとうございます。
<コミットまたはファイル> で対応しました。
変更内容:
- <変更1>
- <変更2>
お手すきで再確認いただけると助かります。
```

## 3) Clarification request (English)

```text
Thanks for the comment.
I want to confirm expected behavior before changing code.
Could you clarify <specific question>?
Current behavior is <current behavior summary>.
```

## 3b) Clarification request (日本語)

```text
コメントありがとうございます。
コードを変える前に期待動作を確認させてください。
<具体的な質問> を教えていただけますか？
現状の挙動は <概要> です。
```

## 4) DISCARD — polite decline with criteria (English)

```text
**Decision: DISCARD**

Thanks for the comment. After checking the code and this PR’s diff, we’re **not** implementing a code change for this thread.

**Reasoning:** <e.g. LOW severity — style preference better handled by linter / comment targets lines not changed in this PR / suggestion is not actionable without a concrete spec.>

We’re resolving this thread; happy to revisit if you have a concrete issue tied to this diff (correctness, security, or IMPORTANT-level behavior).
```

## 4b) DISCARD — 丁寧に見送り（日本語）

```text
**判断: DISCARD**

ご指摘ありがとうございます。コードと本 PR の差分を確認した結果、**このスレッドに対するコード変更は行いません。**

**理由:** <例: 重要度が LOW でリンタ領域 / 本 PR で変更していない行へのコメント / 具体案がなく実装不能 など>

このスレッドは解決にします。差分に紐づく具体的な不具合・セキュリティ・IMPORTANT 相当の点があれば、再度お知らせください。
```

## 5) Blocked reply report to user (English)

```text
I could not post a GitHub reply for this thread.
- Failed command: <command>
- Error summary: <error>
- Draft reply:
<reply text>
```

## 5b) Blocked reply report (日本語)

```text
このスレッドに GitHub へ返信できませんでした。
- 失敗したコマンド: <command>
- エラー概要: <error>
- 送る予定だった返信:
<reply text>
```
