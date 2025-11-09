# vanet_sim.py
import random
import time
from vanet_node import VehicleNode
from utils import current_millis, hmac_sign

class NetworkSimulator:
    def __init__(self, num_nodes=5, tamper_attack=False, replay_attack=False):
        self.nodes = []
        self.tamper_attack = tamper_attack
        self.replay_attack = replay_attack
        self.prev_packet = None
        for i in range(num_nodes):
            self.nodes.append(VehicleNode(f"V{i+1}", self))

    def deliver(self, sender, packet):
        # Optionally simulate attacks
        if self.tamper_attack and random.random() < 0.3:
            packet["msg"]["payload"]["speed"] += 100  # modify value
            print(f"[Attacker] Tampered message from {sender.id}")

        # Optionally replay an old packet
        if self.replay_attack and self.prev_packet and random.random() < 0.2:
            print("[Attacker] Replaying old message")
            for node in self.nodes:
                if node.id != sender.id:
                    node.receive(self.prev_packet)
            return

        # Normal broadcast
        self.prev_packet = packet
        for node in self.nodes:
            if node.id != sender.id:
                node.receive(packet)

    def run(self, rounds=5, delay=1.5):
        print("🚗 VANET Secure Routing Simulation Started")
        for r in range(rounds):
            print(f"\n--- Round {r+1} ---")
            sender = random.choice(self.nodes)
            sender.broadcast()
            time.sleep(delay)

        print("\n📊 Summary:")
        for node in self.nodes:
            print(f"Node {node.id} - Accepted: {node.accept_count}, Dropped: {node.drop_count}")

if __name__ == "__main__":
    sim = NetworkSimulator(num_nodes=4, tamper_attack=True, replay_attack=True)
    sim.run(rounds=6)
