# Better Poster Skill

[English](README.md)

Better Poster Skill 帮助 code agent 将论文 PDF、图表截图、论文文本摘录或 LaTeX 源码压缩包转换为 Better Poster 风格的学术海报。

默认模板采用 claim-first 的学术海报结构：白色左右侧栏、一个高饱和中间主视觉区、超大字号的通俗主结论、居中的底部 QR/download 区、左侧理论信息、右侧实验与证据信息，以及在可用时展示于左下角的纯机构校徽。画布刻意保持宽幅，宽度至少为高度的两倍。

## 使用须知与局限性

本仓库当前阶段已经固化了 CUHK style1 基础模板、通用模板规则和一个特定课题示例的经验参数。请注意：本阶段包含特定课题的实例化微调经验，AI 自动生成的特定文本、公式精炼、理论表述和空间分配不保证百分之百契合每位用户的个性化核心意图。用户在正式投稿、展示或分发前，必须根据论文原文、作者偏好、会议规范和最终渲染结果进行人工校验与微调。

本工具适合作为可复用的 poster scaffold 和视觉约束系统；它不会替代作者对科学表述、公式忠实性、引用准确性、图表裁剪和最终版面取舍的判断。

## CUHK 模板预览

![CUHK style1 template](examples/cuhk_mock_style1/style1.png)

## 提供内容

- 可复用的 CUHK style1 海报模板，采用 2:1 宽幅画布和 claim-first 视觉层级。
- 第二种偏 evidence-oriented 的样式，适合需要中间 hero figure 或结果图的论文。
- 可编辑的 LaTeX 输出和独立 HTML 输出；当同时请求两种格式时，二者保持相同视觉结构。
- 一个持续扩充的 `examples/` 示例库，可作为成功布局、信息密度、措辞风格和视觉层级的参考。
- 内置 QR 行、机构校徽、会议标志和机构感知配色支持。这些内容由 code agent 在生成过程中自动处理，用户不需要单独运行资源命令。

## 设计规则

### CUHK Style1

- 固定 2:1 横向画布，采用 23/54/23 的左 / 中 / 右三栏结构。
- 左栏包含标题、作者、`Introduction` 和 `Theory`；作者行下方不重复展示 affiliation。
- 中栏只承载超大的通俗主结论和底部 QR/download 行。
- 右栏包含 methodology、results、evidence、conclusion，并以 `References` 作为最后一个 section。
- 当存在可支持的机构标志时，机构身份通过左下角 logo strip 呈现。
- 当存在可匹配的会议或 venue 标志时，会议身份放在右栏底部。
- 可视模板文本保持通用、学术，不包含 "fill this section" 这类解释性占位句。

### 中间主结论

中间主结论是整张海报的 billboard。它应该简洁、通俗，并能在几秒内被理解。优先从论文 conclusion 提炼；agent 可以使用主要实验结果来让 conclusion 更具体。

Style1 始终使用三层视觉色块：

| 层级 | 作用 | 最大可视行数 |
|---|---|---|
| White | 核心结论 | 3 |
| Middle gray | 关键结果或延展 | 2 |
| Lower gray | 最终影响或 takeaway | 1 |

中间文字应在各层之间保持一致的字号、字重和行距。当一句话能自然概括论文时，鼓励使用一句话；但不强制所有论文都压缩成一句。

### Theory 与 References

- 左栏不使用 bullet，包括 theory cards 和紧凑摘要。
- `Theory` 应忠实压缩 propositions、lemmas、theorems、corollaries、assumptions 或关键公式。
- 每个 theory card 后面应跟一行通俗摘要，说明该 statement 在讲什么。
- 左栏引用标签使用 `[author + venue/journal + year]` 的信息结构，例如 `(Shumailov et al., Nature 2024)`，而不是 `[1]` 这类纯数字标签。
- 右栏 `References` section 的视觉权重应低于正文。

## 输入

| 输入 | 可接受示例 | 说明 |
|---|---|---|
| 论文内容 | PDF、LaTeX 源码压缩包、Markdown/text 摘录、粘贴的论文段落 | 生成事实准确的海报时必需。 |
| 输出选择 | `latex`、`html` 或 `both` | 未指定时默认两种格式都输出。 |
| 布局模式 | `style1`、`style2` 或 `auto` | `style1` 是默认的 claim-first 布局。 |
| URLs | Paper、code、project、slides、OpenReview | 用于海报 QR/download 区。 |
| Institution / affiliation | 机构名称或作者 affiliation 文本 | 用于可支持的校徽和配色选择。 |
| Figures / screenshots | 方法图、结果图、定性例子 | 当图像直接支持主结论时使用。 |
| Contact line | 邮箱、项目页、实验室主页 | 提供时放在 QR/download 附近。 |

## 使用方式

让安装了本仓库的 code agent 基于论文材料生成或修改海报。agent 应阅读论文、选择最合适的布局、在可用时集成 QR/branding/palette 资源、在依赖可用时渲染预览，并报告仍需人工检查的占位内容。

示例 prompt：

```text
Use $better-poster to generate an academic conference poster from this paper.

Paper source:
- [attach paper.pdf, provide a LaTeX source archive, or paste paper sections]

Preferences:
- Layout mode: auto
- Output: both LaTeX and HTML
- Paper URL: [optional]
- Code URL: [optional]
- Institution / affiliation: [optional]
- Contact line: [optional]
- Key figures to reuse: [optional]
```

## 输出

根据请求格式和本地依赖，agent 会返回：

- 可编辑的 LaTeX 海报源码。
- 独立 HTML 海报源码。
- 用于视觉检查的 PDF/PNG 预览。
- 当提供 URL 时，集成 QR/download 行。
- 当可支持资源存在时，集成机构和会议 branding。
- 简短的变更摘要、预览位置和仍需人工检查的内容。

预览产物默认生成在仓库外部的 `/tmp/better-poster-preview/`。旧版仓库内 `build/` 目录已被 Git 忽略，可以随时删除。

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R Better-Poster-Skill ~/.codex/skills/better-poster
```

安装后，通过 agent 调用：

```text
Use $better-poster to generate a poster from this paper.
```

## 自动资源处理

code agent 会在生成过程中处理海报资源：

- 根据提供的 paper、code、project 或 slides URL 创建 QR 行。
- 当 affiliation 能匹配到支持资源时，选择机构校徽。
- 当存在匹配资源时，加入会议或 venue 标志。
- 当支持机构配色时使用机构感知配色；否则 agent 会选择高对比度学术配色。

用户只需要提供论文源材料，以及希望反映在海报中的 URL 或 affiliation 信息。

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

## License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this skill and is not a vendored copy of Rafael Bailo's GPL-licensed class.

重新分发生成的 logo 文件前，请检查机构 logo 的版权、商标和署名要求。

欢迎提出 suggestions、issues 和 improvements。

[English](README.md)
