# agent-skills

AIコーディングエージェント向けスキルのコレクションです。

スキルは [Agent Skills](https://agentskills.io/) フォーマットに従っています。

## 利用可能なスキル

<!-- スキルを追加する際は、以下の形式で記述してください -->

### gh-pr-review-responder

GitHub の PR レビューコメントを **KEEP / DISCARD** で整理し、返信・必要なら修正まで行うスキルです。

**使用するとき:**

- 開いている PR のレビュースレッドに対応するとき
- `gh-pr-review-responder` や PR レビュー対応を依頼するとき

その他のスキルはリポジトリの [`skills/`](skills/) ディレクトリを参照してください。

---

## インストール

```bash
npx skills add https://github.com/noblejasper/agent-skills --skill gh-pr-review-responder
```

## 使い方

スキルはインストール後、自動的に利用可能になります。エージェントは関連するタスクが検出されたときに自動的にスキルを使用します。

**例:**

```
この PR のレビューコメントに対応して
```

## スキルの構造

各スキルには以下が含まれます:

```
skill-name/
├── SKILL.md         # エージェントへの指示 (必須)
├── scripts/         # 自動化のためのヘルパースクリプト (任意)
└── references/      # 補足ドキュメント (任意)
```

### SKILL.md のフォーマット

`SKILL.md` は YAML フロントマターとMarkdown本文で構成されています:

```markdown
---
name: skill-name
description: スキルの説明。エージェントがいつこのスキルを使うかを明確に記述します。
---

# スキルタイトル

概要説明

## 使い方

...

## 使用するとき

...
```

## 新しいスキルを追加する方法

1. スキル名のディレクトリを作成します (kebab-case)
2. `SKILL.md` を作成し、YAMLフロントマターとMarkdown本文を記述します
3. 必要に応じて `scripts/` や `references/` を追加します
4. このREADMEの「利用可能なスキル」セクションを更新します

テンプレートとして `SKILL_TEMPLATE.md` を参照してください。

## ライセンス

MIT
