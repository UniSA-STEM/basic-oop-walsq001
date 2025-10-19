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

MAX_DMG = 2

class Rig:
    def __init__(self):
        self.__name = "Rig"
        self.__damage = 0
        self.__broken = False
        data_spike = DataSpike()
        data_spike.quantity = 2
        self.__storage: list[Asset] = [data_spike]
        self.__upgrade = 0
        self.__base_capacity = 3

    def __str__(self):
        storage_str = "\n".join(f"{str(item)}" for item in self.__storage) or "Empty"
        return (f"Rig Name: {self.__name}\n"
                f"Damage: {self.__damage}\n"
                f"Broken: {self.__broken}\n"
                f"Storage: {storage_str}\n"
                f"Upgrade: {self.__upgrade}\n")

    def broken(self):
        if self.__damage >= MAX_DMG:
            self.__broken = True
        return self.__broken

    def get_capacity(self):
        return self.__base_capacity + self.__upgrade

    def add_to_storage(self, asset: Asset):
        current_total = sum(a.quantity for a in self.__storage)
        if current_total + asset.quantity > self.capacity:
            print("Storage is full, cannot add asset!")
            return False
        for stored in self.__storage:
            if isinstance(stored, type(asset)):
                stored.quantity += asset.quantity
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
            return self.__damage, self.broken()

    def set_damage(self, damage):
        self.__damage = damage

    def get_storage(self):
        return self.__storage

    def generate_asset(self):
        asset_classes = [HardwarePatch, SecurityChip, DataSpike, RemovableDrive, CryptoToken]
        chosen_asset = random.choice(asset_classes)

        new_asset = chosen_asset()

        if self.add_to_storage(new_asset):
            print(f"Added {new_asset} to storage!")
            return new_asset
        else:
            print(f"Failed to add {new_asset} to storage! Storage full!")
            return None

    dmg = property(get_damage, set_damage)
    capacity = property(get_capacity)
    storage = property(get_storage)