# ETCnomad MCP

MCP server for communicating with ETCnomad via OSC

Implements all commands featured [here](https://www.etcconnect.com/WebDocs/Controls/EosFamilyOnlineHelp/en/Content/23_Show_Control/08_OSC/Using_OSC_with_Eos/OSC_Eos_Control.htm#OSCMacro)

## Prerequisites
- ETCnomad (Eos Family software)
- Python 3.10+
- `uv` or `pip`

## Setup

**Configure ETCnomad**:
   - Open Browser:Setup -> System Settings -> System -> Show Control -> OSC
   - Enable **OSC RX** and **OSC TX**
   - Set **OSC UDP RX Port** to 8000
   - Set **OSC UDP TX Port** to 9001

Install Dependencies:
```bash
uv sync
```

## Vision tools

Two tools let the AI *see* the rig to verify cues during pre-programming:

- `capture_visualizer` — screenshots the **Augment3d** 3D visualizer window (when the console
  and this server run on the same machine). On Windows it crops to the window; on macOS it
  brings the app to the front and captures the primary monitor.
- `capture_camera` — grabs a frame from a USB webcam (`source="0"`) or an RTSP IP camera
  (`source="rtsp://..."`), for setups where the visualizer runs on a separate machine.

These require extra dependencies (already declared in `pyproject.toml`, so `uv sync` covers
them). To install manually:
```bash
pip install mss pygetwindow opencv-python pyautogui
```

## Environment Variables

The network configuration can be overridden with environment variables. If unset, the defaults below are used (no behavior change). This lets you point the MCP at a different console or a backup desk without editing code.

| Variable | Default | Description |
| --- | --- | --- |
| `EOS_IP` | `127.0.0.1` | IP address of the Eos console to send OSC commands to (TX target). |
| `EOS_PORT_TX` | `8000` | UDP port the MCP sends OSC commands to (must match the console's OSC UDP RX Port). |
| `EOS_PORT_RX` | `9001` | UDP port the MCP listens on for OSC replies (must match the console's OSC UDP TX Port). |
| `EOS_RX_HOST` | `0.0.0.0` | Local interface the OSC listener binds to. |

Example:
```bash
EOS_IP=192.168.1.50 EOS_PORT_TX=8000 EOS_PORT_RX=9001 uv run eos_server.py
```

## Project layout

The server is organised as the `eos_mcp` package; `eos_server.py` is a thin entry shim that calls `eos_mcp.server.run()`.

```
eos_server.py            # entry shim (preserves `uv run eos_server.py`)
eos_mcp/
  config.py              # env-driven network config (EOS_IP, ports, host)
  app.py                 # the shared FastMCP instance
  eos_client.py          # the OSC UDP client
  state.py               # typed state dataclasses + state + lock
  osc_listener.py        # OSC address regexes, handlers, listener thread
  prompts.py             # the system-instructions prompt
  server.py              # run(): register tools/prompts, start listener, run server
  tools/                 # @mcp.tool() functions grouped by domain
    levels.py  wheels.py  color_position.py  selection.py  keys_macros.py
    presets.py  faders.py  cue_list_banks.py  playback.py  queries.py
```

## Usage

### Running Locally
```bash
uv run eos_server.py
```

### Claude Desktop Configuration
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "etc-nomad": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "python-osc",
        "/absolute/path/to/eos_server.py"
      ]
    }
  }
}
```
