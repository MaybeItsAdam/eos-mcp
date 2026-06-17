from .app import mcp
from .osc_listener import start_listener_thread

def run():
    # Importing these modules registers their @mcp.tool() / @mcp.prompt() decorators.
    from . import tools  # noqa: F401  (tools/__init__ imports every tool submodule)
    from . import prompts  # noqa: F401
    start_listener_thread()
    mcp.run()
