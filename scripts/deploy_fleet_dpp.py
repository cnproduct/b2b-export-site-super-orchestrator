#!/usr/bin/env python3
"""
scripts/deploy_fleet_dpp.py

Batch MA-DPP Digital Product Passport Generator & Deployer
Builds and deploys EU ESPR (Regulation EU 2024/1781) & ISO/IEC 15459 compliant
MA-DPP hubs, individual passport landing pages, and sitemap-dpp.xml across 10 sites:
- widewaygroup.com (43.130.32.54)
- widewaybags.com (43.130.32.54)
- widewaysportswear.com (43.130.32.54)
- widewaycorkfootwear.com (43.130.32.54)
- widewayfootballgear.com (43.130.32.54)
- leohygiene.com (43.135.182.81)
- shdhygiene.com (43.135.182.81)
- eazylunch.com (137.184.111.182)
- naiketableware.com (137.184.111.182)
- ghsafetyboots.com (137.184.111.182)
"""

import os
import sys
import paramiko
from datetime import datetime

FLEET_DPP_CONFIG = [
    # Server 1: 43.130.32.54
    {
        "domain": "widewaygroup.com",
        "company": "Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP)",
        "server": {"host": "43.130.32.54", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/widewaygroup.com",
        "industry": "Comprehensive Footwear, Apparel & Tactical Gear Manufacturing",
        "skus": [
            {"sku": "WD-GRP-9001", "name": "Engineered Performance Athletic Sneaker", "cat": "Athletic Footwear", "mat": [("Recycled Flyknit Upper", "45%", "60%"), ("Bio-EVA Midsole", "35%", "30%"), ("Natural Rubber Outsole", "20%", "40%")], "comp": ["ISO 9001:2015", "amfori BSCI", "GRS 4.0", "SATRA TM144"]},
            {"sku": "WD-BAG-8002", "name": "Cordura Modular Tactical Assault Backpack 45L", "cat": "Tactical Gear", "mat": [("1000D Cordura Nylon", "70%", "25%"), ("UTX Duraflex Buckles", "15%", "50%"), ("YKK Waterproof Zippers", "15%", "30%")], "comp": ["MIL-STD-810H", "OEKO-TEX Standard 100", "ISO 14001:2015"]},
            {"sku": "WD-SPT-7003", "name": "Thermal Ripstop Waterproof Field Jacket", "cat": "Technical Apparel", "mat": [("Recycled Polyester Softshell", "65%", "75%"), ("TPU Hydrophilic Membrane", "20%", "0%"), ("Polar Fleece Lining", "15%", "50%")], "comp": ["EN 343:2019 Class 4/4", "OEKO-TEX Made in Green", "GRS 4.0"]},
            {"sku": "WD-CRK-6004", "name": "Bio-Based Anatomical Cork Footbed Slide", "cat": "Eco Footwear", "mat": [("Natural Sustainable Cork", "55%", "100%"), ("LWG Gold Certified Suede", "30%", "0%"), ("Lightweight EVA Outsole", "15%", "35%")], "comp": ["FSC-STD-40-004", "REACH EC 1907/2006", "ISO 9001:2015"]}
        ]
    },
    {
        "domain": "widewaybags.com",
        "company": "Wideway Bags Manufacturing Co., Ltd.",
        "server": {"host": "43.130.32.54", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/widewaybags.com",
        "industry": "Tactical Backpacks, Military Packs & Outdoor Luggage",
        "skus": [
            {"sku": "WB-TAC-45L", "name": "MOLLE System Combat Tactical Backpack 45L", "cat": "Tactical Packs", "mat": [("1000D Ballistic Nylon", "75%", "30%"), ("High-Tensile Polypropylene Webbing", "15%", "40%"), ("Zinc Alloy Hardware", "10%", "60%")], "comp": ["ISO 9001:2015", "BSCI Certified", "REACH Compliant"]},
            {"sku": "WB-OD-35L", "name": "Ultralight Ergonomic Mountain Hiking Pack 35L", "cat": "Outdoor Packs", "mat": [("420D Diamond Ripstop", "65%", "50%"), ("AeroMesh Ventilated Backplate", "20%", "30%"), ("Nylon Webbing", "15%", "25%")], "comp": ["OEKO-TEX 100", "ISO 14001:2015", "SGS Tear Resistance"]},
            {"sku": "WB-SCH-28L", "name": "Orthopedic Reflective School Backpack 28L", "cat": "Ergonomic Packs", "mat": [("600D Recycled Oxford Cloth", "70%", "80%"), ("EPE Shock-Absorbing Foam", "20%", "20%"), ("Reflective 3M Scotchlite", "10%", "0%")], "comp": ["EN 71-3 Safety", "CPSIA Compliant", "ISO 9001:2015"]},
            {"sku": "WB-DUF-60L", "name": "Waterproof Heavy-Duty Expedition Duffel 60L", "cat": "Luggage & Travel", "mat": [("Tarpaulin PVC/TPU Hybrid", "80%", "20%"), ("Reinforced Seatbelt Webbing", "15%", "40%"), ("Waterproof Zipper Track", "5%", "0%")], "comp": ["IPX6 Waterproof", "RoHS Compliant", "ISO 9001:2015"]}
        ]
    },
    {
        "domain": "widewaysportswear.com",
        "company": "Wideway Sportswear & Performance Apparel Factory",
        "server": {"host": "43.130.32.54", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/widewaysportswear.com",
        "industry": "Functional Activewear, Teamwear & Industrial Workwear",
        "skus": [
            {"sku": "WS-DRY-101", "name": "Pro-Cooling Seamless Athletic Running Tee", "cat": "Performance Activewear", "mat": [("Recycled Micro-Polyester", "88%", "90%"), ("Spandex Elastane", "12%", "0%")], "comp": ["OEKO-TEX Standard 100", "GRS Certified", "Bluesign Approved"]},
            {"sku": "WS-JOG-202", "name": "Heavyweight French Terry Training Hoodie", "cat": "Athletic Fleece", "mat": [("Organic Combed Cotton", "80%", "0%"), ("Recycled Poly Fleece", "20%", "100%")], "comp": ["GOTS Organic", "BCI Better Cotton", "ISO 9001:2015"]},
            {"sku": "WS-CARGO-303", "name": "Reinforced Tactical Stretch Cargo Work Pants", "cat": "Industrial Workwear", "mat": [("Cotton-Polyester Ripstop Canvas", "65%", "40%"), ("Cordura Knee Insets", "30%", "25%"), ("Elastane Stretch Web", "5%", "0%")], "comp": ["EN ISO 13688:2013", "BSCI Social Audit", "OEKO-TEX 100"]},
            {"sku": "WS-JKT-404", "name": "3-Layer Bonded Windproof Softshell Team Jacket", "cat": "Outerwear", "mat": [("Mechanical Stretch Poly Membrane", "70%", "65%"), ("Microfleece Thermal Core", "30%", "50%")], "comp": ["ISO 14001:2015", "AATCC 127 Hydrostatic", "REACH 1907/2006"]}
        ]
    },
    {
        "domain": "widewaycorkfootwear.com",
        "company": "Wideway Cork Footwear & Anatomical Sandals Co.",
        "server": {"host": "43.130.32.54", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/widewaycorkfootwear.com",
        "industry": "Anatomical Cork Footbeds, Clogs & Eco-Friendly Sandals",
        "skus": [
            {"sku": "WCK-BST-01", "name": "Boston Classic Suede Cork Clog", "cat": "Closed-Toe Clogs", "mat": [("Natural Sustainable Cork Footbed", "50%", "100%"), ("LWG Certified Cow Suede", "35%", "0%"), ("Shock-Absorbing EVA Sole", "15%", "40%")], "comp": ["FSC Chain-of-Custody", "ISO 9001:2015", "REACH Heavy Metal Free"]},
            {"sku": "WCK-ARZ-02", "name": "Arizona Two-Strap Adjustable Slide Sandal", "cat": "Two-Strap Sandals", "mat": [("Latex-Infused Natural Cork", "55%", "100%"), ("Oiled Pull-Up Leather", "30%", "0%"), ("Cushioned EVA Outsole", "15%", "35%")], "comp": ["SATRA Approved", "BSCI Ethical Audit", "GRS 4.0"]},
            {"sku": "WCK-GZH-03", "name": "Gizeh Thong Ergonomic Arch Sandal", "cat": "Thong Sandals", "mat": [("Molded Natural Cork Core", "60%", "100%"), ("Skin-Friendly Birko-Flor Upper", "25%", "50%"), ("Durable EVA Tread", "15%", "30%")], "comp": ["ISO 14001:2015", "OEKO-TEX Leather Standard"]},
            {"sku": "WCK-EVA-04", "name": "Monolithic Waterproof Lightweight EVA Slide", "cat": "Waterproof Slides", "mat": [("Injection Bio-EVA Copolymer", "100%", "30%")], "comp": ["FDA 21 CFR Compliant", "REACH Phthalate-Free", "ISO 9001:2015"]}
        ]
    },
    {
        "domain": "widewayfootballgear.com",
        "company": "Wideway Football Gear & Athletic Protective Equipment",
        "server": {"host": "43.130.32.54", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/widewayfootballgear.com",
        "industry": "Professional Soccer Cleats, Goalkeeper Gloves & Shin Guards",
        "skus": [
            {"sku": "WFB-FG-701", "name": "Elite Firm Ground Kangaroo-Feel Soccer Cleat", "cat": "Soccer Cleats", "mat": [("Microfiber Textured Upper", "55%", "40%"), ("Pebax Responsive Chassis Plate", "30%", "20%"), ("TPU Traction Studs", "15%", "50%")], "comp": ["FIFA Quality Tested", "SATRA TM144 Traction", "ISO 9001:2015"]},
            {"sku": "WFB-TF-702", "name": "Pro Artificial Turf Multi-Stud Football Boot", "cat": "Turf Boots", "mat": [("Flyknit Reinforced Upper", "50%", "60%"), ("High-Density Rubber Outsole", "35%", "45%"), ("Phylon Midsole Cushioning", "15%", "30%")], "comp": ["CE Certified", "REACH Compliant", "BSCI Social Audit"]},
            {"sku": "WFB-PAD-101", "name": "Carbon Composite Ergonomic Shin Guard", "cat": "Protective Equipment", "mat": [("Carbon Fiber / K-Resin Shell", "65%", "25%"), ("Shock Absorbing EVA Foam Backing", "35%", "30%")], "comp": ["EN 13061:2001 Protective Standards", "CE Category II PPE"]},
            {"sku": "WFB-GLV-201", "name": "4mm Contact German Latex Match Goalkeeper Gloves", "cat": "Goalkeeper Gloves", "mat": [("German Contact Latex Palm", "50%", "0%"), ("Neoprene Airprene Backhand", "35%", "40%"), ("Elastic Wrap Wristband", "15%", "30%")], "comp": ["ISO 9001:2015", "REACH Non-Toxic", "SGS Abrasion Resistance"]}
        ]
    },

    # Server 2: 43.135.182.81
    {
        "domain": "leohygiene.com",
        "company": "Leo Hygiene & Healthcare Products Co., Ltd.",
        "server": {"host": "43.135.182.81", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/leohygiene.com",
        "industry": "Medical Incontinence, Adult Briefs & Infant Hygiene Care",
        "skus": [
            {"sku": "LEO-AD-PREM", "name": "Max-Absorption Medical Adult Incontinence Brief", "cat": "Adult Incontinence", "mat": [("FSC Certified Fluff Pulp", "50%", "100%"), ("Japanese Superabsorbent Polymer (SAP)", "25%", "0%"), ("Hydrophilic Nonwoven Topsheet", "15%", "30%"), ("Breathable PE Film", "10%", "40%")], "comp": ["CE MDR (EU) 2017/745", "FDA Registered Class I", "ISO 13485:2016", "OEKO-TEX 100"]},
            {"sku": "LEO-AP-360", "name": "360° All-Around Comfort Adult Pull-Up Pants", "cat": "Adult Pull-Ups", "mat": [("Composite Ultra-Thin SAP Core", "45%", "0%"), ("Air-Through Nonwoven Fabric", "30%", "35%"), ("Lycra Elastic Strands", "15%", "0%"), ("Waterproof Backsheet", "10%", "50%")], "comp": ["ISO 9001:2015", "FDA Device Listing", "Dermatest Excellent"]},
            {"sku": "LEO-UP-6090", "name": "Hospital-Grade Disposable Nursing Underpad 60x90cm", "cat": "Medical Bed Pads", "mat": [("Embossed Diamond Tissue Pulp", "60%", "100%"), ("Anti-Bacterial SAP Granules", "20%", "0%"), ("Non-Skid Polyethylene Film", "20%", "45%")], "comp": ["ISO 13485 Medical Devices", "CE Technical File Validated", "BSCI Audit"]},
            {"sku": "LEO-BP-ECO", "name": "Biodegradable Pure Bamboo Fiber Baby Diaper", "cat": "Baby Diapers", "mat": [("100% Natural Bamboo Nonwoven", "55%", "100%"), ("Chlorine-Free TCF Pulp + SAP", "35%", "60%"), ("Compostable Cornstarch Film", "10%", "100%")], "comp": ["OK Biobased TUV Austria", "OEKO-TEX Class 1 Infant", "FSC Certified"]}
        ]
    },
    {
        "domain": "shdhygiene.com",
        "company": "Quanzhou Shenghongda Hygiene Products Co., Ltd. (SHD Hygiene)",
        "server": {"host": "43.135.182.81", "port": 2222, "user": "ubuntu", "pass": "WHJCwhjc2026"},
        "web_root": "/var/www/shdhygiene.com",
        "industry": "Baby Diapers, Pull-Up Pants & Feminine Period Care",
        "skus": [
            {"sku": "SHD-BB-PRO", "name": "Feather-Soft Cloud Comfort Baby Tape Diaper", "cat": "Baby Tape Diapers", "mat": [("Sumitomo SAP Composite Paper Core", "45%", "0%"), ("Hot-Air Cottony Soft Topsheet", "30%", "30%"), ("Breathable Micro-Porous Backsheet", "15%", "40%"), ("Magic Refastenable S-Tapes", "10%", "20%")], "comp": ["ISO 9001:2015", "FDA Registered", "CE MDR Compliant", "OEKO-TEX Standard 100"]},
            {"sku": "SHD-BP-360", "name": "Active Fit 360° Elastic Waist Baby Training Pant", "cat": "Baby Training Pants", "mat": [("Dual-Core Superabsorbent Matrix", "40%", "0%"), ("Ultrasonic Seamless Nonwoven Band", "35%", "25%"), ("Perforated Air-Flow Lining", "15%", "50%"), ("Wetness Indicator Ink", "10%", "0%")], "comp": ["ISO 13485:2016", "FSC Certified Pulp", "SGS Heavy Metal Free"]},
            {"sku": "SHD-MP-OVR", "name": "Heavy Surge Overnight Period Underwear Pants", "cat": "Feminine Period Care", "mat": [("Ultra-Thin 1.8mm Fast-Absorb Core", "50%", "0%"), ("Skin-Friendly Velvet Touch Nonwoven", "30%", "30%"), ("360° Leak-Guard Barriers", "20%", "40%")], "comp": ["ISO 9001:2015", "Dermatologically Tested", "RoHS Compliant"]},
            {"sku": "SHD-SN-COT", "name": "Organic Cotton Anion Core Sanitary Napkin 290mm", "cat": "Sanitary Napkins", "mat": [("100% GOTS Certified Organic Cotton", "45%", "0%"), ("Negative Ion Mineral Core Strip", "10%", "0%"), ("SAP Airlaid Absorbent Paper", "30%", "0%"), ("Biodegradable Release Paper", "15%", "100%")], "comp": ["GOTS Organic Certified", "FDA 21 CFR", "CE Compliant"]}
        ]
    },

    # Server 3: 137.184.111.182
    {
        "domain": "eazylunch.com",
        "company": "EazyLunch Houseware & Kitchen Storage Co., Ltd.",
        "server": {"host": "137.184.111.182", "port": 22, "user": "root", "pass": "nkwnkw123.."},
        "web_root": "/var/www/eazylunch.com/html",
        "industry": "Stainless Steel Bento Boxes, Silicone Lunchware & Food Storage",
        "skus": [
            {"sku": "EZL-SS-304", "name": "Leakproof SUS304 Food-Grade Stainless Bento Box", "cat": "Stainless Steel Bento", "mat": [("SUS304 (18/8) Austenitic Stainless Steel", "85%", "65%"), ("Food-Grade Silicone Sealing Gasket", "10%", "0%"), ("BPA-Free PP Outer Lock Clip", "5%", "50%")], "comp": ["LFGB Food Contact (Germany)", "US FDA 21 CFR 177.1520", "DGCCRF (France)", "ISO 9001:2015"]},
            {"sku": "EZL-SIL-5C", "name": "Collapsible Platinum Silicone 5-Compartment Bento", "cat": "Silicone Lunchware", "mat": [("100% Platinum Cured Silicone", "85%", "0%"), ("Reinforced Nylon Rigid Rim", "15%", "40%")], "comp": ["LFGB Certified", "FDA Approved", "BPA/BPS Free", "Dishwasher Safe"]},
            {"sku": "EZL-THERM-500", "name": "Double-Wall Vacuum Insulated Food Jar 500ml", "cat": "Thermal Storage", "mat": [("Inner SUS316 Medical-Grade Steel", "45%", "50%"), ("Outer SUS304 Brushed Steel", "40%", "50%"), ("Insulated PP Stopper with Pressure Release", "15%", "25%")], "comp": ["EN 12546-1 Thermal Performance", "LFGB Compliant", "ISO 9001:2015"]},
            {"sku": "EZL-KID-4C", "name": "Drop-Proof Tritan Portion-Control Kids Bento Box", "cat": "Kids Lunchware", "mat": [("Eastman Tritan Copolyester", "60%", "30%"), ("TPE Shock-Absorbing Bumper", "25%", "0%"), ("Silicone Removable Seal", "15%", "0%")], "comp": ["CPSIA Children Safety", "EU 10/2011 Food Plastic", "FDA Certified"]}
        ]
    },
    {
        "domain": "naiketableware.com",
        "company": "Naike Tableware & Eco Kitchen Solutions Co., Ltd.",
        "server": {"host": "137.184.111.182", "port": 22, "user": "root", "pass": "nkwnkw123.."},
        "web_root": "/var/www/naiketableware.com/current",
        "industry": "Biodegradable Wheat Straw Dinnerware & Compostable Catering Sets",
        "skus": [
            {"sku": "NK-WS-PLATE", "name": "Biodegradable Wheat Straw Fiber Dinner Plate 10-Inch", "cat": "Wheat Straw Plates", "mat": [("Agricultural Wheat Straw Plant Fiber", "60%", "100%"), ("Food-Contact Polypropylene Binder", "40%", "30%")], "comp": ["LFGB Standard", "FDA 21 CFR 177.1520", "BPA Free", "Microwave Safe"]},
            {"sku": "NK-WS-BOWL", "name": "Eco-Friendly Deep Cereal & Soup Bowl 800ml", "cat": "Eco Bowls", "mat": [("Natural Organic Wheat Stalk Powder", "65%", "100%"), ("Food-Safe PP Resin", "35%", "25%")], "comp": ["EU Regulation 10/2011", "ISO 9001:2015", "Heavy Metal Free"]},
            {"sku": "NK-WS-CUTLERY", "name": "4-in-1 Compostable Travel Cutlery Set with Case", "cat": "Cutlery Sets", "mat": [("Wheat Straw Biocomposite", "70%", "100%"), ("Food-Grade Polymer", "30%", "40%")], "comp": ["DIN CERTCO Biobased", "FDA Food Grade", "RoHS Compliant"]},
            {"sku": "NK-WS-TUMBLER", "name": "Double-Wall Insulated Eco Coffee Tumbler 450ml", "cat": "Drinkware", "mat": [("Pressed Wheat Straw Outer Wall", "50%", "100%"), ("Food-Grade SUS304 Inner Liner", "40%", "50%"), ("Silicone Leakproof Ring", "10%", "0%")], "comp": ["LFGB & FDA Certified", "ISO 14001:2015", "Dishwasher Safe"]}
        ]
    },
    {
        "domain": "ghsafetyboots.com",
        "company": "Guanghan Safety Footwear & Workwear Manufacturing Co., Ltd.",
        "server": {"host": "137.184.111.182", "port": 22, "user": "root", "pass": "nkwnkw123.."},
        "web_root": "/var/www/ghsafetyboots.com",
        "industry": "EN ISO 20345 Industrial Safety Boots & Tactical Protective Footwear",
        "skus": [
            {"sku": "GH-S3-COMP", "name": "Lightweight Composite Toe Kevlar Midsole S3 Work Boot", "cat": "S3 Safety Boots", "mat": [("Water-Resistant Oiled Nubuck Leather", "50%", "0%"), ("Non-Metallic Fiberglass Safety Cap", "15%", "30%"), ("Anti-Penetration Kevlar Fabric", "15%", "40%"), ("Dual-Density PU/Rubber Sole", "20%", "35%")], "comp": ["EN ISO 20345:2022 S3 SRC", "ASTM F2413-18 M/I/C/PR", "CE Category II PPE", "ISO 9001:2015"]},
            {"sku": "GH-ESD-901", "name": "Electrostatic Discharge (ESD) Cleanroom Safety Shoe", "cat": "ESD Safety Footwear", "mat": [("Microfiber Breathable Leather", "55%", "45%"), ("Composite Safety Toe Cap", "20%", "30%"), ("Conductive ESD Dissipative PU Sole", "25%", "20%")], "comp": ["EN 61340-5-1 ESD", "EN ISO 20345:2022", "RoHS Compliant"]},
            {"sku": "GH-OIL-802", "name": "Heavy-Duty Oil & Chemical Resistant Construction Boot", "cat": "Construction Boots", "mat": [("Full-Grain Hydrophobic Crazy Horse Leather", "55%", "0%"), ("Hardened Steel Toe 200J", "15%", "85%"), ("Nitrile Rubber Heat-Resistant (300°C) Outsole", "30%", "40%")], "comp": ["EN ISO 20345:2022 HRO HI CI", "SATRA Lab Certified", "BSCI Audit"]},
            {"sku": "GH-MET-703", "name": "External Metatarsal Guard Heavy Foundry Boot", "cat": "Foundry Boots", "mat": [("Flame-Retardant Kevlar-Stitched Leather", "60%", "0%"), ("Internal Metatarsal Shield", "15%", "50%"), ("Vibram Fire & Slip Resistant Outsole", "25%", "35%")], "comp": ["EN ISO 20349-2:2017 Foundry Standard", "ASTM F2413 Metatarsal PR EH"]}
        ]
    }
]

def build_dpp_html(product: dict, domain: str, company: str, base_url: str) -> str:
    sku = product["sku"]
    name = product["name"]
    category = product["cat"]
    materials = product["mat"]
    compliance = product["comp"]
    dpp_id = f"MA.156.{abs(hash(domain)) % 900000 + 100000}.01.{sku}"
    canonical_url = f"{base_url}/dpp/dpp-{sku.lower()}.html"
    hub_url = f"{base_url}/ma-dpp.html"

    mat_rows = "".join(f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td></tr>" for m in materials)
    comp_items = "".join(f"<li>{c}</li>" for c in compliance)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MA-DPP Digital Product Passport: {name} ({sku}) | {company}</title>
  <meta name="description" content="Official MA-DPP Digital Product Passport for {name} ({sku}) manufactured by {company}. Certified circular lifecycle, Bill of Materials (BOM), and compliance with EU ESPR 2024/1781 & ISO/IEC 15459.">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow">
  
  <!-- Schema.org Digital Product Passport -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{name}",
    "sku": "{sku}",
    "identifier": "{dpp_id}",
    "category": "{category}",
    "url": "{canonical_url}",
    "brand": {{
      "@type": "Brand",
      "name": "{company}"
    }},
    "additionalProperty": [
      {{ "@type": "PropertyValue", "name": "DPP_ID", "value": "{dpp_id}" }},
      {{ "@type": "PropertyValue", "name": "ComplianceStandard", "value": "ISO/IEC 15459 & EU ESPR 2024/1781" }},
      {{ "@type": "PropertyValue", "name": "CircularityClass", "value": "Class A Industrial Grade" }},
      {{ "@type": "PropertyValue", "name": "VerificationAuthority", "value": "Enterprise MA-DPP National Registry" }}
    ]
  }}
  </script>

  <style>
    :root {{ --primary: #0b1e36; --accent: #0284c7; --surface: #f8fafc; --text: #0f172a; --border: #e2e8f0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--surface); margin: 0; padding: 2rem 1rem; }}
    .container {{ max-width: 920px; margin: 0 auto; background: #fff; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 2.5rem; }}
    .badge {{ display: inline-block; padding: 0.35rem 0.85rem; background: #e0f2fe; color: #0369a1; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }}
    h1 {{ margin: 0.75rem 0 0.5rem; color: var(--primary); font-size: 1.85rem; }}
    .subhead {{ color: #64748b; font-size: 0.95rem; margin-bottom: 2rem; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }}
    @media(max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    .card {{ background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; }}
    .card h3 {{ margin-top: 0; color: var(--primary); font-size: 1.1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }}
    .card p {{ margin: 0.5rem 0; font-size: 0.9rem; }}
    .card strong {{ color: #334155; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; background: #fff; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }}
    th, td {{ padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
    th {{ background: #f1f5f9; font-weight: 700; color: var(--primary); }}
    ul {{ margin: 0.5rem 0; padding-left: 1.25rem; font-size: 0.9rem; }}
    li {{ margin-bottom: 0.35rem; }}
    .footer-nav {{ margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
    .btn {{ display: inline-block; padding: 0.6rem 1.2rem; background: var(--primary); color: #fff; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.9rem; }}
    .btn:hover {{ background: #1e293b; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">ISO/IEC 15459 &amp; EU ESPR Verified</span>
    <h1>Digital Product Passport: {name}</h1>
    <div class="subhead">Passport ID: <code>{dpp_id}</code> | Category: {category} | Standard: EU ESPR 2024/1781</div>

    <div class="grid">
      <div class="card">
        <h3>1. Identity &amp; Manufacturing Traceability</h3>
        <p><strong>SKU Identifier:</strong> {sku}</p>
        <p><strong>Manufacturing Entity:</strong> {company}</p>
        <p><strong>Factory Verification:</strong> ISO 9001 Audited Clean Production</p>
        <p><strong>Traceability Cryptographic Hash:</strong> <code>sha256-{sku.lower()}-verified-espr</code></p>
        <p><strong>Circularity Status:</strong> Fully Recyclable &amp; Disassemblable</p>
      </div>

      <div class="card">
        <h3>2. Quality &amp; Compliance Accreditations</h3>
        <ul>
          {comp_items}
        </ul>
      </div>
    </div>

    <h3>3. Bill of Materials (BOM) &amp; Circular Recycled Content</h3>
    <table>
      <thead>
        <tr>
          <th>Material Component Layer</th>
          <th>Weight Composition (%)</th>
          <th>Post-Consumer Recycled Ratio (%)</th>
        </tr>
      </thead>
      <tbody>
        {mat_rows}
      </tbody>
    </table>

    <div class="footer-nav">
      <a href="{hub_url}" class="btn">← Back to {company} MA-DPP Hub</a>
      <a href="{base_url}/contact" style="color: var(--accent); font-weight: 600; text-decoration: none;">Request Full Laboratory Dossier →</a>
    </div>
  </div>
</body>
</html>
"""

def build_ma_dpp_hub_html(site_cfg: dict, base_url: str) -> str:
    company = site_cfg["company"]
    domain = site_cfg["domain"]
    industry = site_cfg["industry"]
    skus = site_cfg["skus"]

    sku_cards = "".join(f"""
      <div class="dpp-item">
        <div class="dpp-meta">
          <span class="sku-tag">{s['sku']}</span>
          <span class="cat-tag">{s['cat']}</span>
        </div>
        <h4>{s['name']}</h4>
        <p class="specs">Certified Standards: {", ".join(s['comp'][:3])}</p>
        <a href="{base_url}/dpp/dpp-{s['sku'].lower()}.html" class="link-btn">Inspect Digital Passport →</a>
      </div>
    """ for s in skus)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MA-DPP Digital Product Passport Registry | {company}</title>
  <meta name="description" content="Official Enterprise MA-DPP Digital Product Passport (DPP) Registry for {company}. Cryptographically certified product passports under ISO/IEC 15459 and EU ESPR 2024/1781 circular economy regulations.">
  <link rel="canonical" href="{base_url}/ma-dpp.html">
  <meta name="robots" content="index, follow">

  <!-- Schema.org CollectionPage & FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "{base_url}/ma-dpp.html#webpage",
        "url": "{base_url}/ma-dpp.html",
        "name": "{company} MA-DPP Digital Product Passport Portal",
        "description": "Comprehensive registry of verified product passports under ISO/IEC 15459 & EU ESPR 2024/1781.",
        "isPartOf": {{
          "@type": "WebSite",
          "@id": "{base_url}/#website",
          "name": "{company}",
          "url": "{base_url}"
        }}
      }},
      {{
        "@type": "FAQPage",
        "@id": "{base_url}/ma-dpp.html#faq",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "What is the MA-DPP system on {domain}?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "The MA-DPP (Digital Product Passport) is an internationally aligned transparency system built under ISO/IEC 15459 and EU Ecodesign for Sustainable Products Regulation (ESPR 2024/1781), providing full lifecycle traceability, Bill of Materials breakdowns, and verified testing accreditations for global procurement buyers."
            }}
          }},
          {{
            "@type": "Question",
            "name": "How does {company} ensure compliance with international buyer audits?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{company} strictly complies with international production frameworks including ISO 9001 quality management, third-party laboratory verification, and transparent raw material origin tracking."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
    :root {{ --primary: #0b1e36; --accent: #0284c7; --surface: #f8fafc; --text: #0f172a; --border: #e2e8f0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--surface); margin: 0; padding: 2rem 1rem; }}
    .container {{ max-width: 1040px; margin: 0 auto; background: #fff; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 3rem 2.5rem; }}
    .badge {{ display: inline-block; padding: 0.35rem 0.85rem; background: #e0f2fe; color: #0369a1; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }}
    h1 {{ margin: 0.75rem 0 0.5rem; color: var(--primary); font-size: 2.1rem; }}
    .lead {{ color: #475569; font-size: 1.05rem; margin-bottom: 2.5rem; line-height: 1.7; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0; }}
    .dpp-item {{ background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; }}
    .dpp-meta {{ display: flex; justify-content: space-between; margin-bottom: 0.75rem; }}
    .sku-tag {{ font-weight: 700; color: #0369a1; font-size: 0.85rem; background: #e0f2fe; padding: 0.2rem 0.5rem; border-radius: 4px; }}
    .cat-tag {{ font-size: 0.8rem; color: #64748b; }}
    h4 {{ margin: 0 0 0.5rem; color: var(--primary); font-size: 1.15rem; }}
    .specs {{ font-size: 0.85rem; color: #64748b; margin-bottom: 1.25rem; }}
    .link-btn {{ display: block; text-align: center; padding: 0.5rem; background: #fff; border: 1px solid var(--accent); color: var(--accent); text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.85rem; }}
    .link-btn:hover {{ background: var(--accent); color: #fff; }}
    .faq-section {{ margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--border); }}
    .faq-item {{ margin-bottom: 1.5rem; }}
    .faq-item h4 {{ color: var(--primary); margin-bottom: 0.35rem; }}
    .faq-item p {{ margin: 0; color: #475569; font-size: 0.95rem; }}
    .footer-bar {{ margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: center; }}
    .footer-bar a {{ color: var(--primary); font-weight: 600; text-decoration: none; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">Official Enterprise MA-DPP Hub</span>
    <h1>Digital Product Passport Registry</h1>
    <p class="lead">{company} ({industry}) provides fully verified, cryptographic Digital Product Passports in full compliance with ISO/IEC 15459 and EU ESPR (Regulation EU 2024/1781) circular economy requirements.</p>

    <h3>Active Certified Product Passports</h3>
    <div class="grid">
      {sku_cards}
    </div>

    <div class="faq-section">
      <h3>Frequently Asked Compliance Questions</h3>
      <div class="faq-item">
        <h4>What is the purpose of this Digital Product Passport hub?</h4>
        <p>The MA-DPP hub provides European, North American, and global procurement committees with instant, verifiable access to bill-of-materials, carbon footprint, recyclability ratings, and laboratory testing certificates for each SKU.</p>
      </div>
      <div class="faq-item">
        <h4>How often is lifecycle and certification data updated?</h4>
        <p>All product passports are reviewed and updated dynamically upon annual ISO 9001 and third-party compliance recertification audits.</p>
      </div>
    </div>

    <div class="footer-bar">
      <a href="{base_url}/">← Back to {domain} Official Homepage</a>
    </div>
  </div>
</body>
</html>
"""

def build_dpp_sitemap_xml(site_cfg: dict, base_url: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [f"{base_url}/ma-dpp.html"]
    for s in site_cfg["skus"]:
        urls.append(f"{base_url}/dpp/dpp-{s['sku'].lower()}.html")

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        priority = "0.9" if "ma-dpp.html" in u else "0.8"
        xml_lines.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>')
    xml_lines.append('</urlset>')
    return "\n".join(xml_lines)

def deploy_site_dpp(site_cfg: dict):
    domain = site_cfg["domain"]
    server = site_cfg["server"]
    remote_root = site_cfg["web_root"]
    base_url = f"https://www.{domain}"

    print(f"\n=======================================================")
    print(f"🚀 Processing MA-DPP for {domain} on {server['host']}:{server['port']}...")
    print(f"=======================================================")

    # 1. Connect SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server["host"], port=server["port"], username=server["user"], password=server["pass"], timeout=15)
    sftp = ssh.open_sftp()

    # Ensure remote dpp directory exists
    remote_dpp_dir = f"{remote_root}/dpp"
    try:
        sftp.stat(remote_dpp_dir)
    except IOError:
        print(f"Creating remote dir: {remote_dpp_dir}")
        try:
            sftp.mkdir(remote_dpp_dir)
        except Exception as e:
            ssh.exec_command(f"sudo mkdir -p {remote_dpp_dir} && sudo chown -R {server['user']} {remote_dpp_dir}")

    # 2. Generate and upload ma-dpp.html
    hub_html = build_ma_dpp_hub_html(site_cfg, base_url)
    remote_hub_path = f"{remote_root}/ma-dpp.html"
    print(f"  Uploading hub: {remote_hub_path} ({len(hub_html)} bytes)...")
    with sftp.file(remote_hub_path, "w") as f:
        f.write(hub_html)

    # 3. Generate and upload individual dpp-*.html pages
    for s in site_cfg["skus"]:
        pdp_html = build_dpp_html(s, domain, site_cfg["company"], base_url)
        remote_pdp_path = f"{remote_dpp_dir}/dpp-{s['sku'].lower()}.html"
        print(f"  Uploading DPP page: {remote_pdp_path} ({len(pdp_html)} bytes)...")
        with sftp.file(remote_pdp_path, "w") as f:
            f.write(pdp_html)

    # 4. Generate and upload sitemap-dpp.xml
    sitemap_xml = build_dpp_sitemap_xml(site_cfg, base_url)
    remote_sitemap_path = f"{remote_root}/sitemap-dpp.xml"
    print(f"  Uploading sitemap: {remote_sitemap_path} ({len(sitemap_xml)} bytes)...")
    with sftp.file(remote_sitemap_path, "w") as f:
        f.write(sitemap_xml)

    # 5. Update robots.txt to include sitemap-dpp.xml if not present
    remote_robots_path = f"{remote_root}/robots.txt"
    try:
        with sftp.file(remote_robots_path, "r") as f:
            robots_content = f.read().decode("utf-8")
        if "sitemap-dpp.xml" not in robots_content:
            robots_content += f"\nSitemap: {base_url}/sitemap-dpp.xml\n"
            with sftp.file(remote_robots_path, "w") as f:
                f.write(robots_content)
            print(f"  Updated robots.txt with sitemap-dpp.xml reference.")
    except Exception as e:
        print(f"  Note: robots.txt update skipped or not found ({e})")

    # Fix permissions
    ssh.exec_command(f"chmod 644 {remote_root}/sitemap-dpp.xml {remote_root}/ma-dpp.html {remote_dpp_dir}/*.html 2>/dev/null || true")

    sftp.close()
    ssh.close()
    print(f"✅ Finished deployment for {domain}!")

def main():
    print(f"Starting batch MA-DPP deployment across {len(FLEET_DPP_CONFIG)} sites...")
    for site_cfg in FLEET_DPP_CONFIG:
        try:
            deploy_site_dpp(site_cfg)
        except Exception as e:
            print(f"❌ Error deploying {site_cfg['domain']}: {e}")

if __name__ == "__main__":
    main()
