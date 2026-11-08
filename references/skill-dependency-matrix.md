# 90+ 出海细分技能依赖与调度映射矩阵 (Skill Dependency Matrix)

本矩阵系统化梳理了本地与 GitHub (`cnproduct`) 仓库中的专业出海技能，按 **八阶段全生命周期** 进行归类、契约输入输出与动态调用方式定义。

---

## 阶段 1：企业真实基因与资质真理建档 (DNA & Truth)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`exporter-profile-skill`** | Local / GitHub | 深度解析出口商产品目录、工厂产能、公差与认证 | 企业 PDF、官网介绍、质检报告 | `docs/dna/exporter-profile.json` |
| **`product-truth-builder`** | Local / GitHub | 建立经权威核验的 SKU 事实档案与严禁虚构红线 | 规格书、实验报告、MOQ、交期 | `content/public-facts.json` |
| **`ingest-enterprise-assets`** | Local | 多源数字资产解析与非结构化文档结构化提取 | 报价单、PDF、图纸、历史订单 | `content/raw-assets/` 结构化表 |
| **`build-enterprise-knowledge-bases`** | Local | 市场、产品、客户、组织四大专属知识库挂载 | 实体抽取结果 | `knowledge-base/` 向量与索引 |

---

## 阶段 2：目标买家画像、JTBD 与欧亚标准矩阵 (ICP & Standards)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`define-buyer-icp`** | Local / GitHub | 定义采购委员会 4 角色（技师/采购/高管/物流）JTBD | 产品定位、目标国家 | `docs/seo/buyer-strategy.md` |
| **`product-search-mapping-skill`** | Local | 生成海关 HS 编码矩阵与 6 大商业采购分支词树 | 产品主词、目标市场 | `docs/seo/keyword-tree.json` |
| **`analyze-country-market`** | Local | 目标国市场容量、准入法规与强制认证深度分析 | 目标国代码 (US, DE, CIS) | `docs/market/regulatory-matrix.md` |
| **`assess-product-market-fit`** | Local | 对照企业现有 SKU 与目标国偏好规格、关税税率 | 企业 SKU 清单 | `docs/market/pmf-scorecard.json` |
| **`reddit-b2b-b2c-geo-scheduler`** | GitHub (`cnproduct`) | 逆向解构 Reddit 工程师现场失效痛点与高频问答 | 种子词、行业子版块包 | `docs/seo/reddit-pain-points.json` |

---

## 阶段 3：信息架构规划、动态 Sitemaps 与规范标签契约 (IA & Sitemaps)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`B2B Portal Builder with Sitemaps`** | Local / Workspace | 自动化构建树状信息架构、多 Sitemaps 与 Pill 导航 | 栏目规划、品类层级 | `sitemap.xml`, `site-routes.json` |
| **`b2b-geo-portal-builder`** | GitHub (`cnproduct`) | Clean URLs 路由契约、静态着陆页与规范标签互锁 | 路由定义、多语言配置 | 规范 URL 清单、自引用 Canonical 契约 |

---

## 阶段 4：视觉识别系统、反 AI-Slop UI 与设计令牌 (VI & Anti-Slop)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`brandvision`** | Local / Plugin | 工业出海品牌视觉总控、行业原型适配与主色规划 | 行业代码、品牌理念 | `src/styles/design-tokens.css` |
| **`brand-visual-director`** | Local / Plugin | 构图尺寸、Logo 安全区、图实一致性与负向提示词 | 品牌规范 | 视觉指导规范与生图约束 |
| **`svg-logo-designer`** | Local / Plugin | 工业级高精度矢量 Logo、标牌与单色应用导出 | 品牌英文、首字母 | `public/assets/logo.svg` |
| **`layout-typography-auditor`** | Local / Plugin | 排版与中英文字体防错审计、防重叠与边界溢出 | HTML/CSS 代码 | `docs/audit/typography-report.json` |
| **`cc-design`** | Local / Plugin | 跨渠道设计语言一致性审计与硬指标校验 | UI 渲染文件 | 一致性合规评分表 |

---

## 阶段 5：同源静态编译、MA-DPP 欧盟护照与 Clean URLs (SSG & MA-DPP)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`ma-dpp-certification-master`** | Local / GitHub | 依据欧盟 ESPR 与 ISO 15459 建立数字产品护照 | BOM 材料比、循环利用率 | `content/ma_dpp_catalog.json` |
| **`scripts/build_dpp_static_pages.py`** | Built-in | 将 DPP 预渲染为独立静态着陆页 (`/dpp-{sku}`) 与 XML | DPP 目录、目标目录 | `dist/dpp/*.html`, `sitemap-dpp.xml` |
| **`b2b-limestone-geo-site-builder`** | GitHub (`cnproduct`) | 天然石材、文化石垂直独立站编译引擎 | 石材参数、ASTM 标准 | 石材专属静态站与装柜算力 |
| **`wideway-export-site-builder-skill`** | Local | 工业装备与 Master CMS 独立站自动化构建 | 机械参数、视频展厅 | 工业出海整站发布包 |
| **`dingmao-shoes-site-builder`** | GitHub (`cnproduct`) | 鞋服箱包轻工出口独立站编译引擎 | 鞋类 SKU、尺码对照表 | 轻工专属静态整站 |
| **`b2b-foss-lubricants-builder`** | GitHub (`cnproduct`) | 工业润滑油、特种化学品出海门户编译 | 润滑油粘度、DIN/ISO/ГОСТ | 化工出海专属静态整站 |
| **`b2b-stone-machinery-site-builder`** | GitHub (`cnproduct`) | 石材机械与重工装备独立站编译引擎 | 重型机床参数、刀头规格 | 重工机械专属静态整站 |
| **`b2b-bento-geo-site-builder`** | GitHub (`cnproduct`) | 餐饮具、家居日用品出海独立站编译引擎 | 食品级认证、FDA/LFGB | 家居轻工专属静态整站 |
| **`wishtimetoys-site-builder`** | GitHub (`cnproduct`) | 益智玩具出海独立站编译引擎 | EN71、CPSIA 认证、箱规 | 玩具出口专属静态整站 |

---

## 阶段 6：全球多引擎 GEO、五层 AI 端点与知识图谱互锁 (GEO & Graph)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`b2b-gemini-geo-citation-engine`** | GitHub (`cnproduct`) | 0+4 步法算子 (BLUF+IGN, CIT+CGP, MEN+ENT, SOM+FOQ) 与评分 | 编译后 HTML 页面 | `docs/seo/citability-score.json` (目标 $\ge 85$) |
| **`scripts/seo_geo_matrix.py`** | Built-in | 生成 `/llms.txt` (v2)、`/llms-full.txt` 与 `/ai/*.json` | 站点事实数据 | 五层 AI 端点全量文件 |
| **`references/cis-yandex-geo-mastery.md`**| Built-in | Yandex SEO、ГОСТ 标准对照与 Clean-param 规则 | 俄语/中亚市场配置 | Yandex 专属 Webmaster 配置与俄语直答 |

---

## 阶段 7：零摩擦工作台、海运双模算力与 RFQ 守护 (Workbench & RFQ)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`design-commercial-offer`** | Local | 定制无法拒绝的三级商业询盘提案（样品/图纸/整柜） | 企业商务条款、毛利率底线 | `content/commercial-offers.json` |
| **`scripts/design_math.py`** | Built-in | 海运双模装柜算力（外箱体积模式 + 重货限重 26.5T 模式）| 外箱长宽高、毛重、密度 | 装柜测算器与装箱单算法 |
| **`scripts/rfq_daemon.py`** | Built-in | HMAC 算术验证码、5 字段蜜罐诱捕与防刷邮件守护 | 监听端口、接收邮箱 | RFQ 接收微服务与双落盘日志 |

---

## 阶段 8：GSC 自动化取证修复与双循环持续收录飞轮 (GSC & Flywheel)

| 技能名称 (Skill ID) | 来源位置 | 核心职能 | 输入参数 / 契约 | 产出物料 (Artifacts) |
|---|---|---|---|---|
| **`scripts/gsc_ego_operator.js`** | Built-in | 通过 `ego-browser` 自动化排查并一键触发 GSC 6 大原因修复 | 目标域名、Ego Lite 空间 ID | GSC Validation 全部点亮 Started |
| **`cloudflare-indexnow-traffic-optimizer`** | GitHub (`cnproduct`) | IndexNow 秒级收录广播与 40% 冷页动态轮巡唤醒 | 域名、IndexNow API Key | `private/indexnow-state.json` |
| **`reddit-b2b-b2c-geo-scheduler`** | GitHub (`cnproduct`) | 双月度工程师技术问答采矿、专业回复排期与知识引流 | 种子词、产品解决痛点 | `docs/seo/scheduled-reddit-qa.json` |
