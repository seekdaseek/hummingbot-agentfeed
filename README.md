# hummingbot-agentfeed

An AgentFeed source for Hummingbot's liquidations feed (`hummingbot/data_feed/liquidations_feed`), for a Hummingbot that does not ship it yet.
With it, switching a bot's liquidations source is one config line: `connector="agentfeed"`.

**What it gives you.** Cross-venue liquidation pressure, computed by AgentFeed, in 5-second buckets: for every symbol and every bucket
that held a liquidation, the USD, base quantity and VWAP of the long positions and of the short positions that were liquidated, all venues
combined into one figure, plus (in the raw answer) the dominant side and the pressure against the symbol's own baseline.
The source turns each bucket side into one Hummingbot `Liquidation` (`LiquidationSide.LONG` = a long was liquidated). `quantity` is the
summed base quantity and `price` the VWAP; `timestamp` is the start of the bucket in milliseconds.

**What it is not.** It is not a stream of individual liquidations. Numbers are rounded by the server (2 significant figures for USD and
quantity, 3 for the VWAP), there is no print count, and a bucket is served once it is 10 seconds old, so a row reaches you 10 to 20 seconds
after the liquidation. If you need every print the moment it happens, use a venue's own stream.

**It costs money.** The route is paid: $0.001 a call over x402, **$0.0005 a call with a prepaid key**. At a 30-second poll that is 2,880
calls a day, **about $1.44 a day on a key**; at 60 seconds, $0.72; at the 10-second minimum, $4.32. For a bot that polls all day there is also a flat
30-day pass for this route only, $25 (about $0.83 a day). A call that returns nothing is still a call. The server
allows one call per 10 seconds per key. Buy a key or a pass at <https://x402.ochinimus.app/keys>; a failed or refused call is never billed.

## Use it from a script (the five lines)

```python
from hummingbot_agentfeed import register
register()   # adds "agentfeed" to LiquidationsFactory
from hummingbot.data_feed.liquidations_feed.liquidations_factory import LiquidationsConfig, LiquidationsFactory
feed = LiquidationsFactory.get_liquidations_feed(LiquidationsConfig(connector="agentfeed", trading_pairs={"BTC-USDT", "ETH-USDT"}, max_retention_seconds=300))
feed.start()   # then feed.ready, feed.liquidations_df(), feed.liquidations_df("BTC-USDT") as with any liquidations feed
```

The key is read from the `AGENTFEED_API_KEY` environment variable (or pass `api_key=SecretStr(...)` in `LiquidationsConfig`). It is sent as the
`X-AgentFeed-Key` header and never logged. With no key, or a refused or empty one, the feed logs one clear line, stays not ready and checks
again every five minutes; it does not spin.

## Install

Into the Hummingbot environment: `pip install .` from this folder (it only needs `bidict`, which Hummingbot already has). Hummingbot itself
must be importable; this package is a source, not a fork.

## Limits

USDT perpetuals only (`BASE-USDT` pairs), at most 20 pairs per feed, the server keeps 24 hours, poll interval 30 s by default and 10 s at
the shortest. With no `trading_pairs` the route serves SOL, BTC, ETH, XRP and DOGE.

## Tests

From a Hummingbot checkout with its Cython modules built: `PYTHONPATH=<this folder> python -m pytest <this folder>/tests`.
The tests run against an unmodified Hummingbot `development` branch: no change to Hummingbot is needed.

Apache-2.0. Not financial advice.
