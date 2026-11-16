#!/usr/bin/env python3
"""
scripts/inject_geo_breadcrumbs.py

B2B SEO & GEO Responsive Breadcrumb Navigation & Schema.org BreadcrumbList Injector.
Automatically audits, scaffolds, and injects compliant WAI-ARIA breadcrumb components
and JSON-LD structured data into all content pages of a B2B export website.

Key Features:
- WAI-ARIA compliant: <nav class="b2b-breadcrumb" aria-label="Breadcrumb">, aria-current="page", aria-hidden="true" on separators
- Responsive CSS: mobile horizontal touch-scroll (overflow-x: auto), anti-wrapping, desktop auto-wrap, RTL language support
- Clean URLs: 100% strict adherence to clean URLs without .html extensions
- Schema.org BreadcrumbList: full hierarchical mapping for Google Search Console & Generative Engine Optimization (GEO)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

BREADCRUMB_CSS = """/* ==========================================================================
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
"""

SECTION_MAPPINGS = {
    "products": "Products",
    "product": "Products",
    "whitepapers": "Technical Whitepapers",
    "whitepaper": "Technical Whitepapers",
    "news": "News & Insights",
    "article": "Industry Articles",
    "articles": "Industry Articles",
    "dpp": "MA-DPP Registry",
    "ma-dpp": "MA-DPP Registry",
    "certifications": "Certifications",
    "factory": "Factory Tour",
    "about": "About Us",
    "contact": "Contact",
    "faq": "FAQ",
    "case-studies": "Case Studies",
    "compliance": "Compliance & Standards",
    "ar": "الرئيسية",
    "es": "Inicio",
    "ru": "Главная",
    "pt": "Início",
    "pt-br": "Início",
    "fr": "Accueil",
}

def clean_url(url: str) -> str:
    """Strips .html, index.html, trailing slash (unless root), and queries."""
    url = url.split("?")[0].split("#")[0]
    if url.endswith("/index.html"):
        url = url[:-11]
    elif url.endswith(".html"):
        url = url[:-5]
    if len(url) > 8 and url.endswith("/") and not url.endswith("://"):
        url = url[:-1]
    return url

def derive_hierarchy_from_path(rel_path: str, domain: str, base_url: str, html_content: str) -> List[Dict[str, str]]:
    """
    Derives breadcrumb items for a given file path.
    Returns a list of dicts: [{"name": ..., "url": ...}, ...]
    """
    # 1. Base root
    clean_base = base_url.rstrip("/")
    items = [{"name": "Home", "url": f"{clean_base}/"}]
    
    # Check language prefix
    parts = Path(rel_path).parts
    clean_parts = [p for p in parts if p not in (".", "index.html", "dist", "public")]
    
    if not clean_parts:
        return items

    # Language prefix handling (e.g. ar/, es/, ru/, pt/, pt-br/, fr/)
    is_localized = clean_parts[0] in ("ar", "es", "ru", "pt", "pt-br", "fr")
    lang_prefix = clean_parts[0] if is_localized else ""
    
    if is_localized:
        loc_names = {
            "ar": "الرئيسية",
            "es": "Inicio",
            "ru": "Главная",
            "pt": "Início",
            "pt-br": "Início",
            "fr": "Accueil",
        }
        items = [{"name": loc_names.get(lang_prefix, "Home"), "url": f"{clean_base}/{lang_prefix}/"}]
        sub_parts = clean_parts[1:]
    else:
        sub_parts = clean_parts

    # If it's just the home or language home page
    if not sub_parts:
        return items

    # Derive leaf name from H1 or <title>
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_content, re.IGNORECASE | re.DOTALL)
    if not title_match:
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
    
    leaf_name = ""
    if title_match:
        # Strip internal tags
        leaf_name = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
        leaf_name = leaf_name.split("|")[0].split("-")[0].strip()
        leaf_name = re.sub(r"\s+", " ", leaf_name)

    # Walk intermediate directories
    current_path_acc = f"{clean_base}/{lang_prefix}" if is_localized else clean_base
    for i, part in enumerate(sub_parts[:-1]):
        part_clean = part.replace("-", " ").title()
        sec_name = SECTION_MAPPINGS.get(part.lower(), part_clean)
        current_path_acc = f"{current_path_acc}/{part}"
        items.append({
            "name": sec_name,
            "url": clean_url(current_path_acc)
        })

    # Last part (current page)
    last_segment = sub_parts[-1]
    if last_segment.endswith(".html"):
        last_slug = last_segment[:-5]
    else:
        last_slug = last_segment

    if last_slug == "index":
        # It's an index page of a category
        if len(items) > 1:
            items[-1]["name"] = leaf_name or items[-1]["name"]
        return items

    current_page_url = clean_url(f"{current_path_acc}/{last_slug}")
    leaf_display = leaf_name or last_slug.replace("-", " ").title()
    items.append({
        "name": leaf_display,
        "url": current_page_url
    })

    return items

def generate_breadcrumb_html(items: List[Dict[str, str]]) -> str:
    """Generates the semantic responsive HTML breadcrumb navigation."""
    if len(items) <= 1:
        return ""

    html = ['<!-- B2B Responsive Location-Based Breadcrumb Navigation for SEO & GEO -->']
    html.append('<nav class="b2b-breadcrumb" aria-label="Breadcrumb">')
    html.append('  <ol class="b2b-breadcrumb-list">')

    # Root Home item with icon
    home_item = items[0]
    html.append('    <li class="b2b-breadcrumb-item">')
    html.append(f'      <a href="{home_item["url"]}" class="b2b-breadcrumb-link">')
    html.append('        <svg class="b2b-breadcrumb-icon" viewBox="0 0 20 20" fill="currentColor" width="14" height="14" aria-hidden="true">')
    html.append('          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />')
    html.append('        </svg>')
    html.append(f'        <span>{home_item["name"]}</span>')
    html.append('      </a>')
    html.append('      <span class="b2b-breadcrumb-separator" aria-hidden="true">/</span>')
    html.append('    </li>')

    # Intermediate items
    for item in items[1:-1]:
        html.append('    <li class="b2b-breadcrumb-item">')
        html.append(f'      <a href="{item["url"]}" class="b2b-breadcrumb-link">{item["name"]}</a>')
        html.append('      <span class="b2b-breadcrumb-separator" aria-hidden="true">/</span>')
        html.append('    </li>')

    # Current leaf page
    current = items[-1]
    html.append('    <li class="b2b-breadcrumb-item b2b-breadcrumb-current" aria-current="page">')
    html.append(f'      <span>{current["name"]}</span>')
    html.append('    </li>')

    html.append('  </ol>')
    html.append('</nav>')
    return "\n".join(html)

def generate_breadcrumb_schema(items: List[Dict[str, str]]) -> Dict[str, Any]:
    """Generates the Schema.org BreadcrumbList structured data object."""
    elements = []
    for idx, item in enumerate(items, start=1):
        elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": item["name"],
            "item": item["url"]
        })

    last_url = items[-1]["url"] if items else ""
    return {
        "@type": "BreadcrumbList",
        "@id": f"{last_url}#breadcrumb",
        "itemListElement": elements
    }

def inject_breadcrumbs_into_html(
    html: str, 
    rel_path: str, 
    domain: str, 
    base_url: str
) -> Tuple[str, bool]:
    """
    Injects breadcrumb navigation HTML, CSS, and JSON-LD schema into a single HTML string.
    Returns (modified_html, was_changed).
    """
    # Do not inject on pure root index pages
    norm_rel = rel_path.replace("\\", "/").strip("/")
    if norm_rel in ("", "index.html", "dist/index.html", "public/index.html"):
        return html, False

    items = derive_hierarchy_from_path(rel_path, domain, base_url, html)
    if len(items) <= 1:
        return html, False

    changed = False
    breadcrumb_nav_html = generate_breadcrumb_html(items)
    breadcrumb_schema_obj = generate_breadcrumb_schema(items)

    # 1. Check / Inject JSON-LD Schema
    # Search for existing ld+json
    ld_json_pattern = re.compile(r'(<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
    ld_matches = list(ld_json_pattern.finditer(html))

    schema_injected = False
    if ld_matches:
        for m in ld_matches:
            try:
                raw_json = m.group(2).strip()
                data = json.loads(raw_json)
                if isinstance(data, dict):
                    if data.get("@type") == "BreadcrumbList":
                        # Already present
                        schema_injected = True
                        break
                    elif "@graph" in data and isinstance(data["@graph"], list):
                        has_bc = any(node.get("@type") == "BreadcrumbList" for node in data["@graph"] if isinstance(node, dict))
                        if not has_bc:
                            data["@graph"].append(breadcrumb_schema_obj)
                            new_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                            repl = f"{m.group(1)}\n{new_json_str}\n{m.group(3)}"
                            html = html[:m.start()] + repl + html[m.end():]
                            schema_injected = True
                            changed = True
                            break
                        else:
                            schema_injected = True
                            break
            except Exception:
                continue

    if not schema_injected:
        # Inject fresh script tag in <head>
        full_schema = {
            "@context": "https://schema.org",
            **breadcrumb_schema_obj
        }
        schema_tag = f'\n  <script type="application/ld+json">\n{json.dumps(full_schema, indent=2, ensure_ascii=False)}\n  </script>'
        if "</head>" in html:
            html = html.replace("</head>", f"{schema_tag}\n</head>", 1)
            changed = True
        elif "<head>" in html:
            html = html.replace("<head>", f"<head>\n{schema_tag}", 1)
            changed = True

    # 2. Check / Inject CSS styles
    if ".b2b-breadcrumb" not in html and "breadcrumb.css" not in html:
        style_block = f"\n<style>\n{BREADCRUMB_CSS}\n</style>"
        if "</head>" in html:
            html = html.replace("</head>", f"{style_block}\n</head>", 1)
            changed = True

    # 3. Check / Inject Visual HTML Component
    if 'class="b2b-breadcrumb"' not in html and 'aria-label="Breadcrumb"' not in html:
        # Find <h1> to place directly above it
        h1_match = re.search(r'(<h1[^>]*>)', html, re.IGNORECASE)
        if h1_match:
            html = html[:h1_match.start()] + f"{breadcrumb_nav_html}\n    " + html[h1_match.start():]
            changed = True
        else:
            # Try <main>
            main_match = re.search(r'(<main[^>]*>)', html, re.IGNORECASE)
            if main_match:
                html = html[:main_match.end()] + f"\n    {breadcrumb_nav_html}\n" + html[main_match.end():]
                changed = True
            elif "<body" in html:
                body_match = re.search(r'(<body[^>]*>)', html, re.IGNORECASE)
                if body_match:
                    html = html[:body_match.end()] + f"\n    {breadcrumb_nav_html}\n" + html[body_match.end():]
                    changed = True

    return html, changed

def audit_and_inject_fleet(project_dir: Path, domain: Optional[str] = None, do_inject: bool = False) -> Dict[str, Any]:
    """Scans and injects breadcrumbs across all HTML files in a project."""
    project_dir = project_dir.resolve()
    
    # Resolve domain & base_url
    lifecycle_file = project_dir / "site-lifecycle.json"
    base_url = ""
    if lifecycle_file.exists():
        try:
            with open(lifecycle_file, "r", encoding="utf-8") as f:
                lc = json.load(f)
            domain = domain or lc.get("domain")
            base_url = lc.get("base_url")
        except Exception:
            pass

    domain = domain or "example.com"
    if not base_url:
        base_url = f"https://www.{domain}"

    # Search for all HTML files
    html_files = []
    for root, dirs, files in os.walk(project_dir):
        # Skip node_modules, .git, venv
        if any(d in root for d in (".git", "node_modules", "venv", "__pycache__")):
            continue
        for f in files:
            if f.endswith(".html"):
                html_files.append(Path(root) / f)

    total_files = len(html_files)
    injected_count = 0
    already_valid_count = 0
    root_pages_skipped = 0
    modified_files = []

    for path in html_files:
        rel_path = str(path.relative_to(project_dir))
        # Skip home pages
        if rel_path in ("index.html", "dist/index.html", "public/index.html"):
            root_pages_skipped += 1
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue

        has_component = 'class="b2b-breadcrumb"' in content or 'aria-label="Breadcrumb"' in content
        has_schema = "BreadcrumbList" in content

        if has_component and has_schema:
            already_valid_count += 1
            continue

        if do_inject:
            new_content, changed = inject_breadcrumbs_into_html(content, rel_path, domain, base_url)
            if changed:
                path.write_text(new_content, encoding="utf-8")
                injected_count += 1
                modified_files.append(rel_path)
        else:
            injected_count += 1
            modified_files.append(rel_path)

    coverage = 100.0 if (total_files - root_pages_skipped == 0) else round(
        ((already_valid_count + (injected_count if do_inject else 0)) / (total_files - root_pages_skipped)) * 100.0, 1
    )

    return {
        "domain": domain,
        "base_url": base_url,
        "project_dir": str(project_dir),
        "total_html_files": total_files,
        "root_pages_skipped": root_pages_skipped,
        "already_valid_count": already_valid_count,
        "modified_or_target_count": injected_count,
        "coverage_percentage": coverage,
        "action": "INJECTED" if do_inject else "AUDITED",
        "modified_files_sample": modified_files[:20]
    }

def main():
    parser = argparse.ArgumentParser(description="B2B SEO & GEO Responsive Breadcrumb Injector (V1.3.0)")
    parser.add_argument("--project", default=".", help="Project root or HTML output directory")
    parser.add_argument("--domain", help="Target domain, e.g. example.com")
    parser.add_argument("--inject", action="store_true", help="Execute in-place file modifications")
    parser.add_argument("--dry-run", action="store_true", help="Audit without modifying files")

    args = parser.parse_args()
    do_inject = args.inject and not args.dry_run

    res = audit_and_inject_fleet(Path(args.project), domain=args.domain, do_inject=do_inject)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
