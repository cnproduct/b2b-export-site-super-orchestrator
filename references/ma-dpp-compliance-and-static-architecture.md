# 国际合规、欧盟 MA-DPP 数字产品护照与静态落地页矩阵架构规范

> **合规法源依据**：欧盟生态设计法规 ESPR (EU 2024/1781)、国际物品编码协会 ISO/IEC 15459 标准，以及中关村工信二维码技术研究中心 MA 国家顶级节点标准。

---

## 一、 MA-DPP 数字产品护照在出海 B2B 站点的战略地位

自 2024 年下半年起，欧盟海关、国际买家与大型跨国供应链对于电子元器件、工业石材、日化用品、新能源装备等出口品类，全面启动了数字产品护照（DPP）的硬性验真要求：
1. **绿色通关凭据**：在提单（B/L）与报关单中直接嵌入数字护照统一对象标识符（ISO/IEC 15459 编码）与永久 URI，实现口岸无纸化极速核放；
2. **供应链可信防伪**：以 SHA-256 区块账本哈希固化原材料来源、工厂代号、环保合规声明，杜绝贴牌与产地造假；
3. **搜索引擎与 AI 极高权重**：具备真实第三方实验室送检单号与全量 BOM 化学成分的页面，在 Google E-E-A-T 与大模型（Perplexity / ChatGPT Search）权威性评估中享有最高信任级。

---

## 二、 MA-DPP 数据模型与 21 维核心合规字段规范

每个产品在 `data/ma_dpp_catalog.json` 中必须锁定以下事实结构：

```json
{
  "sku": "COS13487",
  "product_id": "cos13487",
  "product_name": "COS13487EESA Half-Duplex RS-485/RS-422 Transceiver",
  "category": "interface-ic",
  "category_name_en": "Industrial & Automotive Interface ICs",
  "hs_code": "8542.39.00",
  "package": "SOP-8",
  "operating_voltage": "4.5V to 5.5V",
  "esd_rating": "±15kV HBM ESD",
  "iso15459_code": "MA.156.100015.01.COS13487",
  "official_ma_code": "MA.15602.315.1029/10.85423910.COS13487",
  "ledger_hash": "D7E8717216D9A2BA09E0E55340F9A110",
  "dpp_url": "https://www.example.com/dpp-cos13487",
  "node_id": "100015",
  "root_code": "MA.15602.315.1029",
  "manufacturer": "Cosine Nanoelectronics (Fujian) Co., Ltd.",
  "country_of_origin": "China (Fujian)",
  "wikidata_qid": "Q141968126",
  "sgs_certification": {
    "testing_lab": "SGS-CSTC Standards Technical Services Co., Ltd.",
    "report_number": "SGS-CANEC26100001-TY",
    "tested_model_declaration": "COS13487 (MA-DPP Verified)",
    "test_standards": [
      "IEC 61000-4-2 Level 4 Electrostatic Discharge Immunity",
      "EU Directive 2011/65/EU (RoHS 2.0) with amendment (EU) 2015/863",
      "Regulation (EC) No 1907/2006 (REACH SVHC 240 Substances)",
      "JEDEC J-STD-020E Moisture Sensitivity & Reflow Profile 260°C",
      "AEC-Q100 Stress Test Qualification for Automotive Integrated Circuits"
    ],
    "status": "PASS / CERTIFIED"
  },
  "bom_composition": {
    "die": {
      "component": "Semiconductor Silicon Core (Active Die)",
      "material": "Monocrystalline Electronic Grade Silicon (Si >99.9999%)",
      "cas_number": "7440-21-3",
      "weight_percent": "18.5%",
      "rohs_reach": "100% Compliant (Zero SVHC, RoHS 2011/65/EU No Lead/Cadmium)"
    },
    "leadframe": {
      "component": "Substrate Leadframe & External Pins",
      "material": "Oxygen-Free High-Conductivity Alloy Copper (CDA 194 / CuFe2P)",
      "cas_number": "7440-50-8",
      "weight_percent": "56.0%",
      "recyclability": "Grade A (100% Metallurgical Recyclable Circular Alloy)"
    },
    "encapsulation": {
      "component": "Protective Molding Compound (Package Body)",
      "material": "Green Epoxy Molding Compound (Fused Silica SiO2 >80%, Epoxy Resin <15%)",
      "cas_number": "60676-86-0",
      "weight_percent": "24.0%",
      "flammability": "UL94 V-0 Certified Halogen-Free Flame Retardant"
    }
  },
  "circular_economy": {
    "weee_compliance": "EU Directive 2012/19/EU Compliant",
    "msl_rating": "JEDEC MSL-1 (Unlimited Floor Life)",
    "reflow_durability": "3x 260°C Lead-Free Reflow Cycles",
    "carbon_footprint_cradle_to_gate": "0.064 kg CO2e / unit (ISO 14067)"
  },
  "timestamp_verified": "2026-11-06T15:04:34Z"
}
```

---

## 三、 独立静态预渲染落地页矩阵（Static DPP Matrix）

严禁使用带查询参数的 URL（如 `/dpp?id=...`）作为最终索引入口。必须由构建流水线一键生成全量独立的静态 HTML 落地页：

1. **页面命名与 Clean URL**：
   - 物理文件：`dpp-{sku.lower()}.html`
   - 服务器暴露 URL：`https://www.example.com/dpp-{sku.lower()}`（由 Nginx `try_files $uri $uri.html =404;` 零重定向解析）。
2. **页面必须预渲染的四大 DOM 结构**：
   - **Hero 凭证标头**：展示 MA 标识代码、ISO/IEC 15459 统一码、SHA-256 账本哈希、企业法定全称。
   - **SGS/第三方实验室检测清单**：完整展示检测机构、报告单号、5 大测试标准（IEC 61000-4-2 / RoHS / REACH 等）与 PASS 状态。
   - **BOM 材质表**：HTML 语义化表格，逐项列明组件名称、化学材料、CAS 登记号、重量占比、无铅环保结论。
   - **ESG 循环经济指标**：MSL 湿敏等级、耐回流焊温度、废旧可回收率与摇篮到大门（Cradle-to-Gate）碳足迹。
3. **结构化数据（JSON-LD）双重绑定**：
   - `@type: "Product"` 包含品牌、型号、原产地、退换货协议；
   - `@type: "DigitalDocument"` 声明该护照文档为官方有效证明；
   - `@type: "BreadcrumbList"` 构建 Home -> MA-DPP Hub -> SKU Passport 的完整面包屑。

---

## 四、 专属站点地图配置与全站联动

1. **生成 `sitemap-dpp.xml`**：
   - 仅包含护照总汇页（`/ma-dpp`、`/dpp`）及全部独立静态护照页（`priority: 0.85`，`changefreq: weekly`）。
2. **`robots.txt` 声明双站点地图**：
   ```text
   Sitemap: https://www.example.com/sitemap.xml
   Sitemap: https://www.example.com/sitemap-dpp.xml
   Feed: https://www.example.com/feed.xml
   ```
3. **全站主导航与站点地图挂载**：
   - 顶栏或底栏提供 `MA-DPP Hub` 入口；
   - 在 `sitemap.html` 开辟独立的 Pillar 6 专区，全面列出所有料号护照链接。
