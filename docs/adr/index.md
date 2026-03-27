# ADR 索引

本リポジトリのアーキテクチャ関連の意思決定を記録する。

| ADR | Status | Title | Summary |
| --- | --- | --- | --- |
| [0001](./0001-skill-authoring-language-and-structure.md) | accepted | スキル執筆における言語とリポジトリ構造 | SKILL.md は英語を既定とし、日本語成果物は *-jp スキルで明示。kebab-case と references によるコンテキスト分割。 |
| [0002](./0002-git-workflow-skills-composition.md) | accepted | Git ワークフロー系スキルの分割と責務 | push / pull / commit-jp / create-pr-jp を単一責任で分離。push 前に pnpm lint && pnpm test（存在時）。 |

## 関連ドキュメント

- [AGENTS.md](../../AGENTS.md) — エージェント向け運用ルール（本索引と重複する箇条書きあり）
- [SKILL_TEMPLATE.md](../../SKILL_TEMPLATE.md) — 新規スキル用テンプレート
