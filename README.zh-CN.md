# repository-review-context-minimap-20260804

## 解决的痛点

大 PR 让人和 AI 都陷入上下文过载，需要先生成一张极小的审查地图。

## 为什么现在值得做

Local-first code intelligence and context reduction are trending because coding agents need fewer tokens and humans need faster review entry points.

## 安装与运行

无需第三方依赖，使用 Python 3.10+。

```bash
python src/repository_review_context_minimap.py --help
python src/repository_review_context_minimap.py examples/changed-files.txt
python src/repository_review_context_minimap.py examples/changed-files.txt --codeowners examples/CODEOWNERS --json
python tests/test_cli.py
```

## 示例

示例输入位于 `examples/`，可运行：

```bash
python src/repository_review_context_minimap.py examples/changed-files.txt
```

## 路线图

- Token budget estimates per area

## 许可证

MIT
