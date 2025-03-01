from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel


class Direction(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class LookResponse(BaseModel):
    title: str
    description: str


@dataclass
class AppContext:
    state: dict


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    try:
        # TODO: Sample the initial starting room
        yield AppContext(state={})
    finally:
        pass


mcp = FastMCP("Tapestry", log_level="ERROR", lifespan=app_lifespan)


@mcp.tool()
async def look(ctx: Context) -> LookResponse:
    """Look around in the current room to see what is there."""
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return LookResponse(title="Test Room", description="You see a room.")


@mcp.tool()
async def go(direction: Direction, ctx: Context) -> str:
    """Move into a room that is in a particular direction."""
    # TODO: Sample a new room based on the direction and the app context (i.e. existing room)
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return f"You move {direction.value}."


if __name__ == "__main__":
    import asyncio

    asyncio.run(mcp.run_stdio_async())
