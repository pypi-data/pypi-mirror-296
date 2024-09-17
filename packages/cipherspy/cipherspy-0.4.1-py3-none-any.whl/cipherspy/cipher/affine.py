import numpy as np

from cipherspy.exceptions import NegativeNumberException


class AffineCipher:
    def __init__(self, shift: int, multiplier: int):
        self._validate_params(shift, multiplier)
        self._shift: int = shift % 26
        self._multiplier: int = multiplier
        self._inv_multiplier: int = self._modular_inverse(multiplier, 26)

    @property
    def shift(self) -> int:
        return self._shift

    @shift.setter
    def shift(self, shift: int) -> None:
        self._validate_params(shift, self._multiplier)
        self._shift = shift % 26

    @property
    def multiplier(self) -> int:
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier: int) -> None:
        self._validate_params(self._shift, multiplier)
        self._multiplier = multiplier
        self._inv_multiplier = self._modular_inverse(multiplier, 26)

    @staticmethod
    def _validate_params(shift: int, multiplier: int) -> None:
        if shift <= 0:
            raise NegativeNumberException(shift)
        if multiplier <= 0:
            raise NegativeNumberException(multiplier)
        if np.gcd(multiplier, 26) != 1:
            raise ValueError("Multiplier must be coprime with 26")

    @staticmethod
    def _modular_inverse(a: int, m: int) -> int:
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")

    @staticmethod
    def _prepare_text(text: str) -> np.ndarray:
        return np.array([ord(char) - ord('a') for char in text.lower() if char.isalnum()])

    def _process_text(self, text: np.ndarray, encrypt: bool) -> str:
        if encrypt:
            processed = (self._multiplier * text + self._shift) % 26
        else:
            processed = (self._inv_multiplier * (text - self._shift)) % 26
        return ''.join([chr(char + ord('a')) for char in processed])

    def encrypt(self, plaintext: str) -> str:
        return self._process_text(self._prepare_text(plaintext), True)

    def decrypt(self, ciphertext: str) -> str:
        return self._process_text(self._prepare_text(ciphertext), False)


# Example usage:
if __name__ == "__main__":
    shift = 3
    multiplier = 3
    cipher = AffineCipher(shift, multiplier)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
