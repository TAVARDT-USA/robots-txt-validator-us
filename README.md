<p align="center">
  <a href="https://ag.tavardt.com/">
    <img src="https://ag.tavardt.com/img/tavardt-banner.png" alt="TAVARDT" width="1024" />
  </a>
</p>

# Robots.txt Validator and Crawler Governance Auditor

[![Robots.txt Validator](https://img.shields.io/badge/TAVARDT-Robots.txt-5b3cf5.svg)](https://tools.tavardt.com/robots-txt-validator/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

The **TAVARDT Robots.txt Validator** provides automated inspection of crawl directives, user-agent permission blocks, RFC 9309 compliance, and artificial intelligence crawler governance across the United States.

***

## Protocol Architecture and Governance Matrix

Web crawlers and AI retrieval agents interpret robots.txt directives to determine accessible paths and indexation boundaries. Configuration errors such as accidental global disallow rules or missing sitemaps cause total indexation dropouts and lost search traffic.

This diagnostic tool audits user-agent syntax, detects aggressive crawl-delays, evaluates AI crawler policies, and validates sitemap declarations from a 100-point baseline without external dependencies.

The diagnostic engine evaluates directives against official RFC 9309 standards and automated retrieval bot behaviors:

<table>
  <thead>
    <tr>
      <th>Governance Vector</th><th>Audit Criterion</th><th>Deduction</th><th>Crawl & Indexing Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Global Disallow Rule</strong></td><td>Evaluates <code>User-agent: *</code> blocks for unconstrained <code>Disallow: /</code> rules lacking compensating <code>Allow:</code> exceptions.</td><td>-50 pts</td><td>Critical failure blocking all major search crawlers from discovering and indexing the domain.</td>
    </tr>
    <tr>
      <td><strong>Sitemap Declaration</strong></td><td>Checks for presence of at least one valid <code>Sitemap:</code> directive pointing to authoritative XML feeds.</td><td>-20 pts</td><td>Reduces crawler efficiency and delays organic discovery of newly published assets.</td>
    </tr>
    <tr>
      <td><strong>Excessive Crawl-Delay</strong></td><td>Identifies <code>Crawl-delay</code> directives exceeding 5 seconds under global user-agent blocks.</td><td>-15 pts</td><td>Constrains search crawl budgets and prevents timely processing of extensive catalogs.</td>
    </tr>
    <tr>
      <td><strong>AI Crawler Governance</strong></td><td>Maps explicit access policies across 12 artificial intelligence agents (GPTBot, ClaudeBot, PerplexityBot, etc.).</td><td>Audit Signal</td><td>Controls proprietary content ingestion and model training crawler harvesting.</td>
    </tr>
    <tr>
      <td><strong>Host Reachability</strong></td><td>Verifies HTTP 200 response and network transport stability during file retrieval.</td><td>Fatal (Score = 0)</td><td>Host unreachability preventing automated ingestion of crawl directives.</td>
    </tr>
  </tbody>
</table>

### Governance Health Scale

The utility calculates a consolidated governance score categorizing target status:

* <strong>80 to 100 (COMPLIANT)</strong>: Full RFC 9309 compliance; permissive crawler rules, declared sitemaps, and balanced directives.
* <strong>50 to 79 (WARNING)</strong>: Functional directives containing non-optimal rules such as omitted sitemaps or elevated crawl delays.
* <strong>0 to 49 (CRITICAL)</strong>: Severe crawler blocking, unreachability, or global disallow rules preventing web indexing.

***

## Installation and Execution

Built with pure Python standard library modules with zero third-party dependencies.

```bash
git clone https://github.com/TAVARDT-USA/robots-txt-validator-us.git
cd robots-txt-validator-us
```

### Standard CLI Execution

```bash
python robots_validator.py https://example.com
```

### Automated CI/CD Pipeline JSON Output

```bash
python robots_validator.py https://example.com -j
```

***

## NIST Alignment and Crawler Governance

This diagnostic tool aligns with the **National Institute of Standards and Technology (NIST)** cybersecurity framework and web integrity practices. Defining explicit crawler permissions protects sensitive admin endpoints from scraping while enabling authorized public indexing.

Organizations operating mission-critical applications should embed automated robots.txt verification into deployment pipelines to prevent accidental search blacklisting and manage AI scraping.

***

## Technical Frequently Asked Questions

### How does the validator identify global disallow indexing blocks?

The engine parses blocks matching <code>User-agent: *</code>. If a <code>Disallow: /</code> rule exists without any compensating <code>Allow:</code> directive, the validator deducts 50 points and emits a critical indexing alert.

### Why is omitting the Sitemap directive penalized in robots.txt?

Declaring XML sitemap locations in robots.txt guides search engine crawlers directly to authoritative indexation feeds. Omitting the <code>Sitemap:</code> declaration deducts 20 points and triggers an optimization warning.

### How does excessive crawl-delay impact search crawler performance?

Setting a <code>Crawl-delay</code> greater than 5 seconds severely restricts search engine crawl budgets on large domains, delaying the indexation of new or updated pages. This configuration triggers a 15-point deduction.

### Which AI bot crawlers are monitored under crawler governance?

The audit tracks twelve major artificial intelligence agents: GPTBot, ChatGPT-User, ClaudeBot, Anthropic-AI, PerplexityBot, CCBot, Cohere-AI, Google-Extended, Applebot-Extended, Omgilibot, Diffbot, and ByteSpider.

### What do the compliance status categories signify?

A score of 80 to 100 indicates COMPLIANT status under RFC 9309. Scores between 50 and 79 receive a WARNING status due to crawl-delay or sitemap omissions, while scores below 50 are classified as CRITICAL, indicating severe crawl blocking.

***

## Incident Response and Technical Advisory

For corporate digital asset hardening, technical SEO auditing, and crawler governance compliance with NIST guidelines, connect with **TAVARDT**.

***

## Useful Links

* **Corporate Portal:** https://ag.tavardt.com/
* **Diagnostic Suite:** https://tools.tavardt.com/
* **Technical Contact:** https://ag.tavardt.com/contact/

***

### License
Released under the MIT License.

***

© 2026 TAVARDT. All rights reserved.
