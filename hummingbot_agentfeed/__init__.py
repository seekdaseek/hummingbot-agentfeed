"""AgentFeed liquidations source for Hummingbot, for a Hummingbot that does not ship it yet.

    from hummingbot_agentfeed import register
    register()   # adds "agentfeed" to LiquidationsFactory

then use LiquidationsConfig(connector="agentfeed", ...) exactly as you would with "binance".
"""
from hummingbot_agentfeed.liquidations import AgentFeedLiquidations

__all__ = ["AgentFeedLiquidations", "register"]


def register() -> None:
    """Registers the "agentfeed" source with LiquidationsFactory (safe to call twice)."""
    from hummingbot.data_feed.liquidations_feed.liquidations_factory import LiquidationsFactory

    LiquidationsFactory._liquidation_feeds_map.setdefault("agentfeed", AgentFeedLiquidations)
