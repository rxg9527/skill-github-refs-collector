# README 与日志格式

## README

根目录 `README.md` 使用以下规则：

- 每个真实仓库条目都用 Markdown 可跳转链接：

```md
- [repo-name](https://github.com/owner/repo): 一句话摘要。本地体积：`123M`。
```

- 摘要优先来自仓库 README 首屏，不要写成空泛标题。
- 对于本地存在但不是独立 Git 仓库的条目，可保留并明确标注：

```md
- [Archives](./some/local/path): 本地归档目录，不是独立 Git 仓库。
```

- 对于本地缺失的条目，默认从 README 移除。

## 日志

日志路径固定：

```text
log/YYMMDD.md
```

每个仓库记录以下字段：

- 仓库名
- HTTPS URL
- Star
- Fork
- README 摘要
- 本地体积
- 目标路径
- 执行结果：`cloned` / `relocated` / `skipped_conflict`
- 确认链接

推荐格式：

```md
### [repo-name](https://github.com/owner/repo)

- URL: [https://github.com/owner/repo](https://github.com/owner/repo)
- Star: `1.2k`
- Fork: `345`
- README 摘要: ...
- 本地体积: `123M`
- 目标路径: `...`
- 执行结果: `cloned`
- 确认链接: [repo-name](https://github.com/owner/repo)
```

## 确认

- 优先使用默认浏览器：

```bash
bash scripts/open_github_https.sh 'https://github.com/owner/repo'
```

- 如果默认浏览器无法打开，再在回复中列出链接，并提示查看日志文件。
