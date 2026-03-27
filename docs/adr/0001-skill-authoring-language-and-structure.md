# ADR 0001: スキル執筆における言語とリポジトリ構造

- Status: accepted
- Date: 2026-03-27
- Related: [AGENTS.md](../../AGENTS.md), [SKILL_TEMPLATE.md](../../SKILL_TEMPLATE.md)

## Context

本リポジトリは複数の Agent Skills をホストし、[Agent Skills](https://agentskills.io/) 形式で配布する。エージェントは通常、起動時に各スキルの **名前と description だけ**を見て関連性を判断し、全文はオンデマンドで読み込む。

一方で、利用者やメンテナは日本語で会話・コミット・PR を書くことが多く、**エージェント向けの説明言語**と**ユーザー向け成果物の言語**が一致しない場面がある。

また、コンテキスト効率のため、SKILL.md に長大な参照を詰め込まない方針が AGENTS.md に既に存在する。

## Decision

1. **SKILL.md およびスキル内の一次ドキュメント**は、エージェントが検索・照合しやすいよう **英語を既定**とする（`description` のトリガー句、見出し、手順）。
2. **ユーザー向けに日本語が必須の成果物**（例: 日本語コミット、日本語 PR タイトル・本文）は、**そのスキル内で明示的に定義する**（`commit-jp`、`create-pr-jp` など）。SKILL 本文は英語のまま、テンプレートや例で日本語を示す。
3. **リポジトリ構造**は AGENTS.md に従う: スキルは `skills/{skill-name}/` の **kebab-case**、`SKILL.md` 固定名、詳細は **`references/`** に分離し、**SKILL.md は概ね 500 行未満**を維持する。

## Options considered

### Option A: スキル本文も含め日本語一本

- Pros: リポジトリの自然言語と一致しやすい
- Cons: ツール横断で description のキーワードマッチが弱くなりやすい; 英語のみのエージェント利用時に不利
- Why not chosen: 本リポジトリの主目的は「エージェントが確実にスキルを引き当てること」であり、執筆言語は英語を優先する

### Option B: すべて英語（コミット・PR も英語スキルのみ）

- Pros: 言語が一つで統一される
- Cons: 利用者が日本語コミット・日本語 PR を求めるユースケースを捨てる
- Why not chosen: 日本語ワークフロー用スキル（`*-jp`）が既に価値を持つため

### Option C: スキルごとに言語を混在させ、ルールなし

- Pros: 柔軟
- Cons: レビューとオンボーディングが困難; AGENTS.md との整合が取りにくい
- Why not chosen: メンテナンスコストが高い

## Consequences

- 新規スキルは **英語の SKILL.md** を前提にレビューする。
- 日本語必須の成果物は **専用スキル名・テンプレ**で表現し、「SKILL 全体を日本語にする」ことで回避しない。
- `references/` への分割が標準パターンになる。

## Rollout / migration

- 既存スキルは段階的に本方針へ寄せる。大規模な書き換えが必要な場合は別 PR とする。
- AGENTS.md の Learned Workspace Facts と本 ADRは同趣旨であり、**長期的には AGENTS の重複箇条書きを本 ADR へのリンクに置き換えてもよい**。

## Validation

- 新規スキル PR で「SKILL.md が英語ベースか」「長文が references に分離されているか」を確認する。
- `npx skills add` 利用者からの「スキルがヒットしない」報告が減ることを目安とする（定性）。

## Rollback / escape hatch

- 個別スキルで「利用者コミュニティが日本語のみ」などの理由で例外が必要な場合は、**そのスキルの SKILL 冒頭に例外理由を英語で 1 段落**記載し、ADR を更新するか別 ADR で上書きする。

## Open questions

- なし（現時点）
