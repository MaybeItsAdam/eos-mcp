from ..app import mcp
from ..eos_client import client


@mcp.tool()
def config_cue_list_bank(index: int, list_num: int, prev: int = 2, pending: int = 6) -> str:
    """Configures an OSC Cue List Bank."""
    address = f"/eos/cuelist/{index}/config/{list_num}/{prev}/{pending}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Configured Cue List Bank {index} for List {list_num}"

@mcp.tool()
def page_cue_list_bank(index: int, delta: int) -> str:
    """Pages a Cue List Bank up or down."""
    address = f"/eos/cuelist/{index}/page/{delta}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Paged Cue List Bank {index} by {delta}"

@mcp.tool()
def select_cue_list_bank_cue(index: int, cue: str) -> str:
    """Selects a cue in a Cue List Bank (jumps to it)."""
    address = f"/eos/cuelist/{index}/select/{cue}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Cue List Bank {index} jump to cue {cue}"

@mcp.tool()
def reset_cue_list_bank(index: int) -> str:
    """Resets a Cue List Bank."""
    address = f"/eos/cuelist/{index}/reset"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Reset Cue List Bank {index}"
