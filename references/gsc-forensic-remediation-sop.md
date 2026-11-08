# Google Search Console 六大未索引根因排查、独立静态预渲染与 ego-browser 自动化运维 SOP

> **适用场景**：外贸 B2B 品牌独立站上线后，Google Search Console（GSC）报表中出现大量“未编入索引（Not indexed）”页面，或需通过 `ego-browser`（Ego Lite）免密接管 GSC 控制台进行批量站点地图提交、验证修正（Start Validation）与加急索引（Request Indexing）。

---

## 一、 GSC 六大未索引分类根因剖析与标准修复矩阵

| GSC 分类状态 | 典型表现 | 根本原因剖析 | 标准技术修复规范 | GSC 运维动作 |
| :--- | :--- | :--- | :--- | :--- |
| **Page with redirect**<br>(网页含有重定向) | 40+ 页 | 网站从 `.html` 后缀迁移为 Clean URLs，或 `http`/non-www 强制 301 重定向留下的历史抓取记录。 | 1. 确保 `sitemap.xml` 中 **100% 直达最终 200 OK，0 个重定向**；<br>2. 站内所有内链、导航、页脚全面剔除 `.html` 后缀；<br>3. Nginx / Cloudflare 边缘实现 0-hop 单跳直达。 | 点击该项 -> 点击 **“验证修正” (VALIDATE FIX)**，让爬虫重检并从历史列表中移除。 |
| **Alternate page with proper canonical tag**<br>(备用网页，有适当的规范标记) | 30–50+ 页 | 1. 产品详情、护照或选型器采用 URL 参数访问（如 `/dpp?id=...`），而公共模板硬编码了主页面 canonical（如 `/dpp`）；<br>2. Googlebot 将数十个参数页视作主页的备用版本，**直接拒绝收录**。 | 1. **全量静态预渲染**：为每个料号生成独立的静态落地页（如 `/dpp-cos13487`）；<br>2. **自引用 Canonical**：页面指向自身无参数 Clean URL；<br>3. **双向内链网格**：产品页与护照页互相通过专属徽章锚定。 | 点击该项 -> 点击 **“验证修正” (VALIDATE FIX)**，Google 将重新确认其为独立规范网页。 |
| **Duplicate without user-selected canonical**<br>(重复网页，用户未选定规范网页) | 8–15 页 | 历史更名文章、测试路径或不同分类目录下的相同内容，未设置 301 重定向或未指定 canonical。 | 1. 在 Nginx 中通过 `map $uri $legacy_redirect` 配置 1-hop 永久 301；<br>2. 检查全站 HTML `<link rel="canonical">` 确保无缺失。 | 点击该项 -> 点击 **“验证修正” (VALIDATE FIX)**，将历史页面权重合并至新版目标页。 |
| **Excluded by ‘noindex’ tag**<br>(已被 'noindex' 标记排除) | 1–3 页 | 后台管理面板（`/admin`）、内部模板或私有报价工具声明了 `<meta name="robots" content="noindex">`。 | **【正常安全行为】**<br>管理后台绝对不能被公共搜索引擎抓取索引，核实确认仅限管理类页面即可。 | **严禁移除 noindex**，无需提交验证，保持排除即可。 |
| **Discovered - currently not indexed**<br>(已发现 - 目前未编入索引) | 50–100+ 页 | Googlebot 已发现 URL（通过 Sitemaps 或外链），但受限于新站日抓取配额（Crawl Budget），处于等待爬取队列中。 | 1. **全网秒级广播**：调用 IndexNow API 批量推送到 Bing、Yandex 及全球网关；<br>2. **内链深度编织**：在 `sitemap.html` 增加专属分类（如 Pillar 6），强化入口权重；<br>3. **双循环持续发布**：每周发布高事实密度工程长文激活蜘蛛。 | 对核心拳头 SKU 使用 **URL Inspection -> Request Indexing** 插队加急通道。 |
| **Crawled - currently not indexed**<br>(已抓取 - 目前未编入索引) | 1–5 页 | Googlebot 抓取后评估该页面内容偏薄（Thin Content）或与全网已有内容语义重叠过高。 | 1. 注入独家量化实测参数表格（`<table>`）；<br>2. 嵌入权威认证标准（ASTM / ISO / CE / RoHS）实测报告单号；<br>3. 增加 BLUF 核心结论前置块与可引用性实体密度。 | 页面丰富后，在 URL Inspection 中点击 **Request Indexing** 重新评估。 |

---

## 二、 动态参数页转独立静态预渲染规范（Anti-Alternate Static Pipeline）

### 1. 架构原则
- **拒绝伪动态参数依赖**：严禁在 `sitemap.xml` 中提交大量带 `?id=`、`?sku=`、`?category=` 的动态查询参数。
- **全量静态生成（SSG）**：将每个商品、数字产品护照（DPP）、合规报告预渲染为独立的静态 `.html` 文件（通过服务器 Clean URL 规则映射为 `/dpp-{sku}`）。
- **三元元数据自洽性**：
  ```html
  <title>{SKU} MA-DPP Digital Product Passport | {BrandName}</title>
  <meta name="description" content="Verified ISO/IEC 15459 & EU ESPR 2024/1781 Digital Product Passport for {SKU}. SGS certified RoHS, REACH, BOM composition.">
  <link rel="canonical" href="https://www.example.com/dpp-{sku}">
  ```

### 2. 双向内链强化拓扑（Bidirectional Link Mesh）
- **从产品详情页指向护照页**：
  ```html
  <a href="/dpp-{sku}" class="btn-dpp-badge">
    🛡️ EU ESPR (2024/1781) & ISO/IEC 15459 Authenticated Passport ↗
  </a>
  ```
- **从护照页指回产品详情页**：
  ```html
  <a href="/product-{sku}" class="btn-action primary">
    View Full Engineering Datasheet & Specs ({SKU}) →
  </a>
  ```
- **站点地图全量索引**：在 `sitemap.html` 中开辟专属板块（如 Pillar 6），以结构化列表完整列出所有静态落地页，确保爬虫 1 次点击即可遍历全量。

---

## 三、 基于 `ego-browser` 的 GSC 自动化免密运维协议

利用用户本地已登录 Google 账号的 `ego lite` 浏览器环境，通过 `ego-browser` 协议实现免 API Key、全自动接管与执行。

### 1. 调度命令流程
```bash
ego-browser nodejs << 'EOF'
// 1. 认领并接管已打开 GSC 的 TaskSpace
const spaces = await listTaskSpaces();
const gscSpace = spaces.find(s => s.recentTabTitles.some(t => t.includes("indexing") || t.includes("Search Console")));
const task = await claimTaskSpace(gscSpace ? gscSpace.id : 1);
const page = task.page("p1");

// 2. 批量提交或刷新多站点地图 (Sitemaps)
await page.goto("https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Aexample.com", { waitUntil: "load" });
const sitemaps = [
  "https://www.example.com/sitemap.xml",
  "https://www.example.com/sitemap-dpp.xml"
];
for (const sm of sitemaps) {
  await page.fill('input[aria-label="Enter sitemap URL"]', sm);
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText.trim().toUpperCase() === 'SUBMIT');
    if (btn) btn.click();
  });
  await page.waitForTimeout(4000);
}

// 3. 遍历未验证项启动 "Validate Fix"
await page.goto("https://search.google.com/search-console/index?resource_id=sc-domain%3Aexample.com", { waitUntil: "load" });
await page.waitForTimeout(3000);

// 点击特定异常分类并触发 VALIDATE FIX
// 针对 Page with redirect, Alternate page, Duplicate without canonical
const triggerValidation = async (rowText) => {
  await page.goto("https://search.google.com/search-console/index?resource_id=sc-domain%3Aexample.com", { waitUntil: "load" });
  await page.evaluate((target) => {
    const trs = Array.from(document.querySelectorAll('table tr'));
    const row = trs.find(r => r.innerText.includes(target));
    if (row) row.click();
  }, rowText);
  await page.waitForTimeout(3000);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
    const b = btns.find(x => x.innerText.trim().toUpperCase() === 'VALIDATE FIX');
    if (b) b.click();
  });
  await page.waitForTimeout(3000);
};

await triggerValidation("Page with redirect");
await triggerValidation("Alternate page with proper canonical tag");
await triggerValidation("Duplicate without user-selected canonical");

// 4. 对核心拳头产品执行加急索引请求 (Request Indexing)
const priorityUrls = [
  "https://www.example.com/product-flagship",
  "https://www.example.com/dpp-flagship"
];
for (const u of priorityUrls) {
  await page.fill('input[aria-label^="Inspect any URL"]', u);
  await page.press('input[aria-label^="Inspect any URL"]', 'Enter');
  await page.waitForTimeout(7000);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
    const b = btns.find(x => x.innerText.trim().toUpperCase().includes('REQUEST INDEXING'));
    if (b) b.click();
  });
  await page.waitForTimeout(8000);
  // 关闭弹窗
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
    const d = btns.find(x => ['DISMISS', 'GOT IT', 'CANCEL'].includes(x.innerText.trim().toUpperCase()));
    if (d) d.click();
  });
}

// 5. 保留操作结果标签页供用户复核
await task.finish({ keep: ["p1"] });
console.log("✅ GSC 自动化免密运维执行完成！");
EOF
```

---

## 四、 持续监控指标与通过标准
- **Sitemap 状态**：`sitemap.xml` 与 `sitemap-dpp.xml` 状态均必须为绿色 `Success`，已发现网址数必须与站点实际 URL 严格对齐。
- **验证流转周期**：点击 `VALIDATE FIX` 后，Googlebot 会在 3~14 天内完成抽样排查，状态将由蓝色的 `Started` 自动流转为绿色的 `Passed`。
- **索引转化率**：健康站点的最终目标为 `Indexed / (Indexed + Not indexed)` 大于 **80%**（除正常排查的后台与历史 301 外，业务产品与指南页面全量收录）。
