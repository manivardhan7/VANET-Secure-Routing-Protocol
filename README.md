VANET Secure Routing Prototype - README
--------------------------------------

What this contains:
- A Python prototype simulating VANET vehicle nodes broadcasting signed/hmac'ed messages.
- Detection of message tampering and replay attacks.
- Optional RSA signing variant (requires `cryptography`).

Files:
- utils.py          : Crypto + message helpers
- vanet_node.py     : Vehicle node implementation
- vanet_sim.py      : Simulator (main)
- ns3_vanet_skeleton.cc : NS-3 skeleton (C++), to be extended for NS-3 port.

Run (Python prototype):
1) Optional: create virtualenv
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

2) Install optional RSA deps (only if using RSA):
   pip install -r requirements.txt

3) Run the simulator:
   python vanet_sim.py

What it does:
- Spawns N simulated vehicle nodes.
- Each node broadcasts periodic messages containing: id, position, timestamp, nonce, payload.
- Messages are authenticated with HMAC-SHA256 using a shared secret.
- Receiver verifies HMAC, checks timestamp and nonce to detect replay/tampering.
- Simulator can inject an attacker that tampers message or replays old messages.

Extension / NS-3 port:
- Use ns-3 C++ skeleton to create nodes and attach applications that send/receive messages.
- Implement message HMAC/signing in application layer.
- Evaluate metrics (packet delivery ratio, detection rate, delay).

Notes:
- This prototype focuses on logic; it does not simulate physical radio propagation or MAC/PHY layers.
- For realistic experiments, port the application logic to NS-3 and use wireless channel models provided by NS-3.
