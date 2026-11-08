<div align="center">

# Markolis MCP Server

### Institutional Quantitative Market Intelligence & Micro-Apps for AI Agents

[![Official MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.markolis--quant%2Fmarkolis-blue?style=flat-square&logo=anthropic)](https://registry.modelcontextprotocol.io)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-green.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Node 18+](https://img.shields.io/badge/node-18+-brightgreen.svg?style=flat-square&logo=node.js)](https://nodejs.org/)
[![Status](https://img.shields.io/badge/Service-Operational-emerald?style=flat-square)](https://www.markolis.com)

**[Terminal & Web App](https://www.markolis.com)** • **[API Documentation](https://www.markolis.com/docs)** • **[Official Registry](https://registry.modelcontextprotocol.io)**

</div>

---

## Overview

**Markolis** brings institutional quantitative telemetry, 100-bin Auction Market Theory (AMT), order book trapped crowd sentiment, and distribution-free conformal volatility cones to autonomous AI agents and trading desks.

Instead of relying on lagging retail indicators (RSI, MACD, Moving Averages), Markolis queries empirical order book volume distributions across **130+ global financial assets** (Gold, Bitcoin, S&P 500, Nasdaq, EUR/USD, Crude Oil, and FX crosses).

### Key Capabilities
- 🎯 **100-Bin Auction Market Theory**: Point of Control (POC), 70% Value Area (VAH / VAL), and balance rotation regimes.
- 🪤 **Order Book Trapped Crowd Radar**: Net long/short retail cluster offside percentages and nearest stop-sweep vectors.
- ⚡ **Conformal Volatility Cones**: Distribution-free 90% confidence excursion bands calibrated across market sessions.
- 🌐 **Global Macro Radar**: Real-time cross-asset session overlaps (London / NY / Tokyo), liquidity multipliers, and news blackouts.
- 🖥️ **Interactive MCP Micro-Apps (`ui://markolis/market-frame`)**: Renders interactive HTML5 visual auction frames inside AI chat clients.

---

## Quickstart

You can connect Markolis to your favorite AI assistant in seconds:

### Option A: Direct Cloud Stream (Zero Installation — Recommended)

No software installation or local dependencies required. Directly configure your MCP client to stream from the hosted endpoint:

#### 1. Claude Desktop
Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "markolis": {
      "url": "https://www.markolis.com/api/mcp"
    }
  }
}
```
*Config file locations:*
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### 2. Cursor
Open **Cursor Settings** $\rightarrow$ **Features** $\rightarrow$ **MCP** $\rightarrow$ **+ Add New MCP Server**:
- **Name**: `markolis`
- **Type**: `SSE` (or `HTTP`)
- **Server URL**: `https://www.markolis.com/api/mcp`

Or in your project's `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "markolis": {
      "url": "https://www.markolis.com/api/mcp"
    }
  }
}
```

#### 3. Windsurf & Zed
In your MCP configuration:
```json
{
  "mcpServers": {
    "markolis": {
      "url": "https://www.markolis.com/api/mcp"
    }
  }
}
```

---

### Option B: Node.js STDIO Runner (`npx`)

If your MCP client requires a local stdio command:

```json
{
  "mcpServers": {
    "markolis": {
      "command": "npx",
      "args": ["-y", "markolis-mcp"]
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
      "args": ["markolis-mcp"]
    }
  }
}
```

*Or with standard Python:*
```bash
pip install markolis-mcp
python -m markolis_mcp
```

---

## Available MCP Tools

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `render_market_intelligence_frame` | `query` *(str, required)*<br/>`default_symbol` *(str, default: 'XAU_USD')* | Queries market intelligence and returns both empirical quantitative analysis and an interactive visual micro-app frame (`ui://markolis/market-frame`). |
| `get_market_telemetry` | `symbol` *(str, required)* | Retrieves comprehensive quantitative metrics: POC, Value Area, Hurst persistence exponent, order book crowd imbalance, and Garman-Klass volatility. |
| `get_macro_radar` | *None* | Retrieves real-time global macroeconomic radar feeds: active session clocks, liquidity multipliers, upcoming news blackouts, and offshore USD velocity. |
| `get_prop_guardian_status` | *None* | Live systematic risk telemetry for prop challenge pacing: trailing drawdown headroom, daily loss usage, and Bayesian Kelly allocation sizing. |
| `get_verified_catalog` | *None* | Full 26-stream verified asset catalog with Garman-Klass volatility ratings and asset classes. |

---

## Example Prompts

Once installed in Claude or Cursor, simply ask:

- *"Where is the retail crowd trapped on Gold ($XAUUSD)?"*
- *"Show me the 100-bin auction theory profile and Value Area for Bitcoin ($BTCUSD)."*
- *"What is the active macroeconomic session overlap and liquidity multiplier right now?"*
- *"Calculate the 90% conformal volatility cone for EUR/USD heading into the New York session."*

---

## Interactive MCP Micro-Apps

Markolis implements the **Model Context Protocol UI Specification** (`ui://markolis/market-frame`). When calling `render_market_intelligence_frame`, supporting clients render an interactive HTML5 frame containing:
1. **Interactive 100-Bin Auction Histogram**: Real-time volume profiles highlighting Value Area High (VAH), Value Area Low (VAL), and Point of Control (POC).
2. **Order Book Trapped Crowd Sentiment**: Visual long vs. short positioning and stop-sweep risk vectors.
3. **Session Regime Sparklines**: Regime persistence and volatility cone bands.

---

## Quotas & Commercial Tiers

Markolis provides a generous **free tier (25 requests/day)** with zero credit card or registration required. 

For institutional desks, algorithmic trading agents, and quantitative researchers:
- **Free**: 25 queries/day, 131 assets, full MCP access.
- **Pro ($49/mo)**: 300 queries/day, private agent tokens, continuous webhook feeds, and priority execution.
- **Enterprise / Prop Desks**: Dedicated custom streams, Sub-10ms WebSockets, and custom data lakes.

Visit **[https://www.markolis.com](https://www.markolis.com)** to upgrade or manage keys.

---

## Regulatory Compliance & Disclaimer

> **CFTC Rule 4.41 Compliance**:
> All quantitative metrics, excursions, order book profiles, and volatility cones delivered by Markolis are empirical statistical estimates based on market structure snapshots. Markolis operates strictly as a quantitative intelligence engine and does not provide financial advice, trading recommendations, or buy/sell calls.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
