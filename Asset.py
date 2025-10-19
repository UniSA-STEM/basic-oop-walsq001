"""
File: Asset.py
Description: This module outlines the asset class and their associated functionality.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
class Asset:
    def __init__(self, name, description, quantity):
        self.__name = name
        self.__description = description
        self.__unencrypted_quantity = quantity
        self.__encrypted_quantity = 0
        self.__encrypted = False

    def __str__(self):
        parts = []
        if self.__encrypted_quantity > 0:
            parts.append(f"{self.__encrypted_quantity} encrypted")
        if self.__unencrypted_quantity > 0:
            parts.append(f"{self.__unencrypted_quantity} unencrypted")
        return (f"{self.__name} - {self.__description} ({', '.join(parts)})")

    def get_encrypt(self):
        return self.__encrypted_quantity > 0

    def toggle_encrypt(self, token=None):
        if token is None or not isinstance(token, SecurityChip):
            print("Encryption requires a SecurityChip!")
            return False
        if token.quantity <= 0:
            print("No security chips available!")
            return False
        token.consume(1)
        if self.__unencrypted_quantity > 0:
            self.__unencrypted_quantity -= 1
            self.__encrypted_quantity += 1
            print(f"{self.__name}: 1 unit encrypted")
        elif self.__encrypted_quantity > 0:
            self.__encrypted_quantity -= 1
            self.__unencrypted_quantity += 1
            print(f"{self.__name}: 1 unit decrypted")
        else:
            print(f"No {self.__name} units available to toggle")
            return False
        self.__encrypted = self.__encrypted_quantity > 0
        return True


    def get_quantity(self):
        return self.__unencrypted_quantity + self.__encrypted_quantity

    def set_quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity must be an integer")
        self.__unencrypted_quantity = max(0, value)
        self.__encrypted_quantity = 0

    def merge_from(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Can only merge assets of the same type")
        self.__unencrypted_quantity += other.__unencrypted_quantity
        self.__encrypted_quantity += other.__encrypted_quantity
        self.__encrypted = self.__encrypted_quantity > 0

    def consume(self, amount=1):
        if self.__unencrypted_quantity == 0:
            print(f"No unencrypted {self.__name} units available to consume!")
            return self.quantity

        if amount < 0:
            raise ValueError("Quantity cannot be negative")

        if self.__unencrypted_quantity >= amount:
            self.__unencrypted_quantity -= amount
        else:
            self.__unencrypted_quantity = 0

        return self.quantity

    quantity = property(get_quantity, set_quantity)
    encrypted = property(get_encrypt)

class CryptoToken(Asset):
    def __init__(self):
        super().__init__("Crypto Token", "Used to acquire or repair rigs.", 1)

class DataSpike(Asset):
    def __init__(self):
        super().__init__("Data Spike", "Used in battles", 1)

class RemovableDrive(Asset):
    def __init__(self):
        super().__init__("Removable Drive", "Found in rigs" +
                         " and used for extraction", 1)

class SecurityChip(Asset):
    def __init__(self):
        super().__init__("Security Chip", "Used to encrypt" +
                         " or decrypt assets", 1)

class HardwarePatch(Asset):
    def __init__(self):
        super().__init__("Hardware Patch", "Used to upgrade rigs", 1)
