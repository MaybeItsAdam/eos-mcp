import re
import threading
from pythonosc import dispatcher, osc_server
from .config import EOS_RX_HOST, EOS_PORT_RX
from .state import state, state_lock, Fader, FaderBank, DirectSelectBank

# --- OSC address regexes (anchored, named numeric segments) --------------

RE_ACTIVE_CUE = re.compile(r"/eos/out/active/cue/(?P<list>\d+)/(?P<cue>\d+)")
RE_PENDING_CUE = re.compile(r"/eos/out/pending/cue/(?P<list>\d+)/(?P<cue>\d+)")
RE_FADER_BANK = re.compile(r"/eos/out/fader/(?P<bank>\d+)")
RE_FADER_LEVEL = re.compile(r"/eos/out/fader/(?P<bank>\d+)/(?P<fader>\d+)")
RE_FADER_NAME = re.compile(r"/eos/out/fader/(?P<bank>\d+)/(?P<fader>\d+)/name")
RE_DS_BANK = re.compile(r"/eos/out/ds/(?P<bank>\d+)")
RE_DS_BUTTON = re.compile(r"/eos/out/ds/(?P<bank>\d+)/(?P<button>\d+)")

# --- OSC handlers --------------------------------------------------------

def handle_active_cue(address, *args):
    """
    Handles /eos/out/active/cue/<list>/<cue> (float argument)
    Example address: /eos/out/active/cue/1/5
    """
    m = RE_ACTIVE_CUE.fullmatch(address)
    if not m:
        return
    list_num = m.group("list")
    cue_num = m.group("cue")
    percent = args[0] if args else 0.0
    with state_lock:
        state.active_cue_list = list_num
        state.active_cue_number = cue_num
        state.active_cue_percent = percent

def handle_active_cue_text(address, *args):
    """Handles /eos/out/active/cue/text (string argument)"""
    if not args:
        return
    text = args[0]
    with state_lock:
        state.active_cue_text = text

def handle_pending_cue(address, *args):
    """
    Handles /eos/out/pending/cue/<list>/<cue>
    """
    m = RE_PENDING_CUE.fullmatch(address)
    if not m:
        return
    list_num = m.group("list")
    cue_num = m.group("cue")
    with state_lock:
        state.pending_cue_list = list_num
        state.pending_cue_number = cue_num

def handle_pending_cue_text(address, *args):
    """Handles /eos/out/pending/cue/text (string argument)"""
    if not args:
        return
    text = args[0]
    with state_lock:
        state.pending_cue_text = text

def handle_live_blind(address, *args):
    """Handles /eos/out/event/state (0=Blind, 1=Live)"""
    if not args:
        return
    value = args[0]
    with state_lock:
        state.live_blind_state = value

def handle_command_line(address, *args):
    """Handles /eos/out/cmd and /eos/out/user/<num>/cmd"""
    if not args:
        return
    value = args[0]
    with state_lock:
        state.command_line = value

def handle_active_chan(address, *args):
    """Handles /eos/out/active/chan"""
    if not args:
        return
    value = args[0]
    with state_lock:
        state.active_channels = value

def handle_fader_bank_label(address, *args):
    """Handles /eos/out/fader/<index> (bank label)"""
    m = RE_FADER_BANK.fullmatch(address)
    if not m or not args:
        return
    bank = int(m.group("bank"))
    label = args[0]
    with state_lock:
        bank_obj = state.faders.setdefault(bank, FaderBank())
        bank_obj.bank_label = label

def handle_fader_level(address, *args):
    """Handles /eos/out/fader/<index>/<fader> (level)"""
    m = RE_FADER_LEVEL.fullmatch(address)
    if not m:
        return
    if not (args and isinstance(args[0], float)):
        return
    bank = int(m.group("bank"))
    fader = int(m.group("fader"))
    level = args[0]
    with state_lock:
        bank_obj = state.faders.setdefault(bank, FaderBank())
        fader_obj = bank_obj.faders.setdefault(fader, Fader())
        fader_obj.level = level

def handle_fader_label(address, *args):
    """Handles /eos/out/fader/<index>/<fader>/name"""
    m = RE_FADER_NAME.fullmatch(address)
    if not m or not args:
        return
    bank = int(m.group("bank"))
    fader = int(m.group("fader"))
    label = args[0]
    with state_lock:
        bank_obj = state.faders.setdefault(bank, FaderBank())
        fader_obj = bank_obj.faders.setdefault(fader, Fader())
        fader_obj.label = label

def handle_ds_bank_label(address, *args):
    """Handles /eos/out/ds/<index>"""
    m = RE_DS_BANK.fullmatch(address)
    if not m or not args:
        return
    bank = int(m.group("bank"))
    label = args[0]
    with state_lock:
        bank_obj = state.direct_selects.setdefault(bank, DirectSelectBank())
        bank_obj.label = label

def handle_ds_button_label(address, *args):
    """Handles /eos/out/ds/<index>/<button>"""
    m = RE_DS_BUTTON.fullmatch(address)
    if not m or not args:
        return
    bank = int(m.group("bank"))
    btn = int(m.group("button"))
    label = args[0]
    with state_lock:
        bank_obj = state.direct_selects.setdefault(bank, DirectSelectBank())
        bank_obj.buttons[btn] = label

def handle_wheel_mode(address, *args):
    if not args:
        return
    value = args[0]
    with state_lock:
        state.wheel_mode = value

def handle_pantilt(address, *args):
    values = list(args)
    with state_lock:
        state.pantilt = values

def handle_xyz(address, *args):
    values = list(args)
    with state_lock:
        state.xyz = values

def default_handler(address, *args):
    pass

def start_osc_listener():
    disp = dispatcher.Dispatcher()

    disp.map("/eos/out/active/cue/*/*", handle_active_cue)
    disp.map("/eos/out/active/cue/text", handle_active_cue_text)
    disp.map("/eos/out/pending/cue/*/*", handle_pending_cue)
    disp.map("/eos/out/pending/cue/text", handle_pending_cue_text)

    disp.map("/eos/out/event/state", handle_live_blind)
    disp.map("/eos/out/cmd", handle_command_line)
    disp.map("/eos/out/user/*/cmd", handle_command_line)
    disp.map("/eos/out/active/chan", handle_active_chan)
    disp.map("/eos/out/wheel", handle_wheel_mode)
    disp.map("/eos/out/pantilt", handle_pantilt)
    disp.map("/eos/out/xyz", handle_xyz)

    disp.map("/eos/out/fader/*", handle_fader_bank_label)
    disp.map("/eos/out/fader/*/*", handle_fader_level)
    disp.map("/eos/out/fader/*/*/name", handle_fader_label)

    disp.map("/eos/out/ds/*", handle_ds_bank_label)
    disp.map("/eos/out/ds/*/*", handle_ds_button_label)

    disp.set_default_handler(default_handler)

    server = osc_server.ThreadingOSCUDPServer((EOS_RX_HOST, EOS_PORT_RX), disp)
    print(f"Serving OSC listener on port {EOS_PORT_RX}")
    server.serve_forever()

def start_listener_thread():
    listener_thread = threading.Thread(target=start_osc_listener, daemon=True)
    listener_thread.start()
    return listener_thread
