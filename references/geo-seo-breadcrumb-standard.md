# B2B GEO & SEO Responsive Breadcrumb Navigation Standard (V1.3.0)

> **适用范围**: 所有新建与存量出海 B2B 独立站、SSG 静态编译落地页、MA-DPP 数字产品护照页面及多语种分站。  
> **核心目标**: 同时满足 **Google 传统搜索引擎优化 (SEO - BreadcrumbList Rich Snippet)** 与 **生成式引擎优化 (GEO - ChatGPT Search, Perplexity, Claude, Google AI Overviews 实体隶属链引用)** 的严苛标准。

---

## 一、架构设计哲学与规范要点

在出海 B2B 场景中，海外大采购商与 AI 爬虫在评估供应商时，最忌讳“孤岛页面”与模糊的层级关系。面包屑导航必须在**前端视觉层**与**底层语义层**实现 1:1 精准互锁：

1. **WAI-ARIA 语义可访问性**:
   - `<nav class="b2b-breadcrumb" aria-label="Breadcrumb">`
   - `<ol class="b2b-breadcrumb-list">` 有序列表，明确体现层级先后递进关系。
   - 最后一级（当前页面）标明 `aria-current="page"`，且设为非可点击文本（`pointer-events: none`），防止无效自循环跳转。
   - 分隔符 `<span class="b2b-breadcrumb-separator" aria-hidden="true">/</span>` 明确标记 `aria-hidden="true"`，防止屏幕阅读器或 AI 爬虫将其读为有声斜杠。
2. **移动端极速横向滑动与防折行 (Touch-Scrolling & Anti-Wrap)**:
   - 移动端默认单行水平铺开（`flex-wrap: nowrap`），支持触摸横向顺滑滚动（`overflow-x: auto; -webkit-overflow-scrolling: touch;`）。
   - 隐藏丑陋滚动条（`-webkit-scrollbar { display: none; }`），单个词条 `white-space: nowrap` 严禁折行断裂。
   - 桌面端（`min-width: 768px`）自适应换行，确保大屏长标题展示自然。
3. **Schema.org JSON-LD 强校验规范**:
   - 类型为 `@type: "BreadcrumbList"`。
   - 每个节点的 `item` 字段严格使用**规范绝对 Clean URL（严禁携带 `.html` 后缀或动态参数 `?id=...`）**，与页面 canonical 标签 100% 一致。
   - 最后一项的 `item` 指向当前页绝对规范路径，`name` 与页面核心 H1 / 主题紧密咬合。
4. **多语种与 RTL 镜像支持**:
   - 针对阿拉伯语（`/ar/`）等从右至左语言，CSS 通过 `[dir="rtl"] .b2b-breadcrumb-separator { transform: scaleX(-1); }` 自动水平翻转分隔符。

---

## 二、前端 HTML 视觉组件标准模版

放置于每个内容页面的 **主标题 `<h1>` 正上方**（通常位于 `<main>` 容器开头或 Hero 区域顶部）：

```html
<!-- B2B Responsive Location-Based Breadcrumb Navigation for SEO & GEO -->
<nav class="b2b-breadcrumb" aria-label="Breadcrumb">
  <ol class="b2b-breadcrumb-list">
    <li class="b2b-breadcrumb-item">
      <a href="https://www.example.com/" class="b2b-breadcrumb-link">
        <svg class="b2b-breadcrumb-icon" viewBox="0 0 20 20" fill="currentColor" width="14" height="14" aria-hidden="true">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
        </svg>
        <span>Home</span>
      </a>
      <span class="b2b-breadcrumb-separator" aria-hidden="true">/</span>
    </li>
    
    <li class="b2b-breadcrumb-item">
      <a href="https://www.example.com/products" class="b2b-breadcrumb-link">Products</a>
      <span class="b2b-breadcrumb-separator" aria-hidden="true">/</span>
    </li>
    
    <!-- 最后一级：当前页面（不可点击，明确语义化 current page） -->
    <li class="b2b-breadcrumb-item b2b-breadcrumb-current" aria-current="page">
      <span>Baby Diapers OEM Manufacturer</span>
    </li>
  </ol>
</nav>
```

---

## 三、响应式 CSS 样式标准

可存放于 `src/styles/breadcrumb.css` 或直接合并入项目全局样式表：

```css
/* ==========================================================================
   B2B SEO & GEO Responsive Breadcrumb Component
   ========================================================================== */
.b2b-breadcrumb {
  margin: 12px 0 20px 0;
  padding: 8px 0;
  font-size: 0.875rem; /* 14px */
  line-height: 1.5;
  color: #64748b; /* slate-500 */
}

.b2b-breadcrumb-list {
  display: flex;
  align-items: center;
  flex-wrap: nowrap; /* 移动端默认单行横向排开 */
  overflow-x: auto;  /* 移动端支持丝滑横向触摸滚动 */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox 隐藏滚动条 */
  list-style: none;
  margin: 0;
  padding: 0;
}

.b2b-breadcrumb-list::-webkit-scrollbar {
  display: none; /* Chrome/Safari 隐藏滚动条 */
}

.b2b-breadcrumb-item {
  display: inline-flex;
  align-items: center;
  white-space: nowrap; /* 防止单个面包屑词条被打断折行 */
}

.b2b-breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #475569; /* slate-600 */
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s ease-in-out;
}

.b2b-breadcrumb-link:hover {
  color: #0284c7; /* sky-600 主题蓝 */
  text-decoration: underline;
}

.b2b-breadcrumb-icon {
  flex-shrink: 0;
  color: #94a3b8;
}

.b2b-breadcrumb-separator {
  margin: 0 8px;
  color: #cbd5e1; /* slate-300 */
  user-select: none;
}

/* 最后一级当前页样式 */
.b2b-breadcrumb-current {
  color: #0f172a; /* slate-900 突出层级深度 */
  font-weight: 600;
  cursor: default;
  pointer-events: none; /* 彻底杜绝可点击性 */
}

/* 桌面端大屏自适应自动折行（若层级很长时） */
@media (min-width: 768px) {
  .b2b-breadcrumb-list {
    flex-wrap: wrap; /* 平板及电脑端自适应折行 */
    overflow-x: visible;
  }
}

/* RTL 语系支持（如阿拉伯语 /ar/） */
[dir="rtl"] .b2b-breadcrumb-separator {
  transform: scaleX(-1);
}
```

---

## 四、Schema.org 结构化数据 (JSON-LD)

放置于 HTML `<head>` 区域内，支持独立 `<script type="application/ld+json">` 或嵌入既有 `@graph` 数组：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://www.example.com/products/baby-diapers-oem#breadcrumb",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Products",
      "item": "https://www.example.com/products"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "OEM Baby Diapers Manufacturer & Wholesale Factory",
      "item": "https://www.example.com/products/baby-diapers-oem"
    }
  ]
}
```

---

## 五、页面层级矩阵映射表 (覆盖所有典型 B2B 场景)

| 页面类型 | 建议层级深度 | 前端展示路径 (Breadcrumb Path) | Schema itemListElement 结构 |
| :--- | :---: | :--- | :--- |
| **产品详情页** | 3 级 | `Home > Products > Baby Diapers OEM` | `Home (/)` → `Products (/products)` → `Product (/products/baby-diapers-oem)` |
| **技术白皮书/新闻** | 3 级 | `Home > Technical Guides > Whitepaper` | `Home (/)` → `Technical Guides (/whitepapers)` → `Article (/news/guide-01)` |
| **企业资质/验厂** | 2 级 | `Home > Certifications` | `Home (/)` → `Certifications (/certifications)` |
| **MA-DPP 数字护照** | 3 级 | `Home > MA-DPP Registry > Passport Pass` | `Home (/)` → `MA-DPP (/ma-dpp)` → `Passport (/dpp/dpp-shd-01)` |
| **多语种分站** | 3 级 | `الرئيسية > المنتجات > حفاضات أطفال` | `Home (/ar/)` → `Products (/ar/products)` → `Product (/ar/products/item)` |

---

## 六、自动化脚本与工具链

在 `b2b-export-site-super-orchestrator` 中，已全面内置自动化注入与审计指令：

```bash
# 1. 针对新项目或存量站点执行全面 Breadcrumbs 扫描与自动注入
python3 scripts/inject_geo_breadcrumbs.py --project /path/to/project --domain example.com --inject

# 2. 仅进行合规审计（不改动任何源码文件）
python3 scripts/inject_geo_breadcrumbs.py --project /path/to/project --dry-run

# 3. 通过 super_orchestrator 统一指令执行
python3 scripts/super_orchestrator.py breadcrumbs --project /path/to/project --domain example.com
```
