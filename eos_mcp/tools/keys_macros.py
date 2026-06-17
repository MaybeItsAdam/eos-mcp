from ..app import mcp
from ..eos_client import client

@mcp.tool()
def press_key(key_name: str) -> str:
    """Presses and releases a hardkey (e.g., "Data", "About", "Go_To_Cue")."""
    address = f"/eos/key/{key_name}"
    client.send_message(address, 1.0)
    client.send_message(address, 0.0)
    print(f"Sent Key Press: {key_name}")
    return f"Pressed key {key_name}"

@mcp.tool()
def fire_macro(macro: int) -> str:
    """Fires a macro."""
    address = "/eos/macro/fire"
    client.send_message(address, macro)
    print(f"Sent: {address} {macro}")
    return f"Fired Macro {macro}"

@mcp.tool()
def press_softkey(index: int) -> str:
    """Presses a softkey (1-12)."""
    address = f"/eos/softkey/{index}"
    client.send_message(address, 1.0)
    client.send_message(address, 0.0)
    print(f"Sent Softkey: {index}")
    return f"Pressed Softkey {index}"
