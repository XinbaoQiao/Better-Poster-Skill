<div align="center">

# CS Conference Maintainer

Turn paper materials into editable CS conference poster drafts with a code agent.

<p>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-0f766e"></a>
  <img alt="Output: LaTeX and HTML" src="https://img.shields.io/badge/output-LaTeX%20%2B%20HTML-2563eb">
  <img alt="Poster style" src="https://img.shields.io/badge/poster-Better%20Poster-7c2d92">
  <img alt="OpenReview QR" src="https://img.shields.io/badge/QR-OpenReview%20ready-a21d16">
</p>

<p>
  <a href="#english">English</a> ·
  <a href="#zh-cn">中文</a> ·
  <a href="#preview">Preview</a> ·
  <a href="#quick-start">Quick Start</a>
</p>

</div>

<a id="preview"></a>

## Preview

<p align="center">
  <img src="examples/cuhk_mock_style1/style1.png" alt="CUHK Better Poster style preview" width="920">
</p>

<a id="english"></a>

## English

CS Conference Maintainer helps a code agent transform paper PDFs, LaTeX source archives, extracted text, figures, screenshots, and project links into polished academic poster drafts.

It is designed for researchers who want a fast, editable poster starting point instead of a blank canvas.

### Highlights

| Feature | Why it helps |
|---|---|
| Branded QR generation | Provide paper, code, project, slides, or OpenReview URLs; the agent creates poster-ready QR codes and places the matching site icon in the center when supported. |
| First-author institution branding | The agent reads affiliation text, prioritizes the first author's institution, and places matching university emblems when available. |
| Paper-aware poster drafting | The agent works from the paper itself, so the poster starts from the actual title, authors, claims, figures, and links instead of generic filler. |
| Example-guided design reuse | New posters can borrow layout patterns from successful examples in `examples/`, helping future papers start from proven visual structures. |
| Editable by default | Outputs stay in LaTeX and/or HTML, so authors can keep refining the poster after the first draft. |

### At A Glance

| You provide | The agent prepares |
|---|---|
| Paper PDF, LaTeX source, or pasted paper sections | Editable poster source files |
| Paper, code, project, slides, or OpenReview links | QR/download area |
| Institution or affiliation text | Institution branding when available |
| Figures, result plots, or screenshots | Poster-ready visual evidence when useful |
| Contact line and presentation preferences | A preview-ready poster draft |

### What This Project Provides

| Area | What you get |
|---|---|
| Templates | Reusable Better Poster-style layouts for claim-first and evidence-focused posters |
| Outputs | LaTeX source, optional standalone HTML, and rendered PDF/PNG previews when local tools are available |
| Assets | QR/download rows, institution marks, conference marks, and a dedicated OpenReview QR icon |
| Examples | A growing `examples/` library that helps the agent reuse successful structures for new papers |

<a id="quick-start"></a>

### Quick Start

Install this repository for Codex:

```bash
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/better-poster
```

Then ask the code agent to generate or revise a poster:

```text
Use $better-poster to generate an academic poster from this paper.

Paper source:
- [attach paper.pdf, provide a LaTeX source archive, or paste paper sections]

Preferences:
- Output: both LaTeX and HTML
- Paper URL: [optional]
- OpenReview URL: [optional]
- Code URL: [optional]
- Institution / affiliation: [optional]
- Contact line: [optional]
- Key figures to reuse: [optional]
```

The agent will read the paper materials, choose a suitable poster structure, integrate available assets, generate the requested source files, and render previews when possible.

### Outputs

Depending on your request and local dependencies, the agent can return:

- Poster source files.
- Rendered previews for visual checking.
- QR/download area connected to your supplied links.
- Institution and conference branding when supported.
- A short summary of generated files, preview locations, and remaining manual checks.

### Author Check

Before submission, presentation, or distribution, manually verify:

| Check | Why it matters |
|---|---|
| Scientific wording and main claims | The poster should match the paper and author intent |
| Formula and theorem compression | Shortened theory must remain faithful |
| Figure cropping and captions | Visual evidence should stay accurate |
| Citation accuracy | References and attributions should be correct |
| Author, venue, institution, and logo usage | Branding may have venue or trademark requirements |
| Final rendered layout | Always inspect the actual PDF/PNG preview |

### References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

### License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this project and is not a vendored copy of Rafael Bailo's GPL-licensed class.

Review institution logo copyright, trademark, and attribution requirements before redistributing generated logo files.

<p align="right"><a href="#cs-conference-maintainer">Back to top</a> · <a href="#zh-cn">中文</a></p>

---

<a id="zh-cn"></a>

## 中文

CS Conference Maintainer 用于帮助 code agent 将论文 PDF、LaTeX 源码、论文文本摘录、图表、截图和项目链接转换为可编辑的学术海报初稿。

它适合希望快速得到高质量海报起点的研究者，而不是从空白页面开始排版。

### 核心特点

| 特点 | 价值 |
|---|---|
| 自动生成带图标的 QR code | 你提供 paper、code、project、slides 或 OpenReview 网址后，agent 会生成适合海报使用的 QR，并在支持时把对应站点图标放到 QR 中央。 |
| 自动匹配第一作者单位校徽 | agent 会从论文或 affiliation 文本中优先识别第一作者单位，并在资源可用时直接放入对应校徽。 |
| 基于论文内容生成海报 | 海报初稿会从论文标题、作者、核心结论、图表和链接出发，而不是套用空泛占位内容。 |
| 参考过往成功示例 | 新论文可以从 `examples/` 中复用已经验证过的布局思路、信息密度和视觉组织方式。 |
| 默认保持可编辑 | 输出保留 LaTeX 和/或 HTML 源码，方便作者继续精修、替换内容和适配会议要求。 |

### 快速概览

| 你提供 | agent 生成 |
|---|---|
| 论文 PDF、LaTeX 源码或粘贴的论文段落 | 可编辑的海报源码 |
| Paper、code、project、slides 或 OpenReview 链接 | QR/download 区域 |
| 机构名称或作者 affiliation | 可匹配时加入机构标识 |
| 图表、结果图或截图 | 适合放入海报的视觉证据 |
| 联系方式和展示偏好 | 可预览的海报初稿 |

### 这个项目提供什么

| 模块 | 内容 |
|---|---|
| 模板 | 可复用的 Better Poster 风格布局，支持主结论优先和证据展示优先两类海报 |
| 输出 | LaTeX 源码、按需生成的独立 HTML，以及本地工具可用时的 PDF/PNG 预览 |
| 资源 | QR/download 区域、机构标识、会议标识，以及专用 OpenReview QR 中心图标 |
| 示例 | 持续扩充的 `examples/`，帮助 agent 为新论文参考过往成功结构 |

### 快速开始

先把本仓库安装到 Codex：

```bash
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/better-poster
```

然后让 code agent 基于论文材料生成或修改海报：

```text
Use $better-poster to generate an academic poster from this paper.

Paper source:
- [attach paper.pdf, provide a LaTeX source archive, or paste paper sections]

Preferences:
- Output: both LaTeX and HTML
- Paper URL: [optional]
- OpenReview URL: [optional]
- Code URL: [optional]
- Institution / affiliation: [optional]
- Contact line: [optional]
- Key figures to reuse: [optional]
```

agent 会阅读论文材料，选择合适的海报结构，整合可用资源，生成所需源码，并在条件允许时渲染预览。

### 输出什么

根据你的请求和本地依赖情况，agent 可以返回：

- 海报源码文件。
- 用于视觉检查的渲染预览。
- 连接到你提供链接的 QR/download 区域。
- 在资源可支持时加入的机构和会议标识。
- 简短的文件变更、预览位置和仍需人工检查内容说明。

### 作者检查

正式投稿、展示或分发前，请人工检查：

| 检查项 | 原因 |
|---|---|
| 科学表述和主结论 | 海报应忠实反映论文和作者意图 |
| 公式、定理和理论压缩 | 压缩后的理论内容仍需准确 |
| 图表裁剪和 caption | 视觉证据不能改变科学含义 |
| 引用准确性 | 参考文献和署名需要正确 |
| 作者、会议、机构和 logo 使用 | 品牌材料可能有会议或商标要求 |
| 最终渲染版面 | 请以实际 PDF/PNG 预览为准 |

### 参考来源

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

### License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this project and is not a vendored copy of Rafael Bailo's GPL-licensed class.

重新分发生成的 logo 文件前，请检查机构 logo 的版权、商标和署名要求。

<p align="right"><a href="#cs-conference-maintainer">Back to top</a> · <a href="#english">English</a></p>
