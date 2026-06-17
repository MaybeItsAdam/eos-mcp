from ..app import mcp
from ..eos_client import client


@mcp.tool()
def fire_cue(list_number: int, cue_number: str) -> str:
    """Fires a specific cue."""
    address = f"/eos/cue/{list_number}/{cue_number}/fire"
    client.send_message(address, 1.0)
    print(f"Sent: {address}")
    return f"Fired cue {cue_number} in list {list_number}"

@mcp.tool()
def go_cue() -> str:
    """Presses the Go button for the master playback pair."""
    address = "/eos/key/go_0"
    client.send_message(address, 1.0)
    client.send_message(address, 0.0)
    print(f"Sent Go")
    return "Pressed Go"

@mcp.tool()
def stop_back_cue() -> str:
    """Presses the Stop/Back button."""
    address = "/eos/key/stop"
    client.send_message(address, 1.0)
    client.send_message(address, 0.0)
    print(f"Sent Stop/Back")
    return "Pressed Stop/Back"

@mcp.tool()
def request_setup() -> str:
    """Requests setup info."""
    address = "/eos/get/setup"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return "Requested setup info."

@mcp.tool()
def reset_osc() -> str:
    """Resets OSC connections."""
    address = "/eos/reset"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return "Sent OSC Reset"
