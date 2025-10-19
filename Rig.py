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
    def __init__(self):
        self.__name = random.choice(
            ["Stonewall Server", "Glitchwitch", "Lambda Core", "Nova Core",
             "Cache Cat"]
        )
        self.__damage = 0.0
        self.__broken = False
        data_spike = DataSpike()
        data_spike.quantity = 2
        self.__storage: list[Asset] = [data_spike]
        self.__upgrade = 0
        self.__base_capacity = 8

    def __str__(self):
        storage_str = "\n".join(f"{str(item)}" for item in self.__storage) or "Empty"
        return (f"Rig Name: {self.__name}\n"
                f"Damage: {self.__damage}\n"
                f"Broken: {self.__broken}\n"
                f"Storage: {storage_str}\n"
                f"Upgrade: {self.__upgrade}\n")

    def get_capacity(self):
        return self.__base_capacity + self.__upgrade

    def add_to_storage(self, asset: Asset):
        current_total = sum(a.quantity for a in self.__storage)
        if current_total + asset.quantity > self.capacity:
            print("Storage is full, cannot add asset!")
            return False
        for stored in self.__storage:
            if isinstance(stored, type(asset)):
                stored.merge_from(asset)
                return True
        self.__storage.append(asset)
        return True

    def consume_from_storage(self, asset_type, amount=1):
        for asset in self.__storage:
            if isinstance(asset, asset_type):
                still_has = asset.consume(amount)
                if not still_has:
                    self.__storage.remove(asset)
                return True
        return False

    def get_damage(self):
            return self.__damage

    def set_damage(self, damage):
        if damage < 0:
            damage = 0.0
        if damage > MAX_DMG:
            damage = MAX_DMG
        self.__damage = damage
        self.__broken = (self.__damage >= MAX_DMG)

    def get_storage(self):
        return self.__storage

    def generate_asset(self):
        asset_classes = [HardwarePatch, SecurityChip, DataSpike, RemovableDrive, CryptoToken]
        chosen_asset = random.choice(asset_classes)

        new_asset = chosen_asset()

        if self.add_to_storage(new_asset):
            print(f"Added {type(new_asset).__name__} to storage!")
            return new_asset
        else:
            print(f"Failed to add {type(new_asset).__name__} to storage! Storage full!")
            return None

    def repair(self):
        if self.dmg <= 0:
            print("Rig has no damage to repair!")
            return False
        self.dmg = 0
        self.__broken = False
        print("Rig repaired!")
        return True

    def upgrade(self):
        self.__upgrade += 1
        print(f"Rig upgraded! New capacity: {self.capacity}")
        return True

    def take_hit(self, hits=1):

        # Calculate per-hit damage floored at 0.25
        per_hit = max(1.0 - 0.25 * self.__upgrade, 0.25)

        # total incoming before clamping
        incoming = per_hit * hits
        old_total = self.dmg
        self.dmg = old_total + incoming
        effective = self.dmg - old_total
        print(f"Rig took {effective:.2f} damage!"
              f"({hits} hits at {per_hit:.2f}/hit per hit, upgrade={self.__upgrade}).\n"
              f"Total damage is now: {self.dmg:.2f}.")
        return effective

    dmg = property(get_damage, set_damage)
    capacity = property(get_capacity)
    storage = property(get_storage)