from ..app import mcp
from ..eos_client import client

@mcp.tool()
def select_channel(channel: str) -> str:
    """Selects a channel number (or range string)."""
    address = "/eos/chan"
    try:
        val = int(channel)
        client.send_message(address, val)
    except ValueError:
        return f"Invalid channel number: {channel}. Use command_line for ranges."
    print(f"Sent: {address} {channel}")
    return f"Selected Channel {channel}"

@mcp.tool()
def select_group(group: int) -> str:
    """Selects a group."""
    address = "/eos/group"
    client.send_message(address, group)
    print(f"Sent: {address} {group}")
    return f"Selected Group {group}"

@mcp.tool()
def select_address_target(address_num: int) -> str:
    """Selects an address (as a target)."""
    address = "/eos/addr"
    client.send_message(address, address_num)
    print(f"Sent: {address} {address_num}")
    return f"Selected Address {address_num}"

@mcp.tool()
def select_curve(curve: int) -> str:
    """Selects a curve."""
    address = "/eos/curve"
    client.send_message(address, curve)
    print(f"Sent: {address} {curve}")
    return f"Selected Curve {curve}"

@mcp.tool()
def select_effect(effect: int) -> str:
    """Selects an effect."""
    address = "/eos/fx"
    client.send_message(address, effect)
    print(f"Sent: {address} {effect}")
    return f"Selected Effect {effect}"

@mcp.tool()
def select_pixel_map(pixmap: int) -> str:
    """Selects a Pixel Map."""
    address = "/eos/pixmap"
    client.send_message(address, pixmap)
    print(f"Sent: {address} {pixmap}")
    return f"Selected Pixel Map {pixmap}"

@mcp.tool()
def open_magic_sheet(ms: int) -> str:
    """Opens a Magic Sheet."""
    address = "/eos/ms"
    client.send_message(address, ms)
    print(f"Sent: {address} {ms}")
    return f"Opened Magic Sheet {ms}"
