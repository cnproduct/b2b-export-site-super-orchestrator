#!/usr/bin/env python3
"""
tests/test_orchestrator.py

Regression test suite for b2b-export-site-super-orchestrator.
Includes validation for 8-stage skill registry, MA-DPP subsystem,
and default GEO & SEO breadcrumb navigation & Schema.org BreadcrumbList injection.
"""

import unittest
import json
import shutil
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from skill_registry import audit_registry, get_stage_skills, STAGE_SKILL_MAPPING
from lifecycle_evaluator import evaluate_all, evaluate_stage_1, evaluate_stage_3, evaluate_stage_5, evaluate_stage_6
from inject_geo_breadcrumbs import inject_breadcrumbs_into_html, audit_and_inject_fleet

class TestSuperOrchestrator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/test-super-orchestrator")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_registry_coverage(self):
        report = audit_registry()
        self.assertGreaterEqual(len(report), 8, "Must cover at least 8 stages")
        for stage in range(1, 9):
            self.assertIn(f"stage_{stage}", report)
            skills = get_stage_skills(stage)
            self.assertTrue(len(skills) >= 2, f"Stage {stage} must have at least 2 associated skills")

    def test_breadcrumb_injection(self):
        html_sample = """<!DOCTYPE html>
<html>
<head>
  <title>Precision CNC Milling Parts - B2B Manufacturer</title>
</head>
<body>
  <main>
    <h1>Precision CNC Milling Parts</h1>
    <p>Details about milling parts.</p>
  </main>
</body>
</html>"""
        rel_path = "products/precision-cnc-milling-parts.html"
        mod_html, changed = inject_breadcrumbs_into_html(
            html_sample, rel_path, "example.com", "https://www.example.com"
        )
        self.assertTrue(changed)
        self.assertIn("b2b-breadcrumb", mod_html)
        self.assertIn("BreadcrumbList", mod_html)
        self.assertIn("https://www.example.com/products/precision-cnc-milling-parts", mod_html)
        self.assertNotIn(".html", mod_html.split("BreadcrumbList")[1].split("</script>")[0])

    def test_gate_evaluators(self):
        # Empty project
        res_empty = evaluate_all(self.test_dir)
        self.assertLess(res_empty["overall_health_score"], 50.0)

        # Stage 1 facts setup
        content_dir = self.test_dir / "content"
        content_dir.mkdir(parents=True, exist_ok=True)
        with open(content_dir / "public-facts.json", "w") as f:
            json.dump({"module_" + str(i): "val" for i in range(15)}, f)
        
        res_s1 = evaluate_stage_1(self.test_dir)
        self.assertTrue(res_s1["passed"])
        self.assertGreater(res_s1["score"], 70.0)

        # Stage 3 sitemap & breadcrumbs setup
        dist_dir = self.test_dir / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        with open(dist_dir / "sitemap.xml", "w") as f:
            f.write("<urlset><url><loc>https://www.example.com/products/item-1</loc></url></urlset>")

        (self.test_dir / "components").mkdir(parents=True, exist_ok=True)
        with open(self.test_dir / "components" / "breadcrumb.html", "w") as f:
            f.write("<nav class='b2b-breadcrumb'></nav>")

        res_s3 = evaluate_stage_3(self.test_dir)
        self.assertTrue(res_s3["passed"])
        self.assertTrue(res_s3["clean_urls"])
        self.assertTrue(res_s3["breadcrumb_component_ready"])

        # Stage 5 MA-DPP setup (sitemap + catalog + ledger hash)
        with open(dist_dir / "sitemap-dpp.xml", "w") as f:
            f.write("<urlset><url><loc>https://www.example.com/dpp-item-1</loc></url></urlset>")

        data_dir = self.test_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "ma_dpp_catalog.json", "w") as f:
            json.dump({
                "products": [{
                    "sku": "ITEM-1",
                    "node100015_identifier": "100015.CN.EXAMPLE.001",
                    "ledger_hash": "a1b2c3d4e5f67890"
                }]
            }, f)

        res_s5 = evaluate_stage_5(self.test_dir)
        self.assertTrue(res_s5["passed"])

if __name__ == "__main__":
    unittest.main()
