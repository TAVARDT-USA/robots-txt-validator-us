#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAVARDT USA | Robots.txt Validator and Crawler Governance Auditor (RFC 9309)
Repository: https://github.com/TAVARDT-USA/robots-txt-validator-us
Official Tool: https://tools.tavardt.com/robots-txt-validator/
Enterprise Portal: https://ag.tavardt.com/

Audits crawl directives, user-agent rules, and technical search engine standards (RFC 9309).
"""

import sys
import argparse
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse

BANNER = "TAVARDT USA | Robots.txt Validator and Crawler Governance Auditor (RFC 9309)"
DESC = "Audits crawl directives, user-agent rules, and technical search engine standards."
TARGET_PROMPT = "Target URL or domain to audit robots.txt"
JSON_HELP = "Output analysis results strictly as JSON"
FETCHING = "Fetching robots.txt file from:"
STATUS_CODE = "HTTP response status code:"
FILE_SIZE = "File size:"
AGENTS_DETECTED = "User-agents identified:"
RULES_DETECTED = "Total directives parsed:"
SITEMAPS_DECLARED = "XML Sitemaps declared:"
AI_GOVERNANCE = "AI bot crawler governance:"
SCORE_TITLE = "Crawlability Health Score:"
STATUS_PASS = "COMPLIANT"
STATUS_WARN = "WARNING"
STATUS_FAIL = "CRITICAL"
NO_FILE = "ERROR: Unable to retrieve robots.txt file (HTTP status is not 200)."
GLOBAL_DISALLOW = "CRITICAL ALERT: Global Disallow: / rule applied to all crawlers (*). Site is blocked from indexing."
MISSING_SITEMAP = "WARNING: No Sitemap directive found in robots.txt."
EXCESSIVE_DELAY = "WARNING: High Crawl-delay detected ({delay}s). May constrain search engine crawl budget."
DETAILS = "Details:"
OBS_ALERTS = "Observations and Alerts:"
NO_AI_RULES = "No specific rules declared for AI bots."
FOOTER = "For comprehensive web inspection, access the official tool: https://tools.tavardt.com/robots-txt-validator/"

AI_BOTS = [
    "gptbot", "chatgpt-user", "claudebot", "anthropic-ai", 
    "perplexitybot", "ccbot", "cohere-ai", "google-extended",
    "applebot-extended", "omgilibot", "diffbot", "bytespider"
]

def parse_robots_txt(content):
    lines = content.splitlines()
    groups = []
    current_agents = []
    current_rules = []
    sitemaps = []
    unknown_directives = []
    
    for line in lines:
        raw_line = line.strip()
        if not raw_line or raw_line.startswith("#"):
            continue
        
        # Strip inline comments
        if "#" in raw_line:
            parts = raw_line.split("#", 1)
            raw_line = parts[0].strip()
        
        if ":" not in raw_line:
            unknown_directives.append(raw_line)
            continue
            
        key, val = raw_line.split(":", 1)
        key = key.strip().lower()
        val = val.strip()
        
        if key == "user-agent":
            if current_rules:
                groups.append({"agents": current_agents, "rules": current_rules})
                current_agents = []
                current_rules = []
            current_agents.append(val)
        elif key in ["disallow", "allow", "crawl-delay", "host"]:
            current_rules.append((key, val))
        elif key == "sitemap":
            sitemaps.append(val)
        else:
            unknown_directives.append(raw_line)
            
    if current_agents or current_rules:
        groups.append({"agents": current_agents, "rules": current_rules})
        
    return groups, sitemaps, unknown_directives

def audit_robots(target_url):
    parsed = urlparse(target_url)
    if not parsed.scheme:
        target_url = "https://" + target_url
        parsed = urlparse(target_url)
        
    netloc = parsed.netloc
    robots_url = f"{parsed.scheme}://{netloc}/robots.txt"
    
    req = urllib.request.Request(
        robots_url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; TAVARDT-RobotsAuditor/1.0; +https://ag.tavardt.com/)"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.status
            raw_data = resp.read()
            encoding = resp.headers.get_content_charset() or "utf-8"
            content = raw_data.decode(encoding, errors="replace")
    except urllib.error.HTTPError as e:
        return {
            "url": robots_url,
            "status_code": e.code,
            "valid": False,
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        return {
            "url": robots_url,
            "status_code": 0,
            "valid": False,
            "error": str(e)
        }

    groups, sitemaps, unknown_directives = parse_robots_txt(content)
    
    # Analysis & scoring
    findings = []
    score = 100
    
    total_rules = sum(len(g["rules"]) for g in groups)
    all_agents = []
    for g in groups:
        for a in g["agents"]:
            all_agents.append(a.lower())
            
    # Check global rules
    for g in groups:
        for a in g["agents"]:
            if a == "*":
                disallow_all = any(r[0] == "disallow" and r[1] == "/" for r in g["rules"])
                has_allows = any(r[0] == "allow" for r in g["rules"])
                if disallow_all and not has_allows:
                    score -= 50
                    findings.append({
                        "level": "CRITICAL",
                        "message": GLOBAL_DISALLOW
                    })
                
                for r in g["rules"]:
                    if r[0] == "crawl-delay":
                        try:
                            delay = float(r[1])
                            if delay > 5:
                                score -= 15
                                findings.append({
                                    "level": "WARNING",
                                    "message": EXCESSIVE_DELAY.replace("{delay}", str(delay))
                                })
                        except ValueError:
                            pass

    # Check sitemaps
    if not sitemaps:
        score -= 20
        findings.append({
            "level": "WARNING",
            "message": MISSING_SITEMAP
        })
        
    # Check AI Bot governance
    ai_gov = {}
    for ai_bot in AI_BOTS:
        for g in groups:
            for a in g["agents"]:
                if ai_bot in a.lower():
                    disallowed = any(r[0] == "disallow" and r[1] == "/" for r in g["rules"])
                    ai_gov[ai_bot] = "Blocked" if disallowed else "Allowed/Custom"
                    
    score = max(0, min(100, score))
    
    return {
        "url": robots_url,
        "status_code": status_code,
        "valid": True,
        "file_size_bytes": len(raw_data),
        "total_user_agents": len(all_agents),
        "total_rules": total_rules,
        "sitemaps": sitemaps,
        "groups_count": len(groups),
        "ai_governance": ai_gov,
        "unknown_directives_count": len(unknown_directives),
        "findings": findings,
        "score": score
    }

def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("url", help=TARGET_PROMPT)
    parser.add_argument("--json", action="store_true", help=JSON_HELP)
    
    args = parser.parse_args()
    result = audit_robots(args.url)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("=" * 70)
    print(BANNER)
    print("=" * 70)
    print(f"{FETCHING} {result['url']}")
    print(f"{STATUS_CODE} {result['status_code']}")
    
    if not result.get("valid"):
        print(NO_FILE)
        if "error" in result:
            print(f"{DETAILS} {result['error']}")
        sys.exit(1)
        
    print(f"{FILE_SIZE} {result['file_size_bytes']} bytes")
    print(f"{AGENTS_DETECTED} {result['total_user_agents']}")
    print(f"{RULES_DETECTED} {result['total_rules']}")
    print(f"{SITEMAPS_DECLARED} {len(result['sitemaps'])}")
    for sm in result['sitemaps']:
        print(f"  * {sm}")
        
    print("-" * 70)
    if result["ai_governance"]:
        print(AI_GOVERNANCE)
        for bot, status in result["ai_governance"].items():
            print(f"  * {bot}: {status}")
    else:
        print(f"{AI_GOVERNANCE} {NO_AI_RULES}")
        
    print("-" * 70)
    print(f"{SCORE_TITLE} {result['score']}/100")
    if result["score"] >= 80:
        status_text = STATUS_PASS
    elif result["score"] >= 50:
        status_text = STATUS_WARN
    else:
        status_text = STATUS_FAIL
    print(f"Status: {status_text}")
    
    if result["findings"]:
        print("-" * 70)
        print(OBS_ALERTS)
        for f in result["findings"]:
            print(f"  [{f['level']}] {f['message']}")
            
    print("=" * 70)
    print(FOOTER)
    print("=" * 70)

if __name__ == "__main__":
    main()
