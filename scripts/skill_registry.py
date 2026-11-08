#!/usr/bin/env python3
"""
scripts/skill_registry.py

Dynamic Skill Registry & Dependency Resolver for b2b-export-site-super-orchestrator.
Catalogs 90+ specialized B2B export, site-building, SEO, GEO, and verification skills
across local configurations and cnproduct GitHub repositories.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

GLOBAL_SKILLS_DIR = Path.home() / ".gemini" / "config" / "skills"
PLUGINS_SKILLS_DIR = Path.home() / ".gemini" / "config" / "plugins"

STAGE_SKILL_MAPPING = {
    1: [
        {"id": "exporter-profile-skill", "role": "Enterprise Product & Factory DNA Ingestion", "tier": "primary"},
        {"id": "product-truth-builder", "role": "SKU Fact Lock & Technical Parameter Verification", "tier": "primary"},
        {"id": "ingest-enterprise-assets", "role": "Multi-Source PDF/Catalog Extraction", "tier": "support"},
        {"id": "build-enterprise-knowledge-bases", "role": "Entity Graph & Vector Knowledge Mount", "tier": "support"},
    ],
    2: [
        {"id": "define-buyer-icp", "role": "Buying Committee 4-Role JTBD & ICP Profiling", "tier": "primary"},
        {"id": "product-search-mapping-skill", "role": "Global HS Code & 6-Branch Commercial Keyword Tree", "tier": "primary"},
        {"id": "analyze-country-market", "role": "Country Market Capacity & Regulatory Compliance", "tier": "support"},
        {"id": "assess-product-market-fit", "role": "Product-Market Fit & Tariff Scorecard", "tier": "support"},
        {"id": "reddit-b2b-b2c-geo-scheduler", "role": "Reverse-Engineered Engineer Failure Pain Points", "tier": "primary"},
    ],
    3: [
        {"id": "B2B Portal Builder with Sitemaps", "role": "Tree Information Architecture & Pill Navigation", "tier": "primary"},
        {"id": "b2b-geo-portal-builder", "role": "Clean URLs Contract & Self-Referencing Canonical Router", "tier": "primary"},
    ],
    4: [
        {"id": "brandvision", "role": "Master B2B Visual System & Archetype Binding", "tier": "primary"},
        {"id": "brand-visual-director", "role": "Composition, Negative Prompts & Image-Fact Consistency", "tier": "support"},
        {"id": "svg-logo-designer", "role": "Precision Vector Logo & Emblem Export", "tier": "support"},
        {"id": "layout-typography-auditor", "role": "Typography & Fluid Clamping Layout Auditor", "tier": "primary"},
        {"id": "cc-design", "role": "Cross-Channel Design Language Audit", "tier": "support"},
    ],
    5: [
        {"id": "ma-dpp-certification-master", "role": "EU ESPR & ISO 15459 Digital Product Passport Data Model", "tier": "primary"},
        {"id": "build_dpp_static_pages.py", "role": "Standalone Static DPP Landing Page & XML Compiler", "tier": "builtin"},
        {"id": "b2b-hygiene-export-site-builder", "role": "Hygiene, Diaper & Medical Nonwoven Export SSG", "tier": "vertical"},
        {"id": "b2b-energy-storage-site-builder", "role": "Commercial BESS & EU Battery Passport SSG", "tier": "vertical"},
        {"id": "b2b-limestone-geo-site-builder", "role": "Limestone / Architectural Stone SSG", "tier": "vertical"},
        {"id": "wideway-export-site-builder-skill", "role": "Machinery, Tactical Boots & Master CMS SSG", "tier": "vertical"},
        {"id": "dingmao-shoes-site-builder", "role": "Footwear & Barefoot Shoes SSG", "tier": "vertical"},
        {"id": "b2b-foss-lubricants-builder", "role": "Lubricants & Chemical Industry SSG", "tier": "vertical"},
        {"id": "b2b-stone-machinery-site-builder", "role": "Heavy Industrial Stone Machinery SSG", "tier": "vertical"},
        {"id": "b2b-bento-geo-site-builder", "role": "Bento / Tableware & Houseware SSG", "tier": "vertical"},
        {"id": "wishtimetoys-site-builder", "role": "Educational Toys & Consumer Goods SSG", "tier": "vertical"},
    ],
    6: [
        {"id": "b2b-gemini-geo-citation-engine", "role": "0+4 GEO Citation Operators (BLUF, IGN, MEN, ENT, SOM, FOQ)", "tier": "primary"},
        {"id": "seo_geo_matrix.py", "role": "Five-Layer AI Endpoints (/llms.txt v2 & /ai/*.json) Generator", "tier": "builtin"},
        {"id": "cis-yandex-geo-mastery", "role": "GOST vs DIN vs ISO & Yandex Clean-param Strategy", "tier": "builtin"},
    ],
    7: [
        {"id": "design-commercial-offer", "role": "3-Tier Risk Reversal Commercial Inquiry Matrix", "tier": "primary"},
        {"id": "design_math.py", "role": "Dual-Mode Freight Container Logistics Calculator", "tier": "builtin"},
        {"id": "rfq_daemon.py", "role": "HMAC Honeypot Anti-Spam RFQ Microservice", "tier": "builtin"},
    ],
    8: [
        {"id": "gsc_ego_operator.js", "role": "Single Site GSC Validation Trigger (All 6 Reasons)", "tier": "builtin"},
        {"id": "gsc_fleet_operator.js", "role": "Multi-Domain Fleet GSC Automated Remediation", "tier": "builtin"},
        {"id": "fleet_site_auditor.py", "role": "28 Customer Sites Automated Diagnostic Scanner", "tier": "builtin"},
        {"id": "cloudflare-indexnow-traffic-optimizer", "role": "IndexNow Instant Push & 40% Cold-Page Boost", "tier": "primary"},
        {"id": "reddit-b2b-b2c-geo-scheduler", "role": "Bi-Monthly Engineer Citation & Knowledge Nurture", "tier": "primary"},
    ],
}

def scan_installed_skills() -> Dict[str, Path]:
    installed = {}
    if GLOBAL_SKILLS_DIR.exists():
        for item in GLOBAL_SKILLS_DIR.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                installed[item.name] = item

    if PLUGINS_SKILLS_DIR.exists():
        for plugin in PLUGINS_SKILLS_DIR.iterdir():
            skills_sub = plugin / "skills"
            if skills_sub.exists() and skills_sub.is_dir():
                for item in skills_sub.iterdir():
                    if item.is_dir() and (item / "SKILL.md").exists():
                        installed[item.name] = item
    return installed

def get_stage_skills(stage_num: int) -> List[Dict[str, Any]]:
    return STAGE_SKILL_MAPPING.get(stage_num, [])

def audit_registry() -> Dict[str, Any]:
    installed = scan_installed_skills()
    report = {}
    for stage, skills in STAGE_SKILL_MAPPING.items():
        report[f"stage_{stage}"] = []
        for s in skills:
            sid = s["id"]
            tier = s["tier"]
            is_installed = sid in installed or tier == "builtin"
            report[f"stage_{stage}"].append({
                "id": sid,
                "role": s["role"],
                "tier": tier,
                "available": is_installed,
                "path": str(installed.get(sid, "Built-in / Script"))
            })
    return report

if __name__ == "__main__":
    report = audit_registry()
    print(json.dumps(report, indent=2, ensure_ascii=False))
