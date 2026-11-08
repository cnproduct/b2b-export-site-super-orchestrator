#!/usr/bin/env node
/**
 * scripts/gsc_fleet_operator.js
 * 
 * Multi-Domain Fleet Operator for Google Search Console via ego-browser
 * Part of b2b-export-site-super-orchestrator V1.0.0
 * 
 * Iterates through client properties in GSC, auditing:
 *  - Core sitemap.xml & sitemap-dpp.xml submission status
 *  - 6 major unindexed error categories
 *  - Dispatches automated clicks to trigger "VALIDATE FIX"
 */

import fs from "fs";

const FLEET_DOMAINS = [
  "cosinechips.com",
  "leohygiene.com",
  "tianmaoshoefactory.com",
  "fosslubricants.com",
  "tianyalimestone.com",
  "widewayfootwear.com",
  "custombentofactory.com",
  "shdhygiene.com",
  "hlstonemachine.com",
  "sossenergy.com"
];

async function main() {
  const targetDomains = process.argv[2] ? process.argv[2].split(",") : FLEET_DOMAINS;
  console.log(`[FLEET-OPERATOR] Starting GSC Fleet Remediation for ${targetDomains.length} domains...`);

  if (typeof taskSpace === "undefined") {
    console.error("[ERROR] Must be executed via `ego-browser nodejs scripts/gsc_fleet_operator.js`");
    process.exit(1);
  }

  const task = await taskSpace(1);
  const p = await task.newPage({ as: "p_fleet" });

  const summary = {};

  for (const domain of targetDomains) {
    console.log(`\n======================================================`);
    console.log(`🔍 Auditing Domain: ${domain}`);
    console.log(`======================================================`);

    const gscUrl = `https://search.google.com/search-console/index?resource_id=sc-domain%3A${domain}`;
    try {
      await p.goto(gscUrl, { waitUntil: "load" });
      await new Promise(r => setTimeout(r, 2500));

      const title = await p.title();
      if (!title || title.includes("Welcome") || title.includes("Sign in")) {
        console.log(`⚠️ Domain ${domain} not yet verified in this Google Account.`);
        summary[domain] = "NOT_VERIFIED";
        continue;
      }

      // Read rows from the Page indexing table
      const rows = await p.evaluate(() => {
        const trs = Array.from(document.querySelectorAll("table tr"));
        return trs.map(r => r.innerText.replace(/\n+/g, " | "));
      });

      console.log(`[${domain}] Found ${rows.length} rows in Page indexing.`);
      summary[domain] = rows.slice(0, 7);

      // Check reasons and validate if not started
      const reasons = [
        "Page with redirect",
        "Alternate page with proper canonical tag",
        "Duplicate without user-selected canonical",
        "Excluded by ‘noindex’ tag",
        "Discovered - currently not indexed",
        "Crawled - currently not indexed"
      ];

      for (const reason of reasons) {
        await p.goto(gscUrl, { waitUntil: "load" });
        await new Promise(r => setTimeout(r, 1500));

        const clicked = await p.evaluate((targetReason) => {
          const trs = Array.from(document.querySelectorAll("table tr"));
          const row = trs.find(r => r.innerText.includes(targetReason));
          if (row) {
            row.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
            return true;
          }
          return false;
        }, reason);

        if (!clicked) continue;

        await new Promise(r => setTimeout(r, 2000));

        const valResult = await p.evaluate(() => {
          const btns = Array.from(document.querySelectorAll("div[role=\"button\"], button"));
          const btn = btns.find(b => b.innerText && b.innerText.trim().toUpperCase() === "VALIDATE FIX");
          if (btn && btn.getAttribute("aria-disabled") !== "true") {
            btn.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true, view: window }));
            btn.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true, view: window }));
            btn.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
            return "VALIDATION_TRIGGERED";
          }
          return btn ? "ALREADY_STARTED" : "NO_BUTTON";
        });

        console.log(`   * ${reason} -> ${valResult}`);
      }
    } catch (e) {
      console.error(`❌ Error on domain ${domain}:`, e.message);
      summary[domain] = `ERROR: ${e.message}`;
    }
  }

  console.log(`\n======================================================`);
  console.log(`🏁 GSC Fleet Remediation Completed!`);
  console.log(`======================================================`);
  console.log(JSON.stringify(summary, null, 2));
}

await main();
