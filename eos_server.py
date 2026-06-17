"""Entry point for the ETC Eos MCP server.

The implementation now lives in the ``eos_mcp`` package; this thin shim
preserves the documented launch command (``uv run eos_server.py``) and the
existing ``claude_desktop_config.json`` configuration.
"""

from eos_mcp.server import run

if __name__ == "__main__":
    run()
