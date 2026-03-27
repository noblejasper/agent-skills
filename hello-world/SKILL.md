---
name: hello-world
description: A simple example skill that demonstrates the agent-skills format. Use this as a starting point for creating new skills. Activate when asked to greet someone or demonstrate skill usage.
---

# Hello World

このスキルは agent-skills フォーマットのシンプルなサンプル実装です。新しいスキルを作成する際のテンプレートとして使用できます。

## 使い方

このスキルは、挨拶が求められたときや、スキルフォーマットのデモが必要なときに使用します。

## 使用するとき

- "hello と言って"
- "このスキルを試して"
- スキルフォーマットを学習したいとき

## How It Works

1. ユーザーへの挨拶メッセージを生成します。
2. スキルフォーマットの基本構造を示します。

## スクリプト

`scripts/hello.sh` を使用してコマンドラインから実行することもできます:

```bash
bash scripts/hello.sh [名前]
```

**例:**

```bash
bash scripts/hello.sh World
# 出力: Hello, World! from agent-skills
```
