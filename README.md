<div align="center">

# Markolis MCP Server

### Institutional Quantitative Market Intelligence & Micro-Apps for AI Agents

[![npm](https://img.shields.io/npm/v/markolis-mcp?style=flat-square&color=cb3837&logo=npm)](https://www.npmjs.com/package/markolis-mcp)
[![PyPI](https://img.shields.io/pypi/v/markolis-mcp?style=flat-square&color=3775a9&logo=pypi)](https://pypi.org/project/markolis-mcp/)
[![Official MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.markolis--quant%2Fmarkolis--mcp-blue?style=flat-square&logo=anthropic)](https://registry.modelcontextprotocol.io)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-green.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Node 18+](https://img.shields.io/badge/node-18+-brightgreen.svg?style=flat-square&logo=node.js)](https://nodejs.org/)
[![Status](https://img.shields.io/badge/Service-Operational-emerald?style=flat-square)](https://www.markolis.com)

**[Terminal & Web App](https://www.markolis.com)** · **[Catalog & Tiers](https://www.markolis.com/catalog)** · **[MCP Setup & Keys](https://www.markolis.com/mcp)** · **[npm](https://www.npmjs.com/package/markolis-mcp)** · **[PyPI](https://pypi.org/project/markolis-mcp/)**

</div>

---

## Overview

**Markolis** brings institutional quantitative telemetry, 100-bin Auction Market Theory (AMT), order book trapped crowd sentiment, empirical H1 Yang-Zhang & jump volatility, and distribution-free conformal volatility cones to autonomous AI agents and trading desks.

Instead of relying on lagging retail indicators (RSI, MACD, Moving Averages), Markolis queries empirical order book volume distributions across **131 global financial assets** (Gold, Bitcoin, S&P 500, Nasdaq, EUR/USD, Crude Oil, and FX crosses).

### Key Capabilities
- **100-Bin Auction Market Theory (AMT)**: Point of Control (POC), 70% Value Area bounds (VAH / VAL), Low-Volume Nodes (LVNs), and balance/imbalance regimes.
- **Order Book Trapped Crowd Radar**: Net long/short retail cluster offside percentages and nearest stop-sweep vectors.
- **Conformal & Empirical H1 Volatility**: Distribution-free 90% confidence intervals alongside Parkinson, Garman-Klass, Yang-Zhang open-jump volatility, and bipower jump variation ratios.
- **Global Macro & Shock Radar**: Active trading session overlaps (London / NY / Tokyo / Sydney), Tier-1 blackout guard, breaking geopolitical shock radar, CFTC COT institutional positioning, and sovereign yield/VIX/MOVE spreads.
- **Interactive MCP Micro-Apps (`ui://markolis/market-frame`)**: Renders interactive 6-tab HTML5 visual frames inside supporting MCP clients.

---

## Quickstart

### Option A: Direct Cloud Stream (Zero Installation — Recommended)

Configure your MCP client to stream directly from the hosted Streamable HTTP endpoint:

#### 1. Claude Desktop
Add this to `claude_desktop_config.json` (include `headers` with a key from [markolis.com/mcp](https://www.markolis.com/mcp), or omit for anonymous preview mode):
```json
{
  "mcpServers": {
    "markolis": {
      "url": "https://www.markolis.com/api/mcp",
      "headers": {
        "Authorization": "Bearer mk_agent_<YOUR_KEY>"
      }
    }
  }
}
```
*Config file locations:*
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### 2. Cursor, Windsurf & Zed
Use your portable `?key=mk_agent_...` token or Bearer Authorization header:
```json
{
  "mcpServers": {
    "markolis": {
      "url": "https://www.markolis.com/api/mcp?key=mk_agent_<YOUR_KEY>"
    }
  }
}
```

---

### Option B: Node.js STDIO Runner (`npx`)

```json
{
  "mcpServers": {
    "markolis": {
      "command": "npx",
      "args": ["-y", "markolis-mcp"],
      "env": {
        "MARKOLIS_AGENT_KEY": "mk_agent_<YOUR_KEY>"
      }
    }
  }
}
```

---

### Option C: Python STDIO Runner (`uvx` / `python`)

```json
{
  "mcpServers": {
    "markolis": {
      "command": "uvx",
      "args": ["markolis-mcp"],
      "env": {
        "MARKOLIS_AGENT_KEY": "mk_agent_<YOUR_KEY>"
      }
    }
  }
}
```

*Or with standard Python:*
```bash
pip install markolis-mcp
python -m markolis_mcp
```

### Bridge Environment Variables
| Variable | Default | Description |
| :--- | :--- | :--- |
| `MARKOLIS_AGENT_KEY` (or `MARKOLIS_API_KEY`) | *unset* | Optional bearer key (`mk_agent_...`) for 50 to 100,000 calls/day. |
| `MARKOLIS_ENDPOINT` (or `MARKOLIS_MCP_URL`) | `https://www.markolis.com/api/mcp` | Target Streamable HTTP MCP endpoint. |

---

## Available MCP Tools & Prompts

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `render_market_intelligence_frame` | `query` *(str, required)*, `default_symbol` *(str, default: `XAU_USD`)*, `use_llm` *(bool)*, `format` *(`"full"` \| `"json_compact"`)* | Returns CFTC 4.41 compliant analysis and an interactive 6-tab visual micro-app frame (`ui://markolis/market-frame`). Uses **0.1 CU** when `format="json_compact"`. |
| `get_market_telemetry` | `symbol` *(str, required)*, `format` *(`"full"` \| `"json_compact"`)* | Retrieves 100-bin AMT levels (POC, VAH, VAL), Hurst persistence, order book crowd imbalance, empirical H1 Yang-Zhang & jump variation, and COT/sovereign overlays. Uses **0.1 CU** in compact mode. |
| `get_macro_radar` | `symbol` *(str, optional)* | Retrieves global session clocks, liquidity multipliers, Tier-1 news blackouts, breaking shock radar, stablecoin velocity, prediction market odds, FRED real yields, sovereign spreads, and optional per-asset COT overlay. |
| `get_prop_guardian_status` | `account_equity_usd` *(float)*, `daily_loss_limit_pct` *(float)*, `stop_loss_pips` *(float)*, `firm_preset` *(str)* | Audits trailing drawdown headroom, `macro_event_guard` news/shock locks, Bayesian fractional-Kelly sizing, and copyable PineScript v5 code. |
| `get_verified_catalog` | *None* | Lists all **30 verified telemetry streams** and 5 commercial tier capabilities. |

### Built-in MCP Prompts
- `gold-trap-check`: Analyzes trapped retail positioning and stop-hunt clusters (`symbol` optional, default `XAU_USD`).
- `intraday-structure-brief`: Pre-session structural briefing covering Hurst persistence, Shannon entropy, Value Area levels, and conformal price bounds (`symbol` required).
- `prop-drawdown-audit`: Audits prop challenge drawdown buffers, `macro_event_guard` locks, and Bayesian fractional-Kelly sizing.
- `macro-shock-radar`: Evaluates breaking macro/geopolitical shock radar, CFTC COT crowded extremes, sovereign yield/VIX spreads, and news blackout status (`symbol` optional, default `XAU_USD`).

---

## Interactive MCP Micro-Apps

Markolis implements the **Model Context Protocol Apps Specification** (`ui://markolis/market-frame`). When calling `render_market_intelligence_frame`, supporting clients render an interactive HTML5/SVG micro-app containing:
1. **Order Book & Trapped Crowd Histogram**: Retail long vs. short split and resting stop-sweep vectors.
2. **Macro Causal Graph & Sovereign Surface**: Cross-asset SVAR-LiNGAM causal transmission, credit spreads, breaking shock alerts, and sovereign yield/VIX telemetry.
3. **Volatility Regime & Hurst Persistence**: Shannon entropy sparkline, short/medium Hurst exponents, Parkinson, Garman-Klass, Yang-Zhang open-jump volatility, and bipower jump variation.
4. **PropGuardian Drawdown Pacing**: Real-time buffer headroom and Bayesian Kelly sizing.
5. **Session Clock & Blackout Radar**: 24h institutional centers, overlap multipliers, and active Tier-1 catalyst / shock alerts.
6. **Multi-Model Consensus & Brier Leaderboard**: Accuracy-weighted desk consensus.

---

## Quotas & Commercial Tiers

- **Public Pulse (Free)**: `8 calls/day` anonymous preview or `50 calls/day` free with a `mk_agent_` key, `25` web queries/day.
- **Markolis Pro ($79/mo)**: `1,000 MCP calls/day` (`300` web queries/day), unredacted stop-hunt clusters, H1 conformal cones, CFTC COT, and sovereign yield spreads.
- **Prop-Desk Sentinel ($149/mo)**: `3,000 MCP calls/day`, `macro_event_guard`, live drawdown pacing, Bayesian Kelly + 95% CVaR sizing.
- **Institutional Desk ($750/mo)**: `15,000 calls/day`, SVAR-LiNGAM causal DAG, VPIN toxicity, and model calibration metrics.
- **Quant Lakehouse ($5,000/mo)**: `100,000 calls/day` and continuous historical Parquet lakehouse access.

Manage keys and tiers at **[https://www.markolis.com/mcp](https://www.markolis.com/mcp)**.

---

## Regulatory Compliance & Disclaimer

> **CFTC Rule 4.41 Compliance**:
> All quantitative metrics, excursions, order book profiles, and volatility cones delivered by Markolis are empirical statistical estimates based on market structure snapshots. Markolis operates strictly as an impersonal quantitative intelligence engine under the SEC Publisher's Exemption and CFTC Rule 4.41 and does not provide individualized financial advice, trading recommendations, or buy/sell calls.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
