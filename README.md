# dev-util-skills

个人开发与项目协作常用 Codex skills 归档库。

这个仓库用于保存可复用的本地开发技能，覆盖项目治理、需求/API 设计、前端 UI 验收、GitHub 协作、部署、安全审查、交付文档和工具集成等场景。仓库只收录开发相关 skills，不包含 Codex 系统内置目录、插件运行时缓存或项目临时产物。

## 快速使用

任选一种方式安装到本机 Codex skills 目录：

```powershell
git clone https://github.com/wxb250/dev-Util-skills.git
$repo = Resolve-Path .\dev-Util-skills
$dest = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Get-ChildItem -Path (Join-Path $repo "skills") -Directory | ForEach-Object {
  Get-ChildItem -Path $_.FullName -Directory | ForEach-Object {
    Copy-Item -Recurse -Force $_.FullName (Join-Path $dest $_.Name)
  }
}
```

如果只想安装某一个 skill，例如前端关键流程验收：

```powershell
Copy-Item -Recurse .\dev-Util-skills\skills\frontend-ui-quality\frontend-critical-flow-acceptance "$env:USERPROFILE\.codex\skills\"
```

安装后重启 Codex 会话或开启新会话，让技能清单重新加载。

## 推荐核心技能

- `frontend-critical-flow-acceptance`：前端关键用户路径真实浏览器验收，避免“测试过了但用户看到灰屏/空白页/按钮无反应”。
- `architecture-freeze-check`：进入实现前冻结架构边界，减少后期大规模 redesign。
- `redesign-risk-check-zh`：中文项目重构风险检查，适合需求仍在变化时使用。
- `autonomous-development-governor`：复杂开发的自动决策、验证收口和阻断判断，避免能本地验证的事项被过早写成“未做”。
- `user-auth-facility-check`：检查登录、注册、找回密码、会话恢复和账号切换隔离等鉴权基础设施。
- `multi-session-project-coordinator`：多 worker 分工、集成与验收协调。
- `frontend-ui-polish-specialist`：现有前端页面的视觉、布局、响应式和交互精修。
- `api-contract-designer`：从需求或材料设计接口契约。
- `security-threat-model`：面向代码仓库的威胁建模。
- `software-demo-ppt-real-prototype`：基于真实可运行页面制作演示/答辩 PPT。

## 分类

| 分类 | 说明 |
| --- | --- |
| `project-governance` | 项目治理、目标定义、架构冻结、任务拆解、鉴权设施检查、自动收口决策、多会话协调 |
| `requirements-api-design` | 需求材料转设计、领域建模、API 契约与请求样例 |
| `frontend-ui-quality` | 前端 UI 精修、关键流程验收、Playwright、Figma、截图 |
| `github-collaboration` | GitHub 仓库阅读、CI 修复、PR 评论处理、Linear |
| `deployment-devops` | Cloudflare、Netlify、Vercel、Render、Sentry |
| `security` | 安全最佳实践、威胁建模、代码所有权与敏感模块分析 |
| `ai-tooling` | OpenAI/ChatGPT Apps、Context7、Codex 迁移、角色/插件/CLI 创建 |
| `framework-app-dev` | ASP.NET Core、WinUI、Jupyter Notebook |
| `docs-delivery` | 软著材料、演示 PPT、PDF、中文文本人化 |
| `media-specialized-tools` | 语音、转录、宠物/精灵资源 |
| `productivity-integrations` | Notion 知识沉淀、会议情报、研究文档、规格落地 |

完整清单见 [skills-manifest.json](skills-manifest.json)。

## 维护原则

- 只收录可复用的开发相关 skills。
- 不提交 `.system`、`superpowers`、运行时缓存、项目输出、测试结果或依赖目录。
- 新增 skill 时优先保持职责窄、触发条件清晰，避免和已有 skill 重叠。
- 跨多个 skill 的复杂任务优先遵循 `skills/project-governance/_shared/skill-collaboration-protocol.md` 的交接格式。
- 提交前可运行 `python scripts/validate_skills.py` 检查 manifest、frontmatter 和 `agents/openai.yaml`。
- 每个 skill 至少应包含 `SKILL.md`，可选包含 `agents/openai.yaml`、`scripts/`、`references/`、`assets/`。
