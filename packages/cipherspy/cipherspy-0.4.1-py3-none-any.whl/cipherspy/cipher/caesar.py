import numpy as np

from cipherspy.exceptions import NegativeNumberException


class CaesarCipher:
    def __init__(self, shift: int):
        self._validate_shift()
        self._shift: int = shift % 26

    @property
    def shift(self) -> int:
        return self._shift

    @shift.setter
    def shift(self, shift: int) -> None:
        self._validate_shift()
        self._shift = shift % 26

    @staticmethod
    def _validate_shift() -> None:
        if shift <= 0:
            raise NegativeNumberException(shift)

    @staticmethod
    def _prepare_text(text: str) -> np.ndarray:
        return np.array([ord(char) - ord('a') for char in text.lower() if char.isalnum()])

    def _process_text(self, text: np.ndarray, encrypt: bool) -> str:
        shift = self._shift if encrypt else -self.shift
        processed_text = (text + shift) % 26
        return ''.join([chr(char + ord('a')) for char in processed_text])

    def encrypt(self, plaintext: str) -> str:
        return self._process_text(self._prepare_text(plaintext), True)

    def decrypt(self, ciphertext: str) -> str:
        return self._process_text(self._prepare_text(ciphertext), False)


# Example usage:
if __name__ == "__main__":
    shift = 3
    cipher = CaesarCipher(shift)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
