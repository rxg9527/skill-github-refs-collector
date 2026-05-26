# github-refs-collector

一个面向 `github_refs` 索引仓库的收集与归档工作流。

它负责把 GitHub 仓库下载到本地、按内容归类到最深层目录、更新 `README.md` 和每日日志，并打开 GitHub 页面供人工确认。

## 安装说明

- 可以使用 Codex 或 Claude，通过自然语言直接发起安装和操作指令，例如“把 https://github.com/rxg9527/skill-github-refs-collector 安装到我的技能目录”
- 建议根目录名使用 `github_refs`

## 示例调用

### Codex

- `$github-refs-collector 下载 openclaw`
- `$github-refs-collector https://github.com/obra/superpowers`

### Claude Code

- `/github-refs-collector 下载 openclaw`
- `/github-refs-collector https://github.com/obra/superpowers`

## 工作流程

1. 确认仓库地址
2. 评估仓库体积并选择 clone 超时
3. 克隆到正确分类目录
4. 更新 `README.md` 和 `log/YYMMDD.md`
5. 打开 GitHub 页面进行人工确认

## 能做什么

- 搜索并确认 GitHub 仓库地址
- 使用 HTTPS 克隆仓库
- 按 README 内容和现有目录树归类
- 更新根目录 `README.md`
- 记录每日 `log/YYMMDD.md`
- 打开 GitHub 页面进行人工确认

## 目录规则

- 仓库必须放到最深层分类目录
- 现有目录能复用时优先复用
- 没有合适目录时，新增最小必要层级
- 分类规则见 [`references/taxonomy.md`](references/taxonomy.md)

## 推荐模型

建议使用 `gpt-5.4-mini` 或同等轻量模型。

这类任务主要是：
- 读仓库 README
- 做分类判断
- 生成简短摘要
- 维护索引和日志

通常不需要更重的模型，使用轻量模型更省 token，也足够稳定。

## 相关参考

- [`references/taxonomy.md`](references/taxonomy.md)
- [`references/readme-log-format.md`](references/readme-log-format.md)
- [`references/timeout-policy.md`](references/timeout-policy.md)
