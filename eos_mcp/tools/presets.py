from ..app import mcp
from ..eos_client import client

@mcp.tool()
def fire_preset(preset: int) -> str:
    """Fires (recalls) a preset."""
    address = "/eos/preset/fire"
    client.send_message(address, preset)
    print(f"Sent: {address} {preset}")
    return f"Fired Preset {preset}"

@mcp.tool()
def fire_palette(palette_type: str, number: int) -> str:
    """Fires a palette.

    Args:
        palette_type: "intensity" (ip), "focus" (fp), "color" (cp), or "beam" (bp).
        number: Palette number.
    """
    type_map = {
        "intensity": "ip", "ip": "ip",
        "focus": "fp", "fp": "fp",
        "color": "cp", "cp": "cp",
        "beam": "bp", "bp": "bp"
    }
    pt = type_map.get(palette_type.lower())
    if not pt:
        return "Invalid palette type. Use intensity, focus, color, or beam."

    address = f"/eos/{pt}/fire"
    client.send_message(address, number)
    print(f"Sent: {address} {number}")
    return f"Fired {palette_type} palette {number}"

@mcp.tool()
def recall_snapshot(snapshot: int) -> str:
    """Recalls a snapshot."""
    address = "/eos/snap"
    client.send_message(address, snapshot)
    print(f"Sent: {address} {snapshot}")
    return f"Recalled Snapshot {snapshot}"

@mcp.tool()
def bump_sub(sub: int, level: float = 1.0) -> str:
    """Bumps a submaster to a level (default 1.0 / 100%)."""
    address = f"/eos/sub/{sub}/fire"
    client.send_message(address, level)
    print(f"Sent: {address} {level}")
    return f"Bumped Sub {sub} to {level}"
