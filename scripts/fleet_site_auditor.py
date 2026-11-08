#!/usr/bin/env python3
"""
scripts/fleet_site_auditor.py

Automated Multi-Site Fleet Auditor for b2b-export-site-super-orchestrator.
Performs concurrent health diagnostics across all 28 B2B customer sites, checking:
1. HTTP 200 availability
2. Primary XML sitemap (sitemap.xml)
3. MA-DPP Digital Product Passport XML sitemap (sitemap-dpp.xml)
4. Generative AI citation endpoint (/llms.txt)
5. Search crawler directives (/robots.txt)
"""

import sys
import ssl
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

CUSTOMER_FLEET = [
    {"domain": "cosinechips.com", "name": "科山芯创", "industry": "半导体/模拟芯片"},
    {"domain": "fosslubricants.com", "name": "福斯润滑油", "industry": "工业润滑油/特种油脂"},
    {"domain": "tianyalimestone.com", "name": "天涯文化石", "industry": "天然石灰石/建筑石材"},
    {"domain": "tianmaoshoefactory.com", "name": "天茂鞋业", "industry": "综合鞋业制造/劳保鞋"},
    {"domain": "dingmaoshoes.com", "name": "鼎茂鞋业", "industry": "赤足鞋/五指鞋"},
    {"domain": "widewayfootwear.com", "name": "威德威鞋业", "industry": "战术军警靴/劳保鞋"},
    {"domain": "widewaygroup.com", "name": "威德威集团", "industry": "综合工贸出海集团"},
    {"domain": "widewaybags.com", "name": "威德威箱包", "industry": "战术背包/军用装具"},
    {"domain": "widewaysportswear.com", "name": "威德威服饰", "industry": "功能性运动工装"},
    {"domain": "widewaycorkfootwear.com", "name": "威德威软木鞋", "industry": "环保软木鞋/勃肯拖鞋"},
    {"domain": "widewayfootballgear.com", "name": "威德威足球装备", "industry": "足球装备/运动护具"},
    {"domain": "leohygiene.com", "name": "利奥卫生用品", "industry": "成人失禁/母婴个护"},
    {"domain": "shdhygiene.com", "name": "盛鸿达卫生用品", "industry": "婴儿纸尿裤/经期裤"},
    {"domain": "chinabaronhygiene.com", "name": "男爵卫生用品", "industry": "医护级卫生护理"},
    {"domain": "custombentofactory.com", "name": "定制便当盒工厂", "industry": "不锈钢/硅胶便当盒"},
    {"domain": "eazylunch.com", "name": "EazyLunch 餐厨", "industry": "便携餐盒/儿童餐具"},
    {"domain": "wishtimetoys.com", "name": "智趣玩具", "industry": "婴幼早教/益智玩具"},
    {"domain": "chengjitoy.com", "name": "澄积玩具", "industry": "澄海塑料玩具出口"},
    {"domain": "hlstonemachine.com", "name": "华隆石材机械", "industry": "数控石材切割机床"},
    {"domain": "shengdamachinery.com", "name": "盛达石材机械", "industry": "石材开采与抛光装备"},
    {"domain": "naiketableware.com", "name": "耐客餐厨", "industry": "环保麦秸秆餐具"},
    {"domain": "ghsafetyboots.com", "name": "广汉安全鞋", "industry": "劳保安全工装靴"},
    {"domain": "huifengsanitary.com", "name": "汇丰卫浴", "industry": "卫浴五金/智能龙头"},
    {"domain": "rrenn.com", "name": "人人易 AI", "industry": "外贸 AI 增长平台"},
    {"domain": "earsoon.com", "name": "开思云聚", "industry": "企业 ERP/数智化"},
    {"domain": "jinyuanfire.com", "name": "劲源消防", "industry": "消防器材与阀门"},
    {"domain": "meihuaumbrella.com", "name": "梅花伞业", "industry": "晴雨伞/高尔夫伞"},
    {"domain": "sossenergy.com", "name": "索森能源", "industry": "工商业储能/户储系统"},
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def test_url(url: str, timeout: float = 7.0) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FleetAuditor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            return resp.status == 200
    except:
        return False

def audit_single_site(site: dict) -> dict:
    domain = site["domain"]
    base_www = f"https://www.{domain}"
    base_root = f"https://{domain}"

    is_live = test_url(base_www) or test_url(base_root)
    active_base = base_www if test_url(base_www) else base_root

    has_sitemap = test_url(f"{active_base}/sitemap.xml")
    has_dpp = test_url(f"{active_base}/sitemap-dpp.xml")
    has_llms = test_url(f"{active_base}/llms.txt")
    has_robots = test_url(f"{active_base}/robots.txt")

    score = 0
    if is_live: score += 40
    if has_sitemap: score += 20
    if has_dpp: score += 15
    if has_llms: score += 15
    if has_robots: score += 10

    return {
        "domain": domain,
        "name": site["name"],
        "industry": site["industry"],
        "live": is_live,
        "sitemap": has_sitemap,
        "sitemap_dpp": has_dpp,
        "llms_txt": has_llms,
        "robots_txt": has_robots,
        "health_score": score
    }

def main():
    print(f"=== B2B Global Brand Site Fleet Auditor (Total {len(CUSTOMER_FLEET)} Sites) ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(audit_single_site, site) for site in CUSTOMER_FLEET]
        for f in futures:
            results.append(f.result())

    print(f"{'Domain':<26} | {'Status':<6} | {'Sitemap':<7} | {'DPP Map':<7} | {'llms.txt':<8} | {'Robots':<6} | {'Score':<5}")
    print("-" * 75)

    for r in sorted(results, key=lambda x: x["health_score"], reverse=True):
        st = "✅ LIVE" if r["live"] else "❌ DOWN"
        sm = "✅ 200" if r["sitemap"] else "❌ Miss"
        dpp = "✅ 200" if r["sitemap_dpp"] else "❌ Miss"
        llms = "✅ 200" if r["llms_txt"] else "❌ Miss"
        rob = "✅ 200" if r["robots_txt"] else "❌ Miss"
        print(f"{r['domain']:<26} | {st:<6} | {sm:<7} | {dpp:<7} | {llms:<8} | {rob:<6} | {r['health_score']:<5}")

    live_count = sum(1 for r in results if r["live"])
    dpp_count = sum(1 for r in results if r["sitemap_dpp"])
    llms_count = sum(1 for r in results if r["llms_txt"])

    print("-" * 75)
    print(f"Summary: {live_count}/{len(CUSTOMER_FLEET)} Sites Live | {dpp_count}/{len(CUSTOMER_FLEET)} Have MA-DPP | {llms_count}/{len(CUSTOMER_FLEET)} Have llms.txt")

if __name__ == "__main__":
    main()
