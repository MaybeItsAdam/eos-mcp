from ..app import mcp
from ..eos_client import client


@mcp.tool()
def wheel_level(ticks: float) -> str:
    """Adjusts the level wheel.

    Args:
        ticks: Number of ticks (positive/negative). e.g. 1.0, -1.0.
    """
    address = "/eos/wheel/level"
    client.send_message(address, ticks)
    print(f"Sent: {address} {ticks}")
    return f"Adjusted Level Wheel by {ticks}"

@mcp.tool()
def wheel_parameter(param: str, ticks: float) -> str:
    """Adjusts a parameter wheel.

    Args:
        param: Parameter name (e.g. "pan").
        ticks: Number of ticks.
    """
    address = f"/eos/wheel/{param}"
    client.send_message(address, ticks)
    print(f"Sent: {address} {ticks}")
    return f"Adjusted {param} Wheel by {ticks}"

@mcp.tool()
def switch_parameter(param: str, ticks: float) -> str:
    """Sets switch mode for repeats.

    Args:
        param: Parameter name.
        ticks: Tick rate.
    """
    address = f"/eos/switch/{param}"
    client.send_message(address, ticks)
    print(f"Sent: {address} {ticks}")
    return f"Set Switch {param} to {ticks}"
