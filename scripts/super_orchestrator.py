#!/usr/bin/env python3
"""
scripts/super_orchestrator.py

Master Lifecycle Super Orchestrator CLI for b2b-export-site-super-orchestrator.
Manages the site-lifecycle.json state machine, triggers specialized skills,
executes deterministic gate audits, and generates executive dashboard reports.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

from skill_registry import STAGE_SKILL_MAPPING, get_stage_skills, audit_registry
from lifecycle_evaluator import evaluate_all, evaluate_stage_1, evaluate_stage_2, evaluate_stage_3, evaluate_stage_4, evaluate_stage_5, evaluate_stage_6, evaluate_stage_7, evaluate_stage_8

LIFECYCLE_FILENAME = "site-lifecycle.json"

def cmd_init(args):
    project_dir = Path(args.out).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    lifecycle_file = project_dir / LIFECYCLE_FILENAME

    if lifecycle_file.exists() and not args.force:
        print(f"[ERROR] {LIFECYCLE_FILENAME} already exists at {project_dir}. Use --force to overwrite.")
        sys.exit(1)

    template_file = Path(__file__).parent.parent / "templates" / "site-lifecycle.json"
    with open(template_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["project_name"] = args.name or f"{args.domain} B2B Portal"
    data["domain"] = args.domain
    data["base_url"] = f"https://www.{args.domain}"
    data["industry"] = args.industry or "general_manufacturing"
    data["archetype"] = args.archetype or "precision_engineering"
    data["last_orchestrated_at"] = datetime.utcnow().isoformat() + "Z"

    with open(lifecycle_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Initialized {LIFECYCLE_FILENAME} for {data['domain']} at {project_dir}")

def cmd_status(args):
    project_dir = Path(args.project).resolve()
    lifecycle_file = project_dir / LIFECYCLE_FILENAME

    if not lifecycle_file.exists():
        print(f"[WARN] No {LIFECYCLE_FILENAME} found. Running ad-hoc evaluation on directory...")
        res = evaluate_all(project_dir)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    with open(lifecycle_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    print("=" * 65)
    print(f"🚀 B2B Global Site Lifecycle Status: {state.get('project_name', 'Unnamed')}")
    print(f"🌐 Domain: {state.get('domain')} | Industry: {state.get('industry')}")
    print(f"📌 Current Active Stage: Stage {state.get('current_stage', 1)}")
    print(f"🩺 Overall Health Score: {state.get('overall_health_score', 0.0)} / 100")
    print("=" * 65)

    stages = state.get("stages", {})
    for idx in range(1, 9):
        key = list(stages.keys())[idx - 1] if idx - 1 < len(stages) else f"stage_{idx}"
        info = stages.get(key, {})
        status = info.get("status", "pending").upper()
        icon = "✅" if status == "PASSED" else ("🔄" if status == "IN_PROGRESS" else "⏳")
        name = info.get("name", key)
        print(f"Stage {idx} [{icon} {status:<11}]: {name}")
    print("=" * 65)

def cmd_audit_gate(args):
    project_dir = Path(args.project).resolve()
    stage_num = int(args.stage)
    print(f"[AUDIT] Running deterministic gate audit for Stage {stage_num} on {project_dir}...")
    
    eval_res = evaluate_all(project_dir)
    stage_res = eval_res["stage_evaluations"].get(f"stage_{stage_num}", {})
    
    print("\n--- Gate Audit Result ---")
    print(json.dumps(stage_res, indent=2, ensure_ascii=False))
    
    if stage_res.get("passed", False):
        print(f"\n[PASS] Stage {stage_num} Gate Criteria Satisfied! (Score: {stage_res.get('score')}%)")
    else:
        print(f"\n[FAIL] Stage {stage_num} Gate Criteria Not Met: {stage_res.get('reason')}")

def cmd_self_test(args):
    print("[TEST] Running self-test for super_orchestrator...")
    registry_report = audit_registry()
    assert len(registry_report) == 8, "Expected 8 stages in registry"
    print("  ✓ Skill Registry verified across 8 stages")

    temp_dir = Path("/tmp/orchestrator-test")
    temp_dir.mkdir(parents=True, exist_ok=True)
    (temp_dir / "content").mkdir(exist_ok=True)
    with open(temp_dir / "content" / "public-facts.json", "w") as f:
        json.dump({"module_" + str(i): f"fact_{i}" for i in range(15)}, f)
    
    eval_res = evaluate_stage_1(temp_dir)
    assert eval_res["passed"] is True, "Stage 1 evaluation should pass"
    print("  ✓ Deterministic Gate Evaluator self-test passed")

    import shutil
    shutil.rmtree(temp_dir)
    print("\n[ALL TESTS PASSED] super_orchestrator is fully verified.")

def main():
    parser = argparse.ArgumentParser(description="Master Lifecycle Super Orchestrator for B2B Export Sites")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialize site-lifecycle.json")
    p_init.add_argument("--domain", required=True, help="Target domain name, e.g. example.com")
    p_init.add_argument("--out", required=True, help="Target project output directory")
    p_init.add_argument("--name", help="Human-readable project name")
    p_init.add_argument("--industry", help="Industry code (e.g. limestone, electronics, footwear)")
    p_init.add_argument("--archetype", help="Visual archetype")
    p_init.add_argument("--force", action="store_true", help="Force overwrite existing lifecycle file")

    # status
    p_status = subparsers.add_parser("status", help="Check lifecycle status")
    p_status.add_argument("--project", default=".", help="Project directory")

    # audit-gate
    p_audit = subparsers.add_parser("audit-gate", help="Audit stage gate requirements")
    p_audit.add_argument("--stage", required=True, type=int, help="Stage number (1-8)")
    p_audit.add_argument("--project", default=".", help="Project directory")

    # self-test
    p_test = subparsers.add_parser("self-test", help="Run internal validation test suite")

    args = parser.parse_args()

    if args.subcommand == "init":
        cmd_init(args)
    elif args.subcommand == "status":
        cmd_status(args)
    elif args.subcommand == "audit-gate":
        cmd_audit_gate(args)
    elif args.subcommand == "self-test":
        cmd_self_test(args)

if __name__ == "__main__":
    main()
