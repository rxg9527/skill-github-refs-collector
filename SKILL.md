---
name: github-refs-collector
description: 在当前 `github_refs` 索引仓库中搜索 GitHub 仓库、确认准确地址、使用 HTTPS 克隆、按 README 内容归类到最深层目录、更新 `README.md` 和 `log/YYMMDD.md`，并使用默认浏览器打开 GitHub 页面供人工确认。适用于“帮我找仓库并归类”“克隆这些 GitHub 仓库并更新索引”“把新增仓库写入 README 和日志”这类请求。
---

# GitHub Refs Collector

为当前 `github_refs` 目录体系执行 GitHub 仓库收集、归类、索引维护和确认闭环。

先读取 [`references/taxonomy.md`](references/taxonomy.md) 了解分类规则；更新索引与日志前，读取 [`references/readme-log-format.md`](references/readme-log-format.md)。
如果仓库地址已知，先按 [`references/timeout-policy.md`](references/timeout-policy.md) 估算仓库体积并选择 clone 超时窗口。

## 核心原则

- 只面向当前 `github_refs` 目录体系，不做泛化仓库管理。
- 远端地址统一使用 `HTTPS`；不要保留 `git@...` 作为新克隆仓库的 `origin`。
- 仓库必须落到“最深层分类目录”。
- 没有合适目录时，新增中间分类目录，命名使用“数字 + 中文”。
- `README.md` 里的仓库条目必须是 Markdown 可跳转链接，并带一句摘要。
- `log/YYMMDD.md` 必须记录 URL、Star、Fork、摘要、目标路径和执行结果。
- 人工确认优先使用技能内脚本 `scripts/open_github_https.sh` 调用 macOS 默认浏览器
- `git clone` 使用体积感知的等待窗口；无法估算体积时，默认等待 180 秒。

## 标准流程

### 1. 确认仓库

- 如果用户只给仓库名，先搜索 GitHub，确认唯一仓库地址。
- 如果用户给了完整 URL，直接使用该 URL。
- 记录最终仓库的 HTTPS 地址。
- 如果能直接从 URL 识别 `owner/repo`，先读取 GitHub 仓库元数据中的 `size` 作为粗略体积。
- 读取 GitHub 页面上的 `star` 和 `fork`，不要从本地推断。

### 2. 本地查重

- 在 `github_refs` 根目录下搜索同名目录和同远端 URL。
- 如果已经存在且远端一致，不重复克隆；直接复用并移动到正确分类目录。
- 如果目标路径已有不相关目录占用，不覆盖，标记为冲突并写入日志。

### 3. 分类

- 先读仓库 README 首屏和项目描述，再决定分类。
- 分类时绑定当前目录树，优先复用已有目录。
- 没有合适目录时，新增最小必要层级，并保持命名风格与现有目录一致。
- 具体分类规则见 [`references/taxonomy.md`](references/taxonomy.md)。

### 4. 克隆或搬迁

- 新仓库统一使用：

```bash
git clone https://github.com/owner/repo <target-path>
```

- 克隆时先按 [`references/timeout-policy.md`](references/timeout-policy.md) 选择等待窗口。
- 如果选择的窗口内未完成：
  - 中断当前 clone
  - 保留已获得的上下文
  - 停下来向用户说明卡点并等待指示
- 不要为了等 clone 完成而无限轮询或长时间阻塞。
- 完成后校验：

```bash
git -C <target-path> remote get-url origin
```

- 如果结果不是 `https://...`，修正为 HTTPS。

### 5. 更新 README 与日志

- 根目录 `README.md` 只保留本地实际存在的条目，外加用户明确要求保留的本地非标准条目。
- 对真实仓库：
  - 使用 `[repo](https://...)` 形式
  - 附一句摘要
- 对本地存在但不是独立 Git 仓库的条目：
  - 使用本地相对链接
  - 明确标注“不是独立 Git 仓库”或“打包版本目录”
- 对本地缺失条目：
  - 默认移除
- 日志文件固定为 `log/YYMMDD.md`，字段格式见 [`references/readme-log-format.md`](references/readme-log-format.md)。

### 6. 人工确认

- 优先使用默认浏览器打开确认页：

```bash
bash scripts/open_github_https.sh 'https://github.com/owner/repo'
```

- 如果 GUI 打开失败，再退化为：
  - 在回复中列出 GitHub 链接
  - 引导用户查看 `log/YYMMDD.md`

## 脚本

优先复用技能内脚本而不是重复写一遍 README 摘要提取逻辑：

```bash
python3 scripts/extract_repo_meta.py <repo-path> [<repo-path> ...]
bash scripts/open_github_https.sh 'https://github.com/owner/repo'
```

脚本会输出 JSON，包含：

- `name`
- `path`
- `url`
- `summary`

用途：

- 给 `README.md` 生成条目描述
- 给 `log/YYMMDD.md` 填写摘要和 URL
- 批量核对仓库 `origin`
- 以受限方式打开 GitHub 确认页，只允许 `https://github.com/...`

## 输出要求

- 回复里给出本次操作摘要。
- 摘要至少包含：
  - 新增或移动了哪些仓库
  - 更新了哪些目录层级
  - README 和日志是否已更新
  - 是否已打开默认浏览器确认页
