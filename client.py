import json

import mcp.types as types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich.console import Console

server_params = StdioServerParameters(command="python", args=["server.py"], env=None)


async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    print(message.model_dump_json(indent=2))
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            await session.initialize()

            tools = await session.list_tools()

            # # List available prompts
            # prompts = await session.list_prompts()
            # # Get a prompt
            # prompt = await session.get_prompt("example-prompt", arguments={"arg1": "value"})
            # # List available resources
            # resources = await session.list_resources()
            # # Read a resource
            # content, mime_type = await session.read_resource("file://some/path")

            console = Console(width=60)

            result = await session.call_tool("look", arguments={})
            room = json.loads(result.content[0].text)

            while True:
                console.print(f"[cyan]{room['title']}", justify="center")
                console.print(room["description"])

                cmd = console.input("[green]> ")

                # TODO: Have this be an agent with access to tools
                if cmd in ["exit", "quit"]:
                    break
                elif cmd in ["north", "south", "east", "west"]:
                    result = await session.call_tool("go", arguments={"direction": cmd})
                    console.print(f"[bold magenta]{result.content[0].text}")
                    result = await session.call_tool("look", arguments={})
                    room = json.loads(result.content[0].text)
                elif cmd == "look":
                    pass
                else:
                    console.print("[bold red]Unknown command.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
