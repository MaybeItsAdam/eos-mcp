import time
from ..app import mcp
from ..eos_client import client
from ..state import state, state_lock


@mcp.tool()
def get_active_cue() -> str:
    """Returns the current active cue."""
    with state_lock:
        list_num = state.active_cue_list
        cue_num = state.active_cue_number
        percent = state.active_cue_percent
        text = state.active_cue_text
    if cue_num is None:
        return "No active cue data received yet."
    return (f"Active Cue: {list_num}/{cue_num} "
            f"({percent*100:.0f}%) "
            f"Label: '{text}'")

@mcp.tool()
def get_pending_cue() -> str:
    """Returns the current pending cue."""
    with state_lock:
        list_num = state.pending_cue_list
        cue_num = state.pending_cue_number
        text = state.pending_cue_text
    if cue_num is None:
        return "No pending cue data received yet."
    return (f"Pending Cue: {list_num}/{cue_num} "
            f"Label: '{text}'")

@mcp.tool()
def get_live_blind_state() -> str:
    """Returns the current Live/Blind state."""
    with state_lock:
        live = state.live_blind_state == 1
    state_str = "Live" if live else "Blind"
    return f"Console State: {state_str}"

@mcp.tool()
def get_command_line() -> str:
    """Returns the current command line text."""
    with state_lock:
        command_line = state.command_line
    return f"Command Line: {command_line}"

@mcp.tool()
def get_selection() -> str:
    """Returns the current active channel selection."""
    with state_lock:
        active_channels = state.active_channels
    return f"Selected Channels: {active_channels}"

@mcp.tool()
def get_faders(bank: int) -> str:
    """Returns the status of faders in a specific bank (1-based)."""
    with state_lock:
        if bank not in state.faders:
            return f"No data for Fader Bank {bank}"
        fader_bank = state.faders[bank]
        bank_label = fader_bank.bank_label
        fader_rows = [(f_idx, fader.label, fader.level)
                      for f_idx, fader in fader_bank.faders.items()]

    bank_info = f"Bank {bank} ({bank_label}):\n"
    fader_info = []
    for f_idx, label, level in fader_rows:
        fader_info.append(f"  Fader {f_idx}: {label} = {level:.2f}")

    if not fader_info: return bank_info + "  No faders populated."
    return bank_info + "\n".join(fader_info)

@mcp.tool()
def get_direct_selects(bank: int) -> str:
    """Returns the status of a Direct Select bank (1-based)."""
    with state_lock:
        if bank not in state.direct_selects:
            return f"No data for DS Bank {bank}"
        ds_bank = state.direct_selects[bank]
        label = ds_bank.label
        btn_rows = list(ds_bank.buttons.items())

    bank_info = f"DS Bank {bank} ({label}):\n"
    btn_info = []
    for btn_idx, btn_label in btn_rows:
        btn_info.append(f"  Btn {btn_idx}: {btn_label}")

    if not btn_info: return bank_info + "  No buttons populated."
    return bank_info + "\n".join(btn_info)

@mcp.tool()
def get_system_state() -> str:
    """Returns aggregate system state information."""
    with state_lock:
        live = state.live_blind_state == 1
        wheel_mode = state.wheel_mode if state.wheel_mode is not None else "Unknown"
        pantilt = state.pantilt
        xyz = state.xyz

    state_str = "Live" if live else "Blind"
    info = [
        f"Console State: {state_str}",
        f"Wheel Mode: {wheel_mode}",
    ]
    if pantilt:
        info.append(f"Pan/Tilt: {pantilt}")
    if xyz:
        info.append(f"XYZ: {xyz}")

    return "\n".join(info)

@mcp.tool()
def sync_state() -> str:
    """
    Forces Eos to re-send all current status information.
    STRONGLY RECOMMENDED: Call this tool immediately upon startup to populate the state.
    After sending the requests, this waits for the console to respond before returning.
    """
    client.send_message("/eos/get/cue/active", [])
    client.send_message("/eos/get/cue/pending", [])

    client.send_message("/eos/get/version", [])
    client.send_message("/eos/get/cmd", [])
    client.send_message("/eos/get/setup", [])

    # Request fader banks (0, 1, 2)
    client.send_message("/eos/fader/0/config", [])
    client.send_message("/eos/fader/1/config", [])

    # Request direct selects bank 1
    client.send_message("/eos/ds/1/config", [])

    # Wait for the console's OSC replies to populate the shared state.
    SYNC_TIMEOUT = 1.5   # seconds to wait for any reply before giving up
    SYNC_POLL_INTERVAL = 0.05  # seconds between state checks
    deadline = time.monotonic() + SYNC_TIMEOUT
    populated = False
    while time.monotonic() < deadline:
        with state_lock:
            populated = (
                state.command_line != ""
                or state.active_cue_number is not None
                or state.wheel_mode is not None
                or len(state.faders) > 0
            )
        if populated:
            break
        time.sleep(SYNC_POLL_INTERVAL)

    if populated:
        return "Synchronization complete — Eos responded and state is populated."
    return (
        f"Synchronization requests sent, but no response from Eos within {SYNC_TIMEOUT}s. "
        "The console may be unreachable or OSC TX may be disabled — verify the connection "
        "before trusting state."
    )
