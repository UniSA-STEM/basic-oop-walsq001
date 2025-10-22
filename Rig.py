"""
File: Rig.py
Description: This module encompasses the Rig class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
import random
from Asset import Asset, DataSpike, CryptoToken, RemovableDrive, SecurityChip, HardwarePatch

MAX_DMG = 2.0

class Rig:
    """
    Represents a hacker's rig.
    Stores assets, can be upgraded, repaired, and attacked.
    """
    def __init__(self, damage=0.0, upgrade=0, base_capacity=5):
        # Each rig starts with 2 DataSpikes and 1 RemovableDrive.
        # Damage starts at 0, broken = False, upgrade level = 0.
        self.__name = random.choice(
            ["Stonewall Server", "Glitchwitch", "Lambda Core", "Nova Core",
             "Cache Cat"]
        )
        self.__damage = damage
        self.__broken = False
        ds = DataSpike()
        rd = RemovableDrive()
        ds.set_unencrypted(2)
        self.__storage = [ds, rd]
        self.__upgrade = upgrade
        self.__base_capacity = base_capacity

    # --- Properties ---
    def get_dmg(self):
        return self.__damage
    def set_dmg(self, dmg):
        if dmg > MAX_DMG:
            dmg = MAX_DMG
        self.__damage = dmg
        self.__broken = self.__damage >= MAX_DMG
    def get_broken(self):
        return self.__broken
    def get_capacity(self):
        return self.__base_capacity + self.__upgrade
    def get_storage(self):
        return self.__storage
    def get_name(self):
        return self.__name
    def get_condition(self):
        if self.__broken:
            return f"Broken (Level {self.__upgrade})"
        elif self.__damage == 0:
            return f"Pristine (Level {self.__upgrade})"
        else:
            return f"Damaged {self.__damage} (Level {self.__upgrade})"
    broken = property(get_broken)
    storage = property(get_storage)
    capacity = property(get_capacity)
    name = property(get_name)
    dmg = property(get_dmg, set_dmg)

    # --- Methods ---
    def add_to_storage(self, asset):
        """
        Attempt to add an asset to this rig.
        - Rejects if not an asset or if quantity <= 0.
        - Rejects if capacity would be exceeded.
        - If an asset of the same type exists, merge into it.
        - Otherwise, append as a new entry.
        """
        if not isinstance(asset, Asset) or asset.quantity() <= 0:
            return False
        if sum(a.quantity() for a in self.__storage) + asset.quantity() > self.capacity:
            return False
        for stored in self.__storage:
            if isinstance(stored, type(asset)):
                stored.merge_from(asset)
                return True
        self.__storage.append(asset)
        return True

    def consume_from_storage(self, asset_type, amount=1):
        """
        Consume an amount of the first matching asset_type in storage.
        - Return 0 if no asset found.
        - Removes the asset from storage if it becomes empty.
        """
        asset = next((a for a in self.__storage if isinstance(a, asset_type)), None)
        if not asset:
            return 0
        consumed = asset.consume(amount)
        if asset.quantity() == 0:
            self.__storage.remove(asset)
        return consumed

    def generate(self):
        """
        Randomly create a new single-unit asset
        and attempt to add it to storage.
        """
        asset_classes = [
            CryptoToken,
            RemovableDrive,
            SecurityChip,
            HardwarePatch,
            DataSpike,
        ]
        chosen = random.choice(asset_classes)
        new_asset = chosen()
        if self.add_to_storage(new_asset):
            return new_asset
        else:
            return None

    def repair(self):
        # Repairs if damaged.
        if self.dmg <= 0:
            print("No repair is needed!")
            return False
        self.dmg = 0
        self.__broken = False
        return True

    def upgrade(self):
        # Increases upgrade level, expands capacity
        self.__upgrade += 1
        print(f"Rig upgraded! New capacity: {self.capacity}")
        return True

    def take_hit(self, hits=1, attacker=None):
        # Calculate per-hit damage floored at 0.25
        per_hit = max(1.0 - 0.25 * self.__upgrade, 0.25)

        # total incoming before clamping
        incoming = per_hit * hits
        new_total = self.dmg + incoming
        self.dmg = new_total
        self.__broken = self.dmg >= MAX_DMG
        print(f"{attacker} launched a DataSpike on {self.name}, causing {incoming} damage.\n"
              f"{self.dmg} damage accumulated.\n")
        return True

    def __str__(self):
        """
        Returns a string representation of the rig.
        """
        storage_str = "\n".join(f"{str(item)}" for item in self.__storage) or "Empty"
        return (f"Rig Name: {self.__name}\n"
                f"Condition: {self.get_condition()}\n"
                f"---Storage---\n"
                f"{storage_str}\n")