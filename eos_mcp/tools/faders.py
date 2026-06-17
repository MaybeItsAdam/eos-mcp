from ..app import mcp
from ..eos_client import client

@mcp.tool()
def set_fader(bank: int, fader: int, level: float) -> str:
    """Sets a fader level (0.0-1.0)."""
    address = f"/eos/fader/{bank}/{fader}"
    client.send_message(address, level)
    print(f"Sent: {address} {level}")
    return f"Set Fader {bank}/{fader} to {level}"

@mcp.tool()
def control_fader_button(bank: int, fader: int, action: str) -> str:
    """Controls fader buttons.

    Args:
        bank: Fader bank/index.
        fader: Fader index.
        action: "load", "unload", "stop", "fire".
    """
    address = f"/eos/fader/{bank}/{fader}/{action}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Fader {bank}/{fader} action: {action}"

@mcp.tool()
def press_direct_select(bank: int, button: int) -> str:
    """Presses a direct select button."""
    address = f"/eos/ds/{bank}/{button}"
    client.send_message(address, 1.0)
    client.send_message(address, 0.0)
    print(f"Sent DS Press: {bank}/{button}")
    return f"Pressed Direct Select {bank}/{button}"
