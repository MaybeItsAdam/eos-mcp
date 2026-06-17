from dataclasses import dataclass, field
from typing import Optional
import threading

# --- Typed state model ---------------------------------------------------

@dataclass
class Fader:
    level: float = 0.0
    label: str = ""

@dataclass
class FaderBank:
    bank_label: str = ""
    faders: dict = field(default_factory=dict)  # fader index (int) -> Fader

@dataclass
class DirectSelectBank:
    label: str = ""
    buttons: dict = field(default_factory=dict)  # button index (int) -> label (str)

@dataclass
class EosState:
    active_cue_list: Optional[str] = None
    active_cue_number: Optional[str] = None
    active_cue_percent: float = 0.0
    active_cue_text: str = ""
    pending_cue_list: Optional[str] = None
    pending_cue_number: Optional[str] = None
    pending_cue_text: str = ""
    live_blind_state: int = 1
    command_line: str = ""
    active_channels: str = ""
    faders: dict = field(default_factory=dict)          # bank index (int) -> FaderBank
    direct_selects: dict = field(default_factory=dict)  # bank index (int) -> DirectSelectBank
    wheel_mode: Optional[object] = None
    pantilt: list = field(default_factory=list)
    xyz: list = field(default_factory=list)

state = EosState()
state_lock = threading.Lock()
