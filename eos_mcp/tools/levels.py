from ..app import mcp
from ..eos_client import client


@mcp.tool()
def command_line(command: str) -> str:
    """Sends a command to the ETC Nomad command line.

    Args:
        command: The command string (e.g., "Chan 1 At 50").
    """
    address = "/eos/cmd"
    client.send_message(address, command)
    print(f"Sent: {address} '{command}'")
    return f"Sent command: {command}"

@mcp.tool()
def set_level(value: float) -> str:
    """Sets the level of the currently selected channels (0-100)."""
    address = "/eos/at"
    client.send_message(address, value)
    print(f"Sent: {address} {value}")
    return f"Set level to {value}"

@mcp.tool()
def set_level_mod(modification: str) -> str:
    """Sets level variants.

    Args:
        modification: "out", "home", "remdim", "level", "full", "min", "max", "+%", "-%".
    """
    address = f"/eos/at/{modification}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Set level modification: {modification}"

@mcp.tool()
def set_channel_mod(channel: int, modification: str) -> str:
    """Sets level variants for a specific channel.

    Args:
        channel: Channel number.
        modification: "out", "home", "remdim", "level", "full", "min", "max", "+%", "-%".
    """
    address = f"/eos/chan/{channel}/{modification}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Set Channel {channel} mod: {modification}"

@mcp.tool()
def set_group_mod(group: int, modification: str) -> str:
    """Sets level variants for a specific group.

    Args:
        group: Group number.
        modification: "out", "home", "remdim", "level", "full", "min", "max", "+%", "-%".
    """
    address = f"/eos/group/{group}/{modification}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Set Group {group} mod: {modification}"

@mcp.tool()
def set_parameter(param: str, value: float) -> str:
    """Sets a specific parameter to a value.

    Args:
        param: Parameter name (e.g., "pan", "tilt", "zoom").
        value: Value to set.
    """
    address = f"/eos/param/{param}"
    client.send_message(address, value)
    print(f"Sent: {address} {value}")
    return f"Set {param} to {value}"

@mcp.tool()
def set_parameter_mod(param: str, modification: str) -> str:
    """Sets parameter variants.

    Args:
        param: Parameter name.
        modification: "out", "home", "level", "full", "min", "max", "+%", "-%".
    """
    address = f"/eos/param/{param}/{modification}"
    client.send_message(address, [])
    print(f"Sent: {address}")
    return f"Set {param} modification: {modification}"

@mcp.tool()
def set_dmx(address_num: int, value: int) -> str:
    """Sets a DMX address to a level (0-255)."""
    address = f"/eos/addr/{address_num}/DMX"
    client.send_message(address, value)
    print(f"Sent: {address} {value}")
    return f"Set DMX address {address_num} to {value}"
