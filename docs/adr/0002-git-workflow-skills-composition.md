# ADR 0002: Git ワークフロー系スキルの分割と責務

- Status: accepted
- Date: 2026-03-27
- Related: [AGENTS.md](../../AGENTS.md), [ADR 0001](./0001-skill-authoring-language-and-structure.md)

## Context

本リポジトリは `commit-jp`、`push`、`pull`、`create-pr-jp`、`commit-and-push-jp` など、Git 操作に関するスキルを複数保持する。単一の「なんでも Git スキル」にまとめると、**いつどのスキルを起動すべきか**が曖昧になり、description だけでは誤起動しやすい。

また、スレッド内の合意として **push はリモートへの反映まで**とし、**PR 作成・更新は別スキル（create-pr-jp）**に分けた経緯がある。

## Decision

1. **単一責任**: 各スキルは一つの主目的に絞る。
   - **commit-jp**: コミット（日本語メッセージ、`git commit -F` 等）
   - **push**: `origin` への push、拒否時は **pull** で同期後に再検証
   - **pull**: ベースブランチとのマージ同期・コンフリクト解消
   - **create-pr-jp**: GitHub 上での PR 作成・更新（日本語タイトル・本文、テンプレート利用）
   - **commit-and-push-jp**: コミットと push を一連で行うフロー（PR は含めない）
2. **push は PR を作らない**: PR が必要なら **create-pr-jp** を使う（または push 後にユーザーが明示したときに create-pr-jp）。
3. **push / commit-and-push-jp に共通する検証**: リポジトリに `pnpm lint` / `pnpm test` がある場合は **`pnpm lint && pnpm test`** を push 前に実行する。スクリプトが無いプロジェクトでは AGENTS.md または README の手順に従う。

## Options considered

### Option A: 単一の「git 全部」スキル

- Pros: ユーザーが一発で頼める
- Cons: description が肥大化; 不要なツール実行（PR までやりたくないとき）を引き起こしやすい
- Why not chosen: 起動精度とコンテキスト効率が悪化する

### Option B: push に PR 作成を含める

- Pros: 「出して」の一回で完結
- Cons: gh 認証・テンプレ・本文生成が push と常に結合し、失敗時の切り分けが難しい
- Why not chosen: スレッド内で却下され、create-pr-jp に分離した

### Option C: lint のみ・test なし

- Pros: 速い
- Cons: CI でテストが落ちる変更を push しやすい
- Why not chosen: 利用者ルールおよび push スキルで **lint と test の両方**を採用

## Consequences

- 新規の「Git 系」機能は、既存スキルへの追記か、**責務が明確な新スキル**かの二択で設計する。
- `create-pr-jp` は `.github/pull_request_template.md` または `docs/pull_request_template.md` を参照する（既存スキル定義）。
- **`gh-pr-review-responder`** は **既に開いている PR** のレビューコメント・スレッドに対応する。コード変更があった場合の検証と push 前チェックは **push** と同様に **`pnpm lint && pnpm test`**（スクリプトがある場合）を原則とする。PR の新規作成・タイトル本文の編集は **create-pr-jp** の責務と分離する。

## Rollout / migration

- 既存スキル文言は本 ADR と整合している。変更は不要。

## Validation

- ユーザーが「push したのに PR がない」と誤解する報告が出た場合、**create-pr-jp** の案内を SKILL と AGENTS で強化する。

## Rollback / escape hatch

- モノレポで `pnpm` がルートに無い等の場合は、スキル内に「プロジェクトの標準チェックコマンドに置き換え」と明記し、本 ADR の「pnpm」は例示として扱う。

## Open questions

- `land`（マージ完了まで）のようなスキルを別途追加するかは、利用頻度を見てから。
