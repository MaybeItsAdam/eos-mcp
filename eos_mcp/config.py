import os
EOS_IP = os.environ.get("EOS_IP", "127.0.0.1")
EOS_PORT_TX = int(os.environ.get("EOS_PORT_TX", "8000"))
EOS_PORT_RX = int(os.environ.get("EOS_PORT_RX", "9001"))
EOS_RX_HOST = os.environ.get("EOS_RX_HOST", "0.0.0.0")
