from ..app import mcp
from ..eos_client import client


@mcp.tool()
def set_xyz(x: float, y: float, z: float) -> str:
    """Sets XYZ position."""
    address = "/eos/xyz"
    client.send_message(address, [x, y, z])
    print(f"Sent: {address} {x}, {y}, {z}")
    return f"Set XYZ to {x}, {y}, {z}"

@mcp.tool()
def set_color_hs(hue: float, saturation: float) -> str:
    """Sets color using Hue (0-360) and Saturation (0-100)."""
    address = "/eos/color/hs"
    client.send_message(address, [hue, saturation])
    print(f"Sent: {address} {hue}, {saturation}")
    return f"Set Color HS: {hue}, {saturation}"

@mcp.tool()
def set_color_rgb(red: float, green: float, blue: float) -> str:
    """Sets color using RGB values (0.0-1.0)."""
    address = "/eos/color/rgb"
    client.send_message(address, [red, green, blue])
    print(f"Sent: {address} {red}, {green}, {blue}")
    return f"Set Color RGB: {red}, {green}, {blue}"

@mcp.tool()
def set_color_xy(x: float, y: float) -> str:
    """Sets color using CIE xy coordinates (0.0-1.0)."""
    address = "/eos/color/xy"
    client.send_message(address, [x, y])
    print(f"Sent: {address} {x}, {y}")
    return f"Set Color XY: {x}, {y}"

@mcp.tool()
def set_pan_tilt(pan: float, tilt: float) -> str:
    """Sets Pan and Tilt (0.0-1.0 range usually maps to max range)."""
    address = "/eos/pantilt/xy"
    client.send_message(address, [pan, tilt])
    print(f"Sent: {address} {pan}, {tilt}")
    return f"Set Pan/Tilt to {pan}, {tilt}"
