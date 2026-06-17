from .app import mcp

@mcp.prompt()
def system_instructions() -> str:
    """Returns the system instructions for using this MCP server."""
    return (
        "You are controlling an ETC Eos lighting console via OSC.\n"
        "The current state of the console (cues, faders, etc.) is NOT automatically known.\n"
        "You MUST call the `sync_state` tool immediately upon starting to populate the state.\n"
        "Wait for the confirmation message before querying for specific status.\n"
    )
