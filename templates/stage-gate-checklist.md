# 全生命周期 8 阶段交付验收闸门清单 (Stage Gate Checklist)

---

## 阶段 1：企业真实基因与资质真理建档 (DNA & Truth)
- [ ] 21 模块事实档案 `content/public-facts.json` 完整生成
- [ ] 权威资质编号（ISO 9001/CE/RoHS/REACH/ASTM/IATF 16949）100% 具备出证机构代码
- [ ] 工厂基础产能、MOQ 与定制交期明确，无无来源占位符
- [ ] 事实隔离状态：企业事实、公开观察与待验证假设三层标签锁定

---

## 阶段 2：目标买家画像、JTBD 与欧亚标准矩阵 (ICP & Standards)
- [ ] 采购委员会 4 大角色（技术评估者、使用者、商务决策者、物流财务）JTBD 弹药齐全
- [ ] 6 大商业采购意图分支词树已扩展完成，剔除 C 端零碎词
- [ ] 欧亚国际标准（美标 ASTM/ASME vs 德标 DIN vs 欧标 EN vs 俄标 ГОСТ）1:1 转换对照建立
- [ ] Reddit / 行业论坛一线工程师现场失效痛点逆向清单完成提取

---

## 阶段 3：信息架构规划、动态 Sitemaps 与规范标签契约 (IA & Sitemaps)
- [ ] 全站 Clean URLs 规范执行，剥离任何静态 `.html` 后缀
- [ ] 拆分为核心地图 `sitemap.xml` 与独立护照地图 `sitemap-dpp.xml`
- [ ] 100% 页面部署自引用 `<link rel="canonical" href="...">` 强契约
- [ ] 零动态参数 URL（如 `?id=...`）泄漏进公开 Sitemaps

---

## 阶段 4：视觉识别系统、反 AI-Slop UI 与设计令牌 (VI & Anti-Slop)
- [ ] 绑定 4 大工业视觉原型之一，生成 `src/styles/design-tokens.css`
- [ ] Major Third (1.25) `clamp()` 流式字阶与微冷/微暖 OKLCH 中性色配置
- [ ] 坚决清零霓虹渐变字（`bg-clip-text`）与全屏大圆角阴影（`shadow-xl`）
- [ ] 文本对比度达到 WCAG AA 级别（$\ge 4.5:1$），排版审计零错位

---

## 阶段 5：同源静态编译、MA-DPP 欧盟护照与 Clean URLs (SSG & MA-DPP)
- [ ] 单一事实源 `public-facts.json` 编译输出静态页面
- [ ] MA-DPP 欧盟数字产品护照静态预渲染完成（`/dpp-{sku}`），遵循 ISO/IEC 15459
- [ ] 前 1024 字节声明 UTF-8，CSS/JS 绑定内容指纹哈希 `?v={hash}`
- [ ] 离线构建页面在无 JavaScript 状态下完整呈现核心参数表格

---

## 阶段 6：全球多引擎 GEO、五层 AI 端点与知识图谱互锁 (GEO & Graph)
- [ ] 134–167 词 GEO 自包含工程直答块（BLUF+IGN 嵌套）通过率 100%
- [ ] 0–100 分 B2B GEO 可引用性评分审计 $\ge 85$ 分
- [ ] `/llms.txt` (v2 规范)、`/llms-full.txt` 与 `/ai/*.json` 生成完成
- [ ] 企业专属 Wikidata QID 绑定并在 Schema.org `sameAs` 首位建立双向互锁
- [ ] Yandex Webmaster Clean-param 指令与 ГОСТ 俄文参数块就绪

---

## 阶段 7：零摩擦工作台、海运双模算力与 RFQ 守护 (Workbench & RFQ)
- [ ] 首屏提供无需注册的材质预设切换、BOM 选型或装柜测算
- [ ] `design_math.py` 双模装柜算力集成（体积模式 + 重货限重 26.5 吨模式）
- [ ] 三级商业询盘卡（标准样品包 / 定制图纸评估 / 整柜阶梯报价）部署完毕
- [ ] RFQ 接口开启 HMAC 算术防刷验证码与 5 字段蜜罐诱捕

---

## 阶段 8：GSC 自动化取证修复与双循环持续收录飞轮 (GSC & Flywheel)
- [ ] `ego-browser` 自动巡检并一键触发 GSC 6 大未收录原因 Validation（全部显示 Started）
- [ ] IndexNow 官方广播开通，40% 冷页动态轮巡唤醒 (Cold-Page Boost) 激活
- [ ] Reddit 双月度工程师采矿与技术解答调度任务运行中
- [ ] Cloudflare 边缘 Crawler Hints 开启，异常路由 404 熔断器就绪
