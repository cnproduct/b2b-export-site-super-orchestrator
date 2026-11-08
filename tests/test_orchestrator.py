#!/usr/bin/env python3
"""
tests/test_orchestrator.py

Regression test suite for b2b-export-site-super-orchestrator.
"""

import unittest
import json
import shutil
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from skill_registry import audit_registry, get_stage_skills, STAGE_SKILL_MAPPING
from lifecycle_evaluator import evaluate_all, evaluate_stage_1, evaluate_stage_3, evaluate_stage_5

class TestSuperOrchestrator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/test-super-orchestrator")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_registry_coverage(self):
        report = audit_registry()
        self.assertEqual(len(report), 8, "Must cover exactly 8 stages")
        for stage in range(1, 9):
            skills = get_stage_skills(stage)
            self.assertTrue(len(skills) >= 2, f"Stage {stage} must have at least 2 associated skills")

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

        # Stage 3 sitemap setup
        dist_dir = self.test_dir / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        with open(dist_dir / "sitemap.xml", "w") as f:
            f.write("<urlset><url><loc>https://www.example.com/products/item-1</loc></url></urlset>")

        res_s3 = evaluate_stage_3(self.test_dir)
        self.assertTrue(res_s3["passed"])
        self.assertTrue(res_s3["clean_urls"])

        # Stage 5 MA-DPP setup
        with open(dist_dir / "sitemap-dpp.xml", "w") as f:
            f.write("<urlset><url><loc>https://www.example.com/dpp-item-1</loc></url></urlset>")

        res_s5 = evaluate_stage_5(self.test_dir)
        self.assertTrue(res_s5["passed"])

if __name__ == "__main__":
    unittest.main()
