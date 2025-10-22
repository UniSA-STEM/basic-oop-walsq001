"""
File: main.py
Description: This module is the main program, importing the necessary modules
and ensuring they interact per the Basic OOP brief.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Hacker import Hacker
from Asset import Asset, DataSpike, CryptoToken, RemovableDrive, SecurityChip, HardwarePatch

from Hacker import Hacker
from Asset import DataSpike, SecurityChip, HardwarePatch, CryptoToken

# Create two hackers
p1 = Hacker()
p2 = Hacker()

print("\n--- Initial State ---")
print(p1)
print(p2)

# Acquire rigs
p1.get_rig()
p2.get_rig()

print("\n--- After Rig Acquisition ---")
print(p1)
print(p2)

# Generate some assets
print("\n--- Generating Assets ---")
for _ in range(3):
    new_asset = p1.generate()
    if new_asset:
        print(f"{p1.get_name()} generated: {new_asset}")
print(p1)

# Try upgrading without a patch
print("\n--- Upgrade without HardwarePatch ---")
print("Upgrade result:", p1.upgrade_rig())

# Add a HardwarePatch manually for testing
patch = HardwarePatch()
p1._Hacker__inventory.append(patch)
print("Upgrade result with patch:", p1.upgrade_rig())

# Encrypt without a SecurityChip
print("\n--- Encrypt without SecurityChip ---")
print("Encrypt result:", p1.encrypt_assets(DataSpike, 1))

# Add a SecurityChip and encrypt
chip = SecurityChip()
p1._Hacker__inventory.append(chip)
print("Encrypt result with chip:", p1.encrypt_assets(DataSpike, 1))
print(p1)

# Launch an attack
print("\n--- Launch Attack ---")
damage = p1.launch_attack(p2, hits=2)
print(f"Damage dealt: {damage}")
print(p2)

# Force p2’s rig to break
print("\n--- Breaking Rig ---")
while not p2.rig.broken:
    p1.rig.consume_from_storage(DataSpike, 1)  # ensure spikes
    p2.rig.take_hit(1, attacker=p1.get_name())
print(p2)

# Extract assets from broken rig
print("\n--- Extract Assets ---")
extracted = p1.extract_assets(p2)
print(f"Assets extracted: {extracted}")
print(p1)
print(p2)

# Repair rig
print("\n--- Repair Rig ---")
token = CryptoToken()
p2._Hacker__inventory.append(token)
print("Repair result:", p2.repair_rig())
print(p2)

# Demonstrate storing and retrieving assets
print("\n--- Store and Retrieve Assets ---")
# Move a CryptoToken from inventory into rig storage
print("Store CryptoToken:", p1.store_asset(CryptoToken, 1))
print(p1)
# Move it back into inventory
print("Retrieve CryptoToken:", p1.get_asset(CryptoToken, 1))
print(p1)

# Demonstrate trace reaching max
print("\n--- Trace Level Test ---")
for _ in range(6):
    p1.set_trace()
print("Trace level:", p1.get_trace())
print("Attempting attack while exposed:", p1.launch_attack(p2))

