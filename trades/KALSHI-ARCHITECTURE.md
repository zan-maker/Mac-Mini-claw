# Kalshi-Sportsbook Mispricing Agent

## Overview

This project implements an AI-driven arbitrage and mispricing engine between Kalshi event markets and one or more sportsbook APIs. Kalshi provides regulated event contracts with an API for market data and trading, while sportsbooks provide odds on overlapping real-world events.

## Architecture

### Data Connectors
- `KalshiClient`: authenticated REST access to events, markets, order books, orders, and positions.
- `SportsbookClient` interface: standardized odds/trading API for each book.

### Canonical Event Layer
- Normalizes events across venues (teams, timing, league, market type).
- Stores mapping between Kalshi contract IDs and sportsbook market IDs.

### Pricing & Mispricing Engine
- Converts all odds to implied probabilities (vig-adjusted for sportsbooks).
- Computes pure arbitrage opportunities and directional mispricings.
- Outputs candidate trades with suggested stakes and expected value.

### Execution & Risk
- Enforces per-market, per-venue, and global exposure limits.
- Handles order placement, cancellation, and partial fills.
- Includes a global "kill switch" and logging for all trades.

### AI Agent
- Orchestrates scanning, ranking, and selection of mispricings.
- Interacts via natural language for queries and reports.
- Learns from performance data to refine search and sizing rules.

## Kalshi Integration

### Authentication
- RSA-signed requests using API key ID and private key.
- Shared `KalshiClient` handles signing, timestamping, and rate limits.

### Market Data
- Endpoints to list events and markets.
- Public market data for series info and order books.
- Scheduled snapshots plus real-time updates where available.

### Trading
- Order placement, modification, and cancellation.
- Portfolio and position retrieval for real-time risk tracking.

## Sportsbook Integration

### `SportsbookClient` Interface
- `get_odds(event_id)` for all relevant markets and outcomes.
- `place_bet(event_id, outcome, stake, price_limit)`.
- `get_open_bets()` and `get_balance()`.

### Adapters
- One implementation per sportsbook, handling odds format, limits, and error modes.

## Event Mapping

### Canonical Event Model
- `sport`, `league`, `home_team`, `away_team`, `start_time`, `venue`.
- `market_type` (`moneyline`, `spread`, `total`, `prop`).
- `kalshi_contract_ids[]` and `sportsbook_market_ids[]`.

### Mapping Logic
- Rule-based string and datetime matching plus manual overrides.
- Settlement rule compatibility flags.

## Mispricing Logic

### Odds Normalization
- Convert all prices to implied probabilities.
- Adjust sportsbook odds for margin; adjust for Kalshi fee structure.

### Arbitrage Detection
- For each event, search stake vectors that yield non-negative payoff in all states.
- Filter by minimum guaranteed profit and minimum stake size.

### Value Opportunities
- Rank events where Kalshi vs sportsbook probabilities diverge beyond a threshold.
- Allow user-defined models for "fair" probability estimates.

## Risk Management

### Limits
- Per-outcome and per-market exposure caps.
- Per-venue and global loss/drawdown limits.

### Execution Strategy
- Leg ordering and retry logic.
- Handling of partial fills and limit/market order choices.

## AI Agent Behavior

### Core Tasks
- Monitor target markets and refresh mispricing set.
- Propose and explain trades to the user.
- Adapt thresholds and focus areas based on P&L and feedback.

### Interfaces
- CLI and/or web dashboard.
- Natural-language prompt interface ("Show top mispricings in NBA tonight").

## Data & Logging

### Store
- All odds snapshots used for decisions.
- Trade instructions, fills, and P&L.
- Features for later model training.

### Analysis
- Backtests of mispricing filters.
- Performance by venue, sport, and time horizon.

## Setup

### Configure API keys and private keys for:
- Kalshi
- Each sportsbook

### Run services:
- `data-feeder` for odds ingestion
- `mispricing-engine` for detection
- `trader` for execution
- `agent` for AI orchestration

## Roadmap

- Add more market types (spreads, totals, props).
- Improve event-matching via ML.
- Train models to predict which mispricings are most persistent/profitable.

---

*Kalshi-Sportsbook Mispricing Agent Architecture*
