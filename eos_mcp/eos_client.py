from pythonosc import udp_client
from .config import EOS_IP, EOS_PORT_TX
client = udp_client.SimpleUDPClient(EOS_IP, EOS_PORT_TX)
