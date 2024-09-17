import math

import numpy as np


class HillCipher:
    def __init__(self, key: str):
        self._key_size: int = int(math.sqrt(len(key)))
        if self._key_size * self._key_size != len(key):
            raise ValueError("Key must give quare matrix")
        self._key_matrix: list[int] = [ord(char) - ord('a') for char in key]
        self._key: np.ndarray = np.array(self._key_matrix).reshape(self._key_size, self._key_size)
        self._inv_key: np.ndarray = self._validate_key()

    @property
    def key(self) -> np.ndarray:
        return self._key

    @key.setter
    def key(self, value: np.ndarray) -> None:
        self._key_size: int = int(math.sqrt(len(key)))
        if self._key_size * self._key_size != len(key):
            raise ValueError("Key must give quare matrix")
        self._key_matrix: list[int] = [ord(char) - ord('a') for char in key]
        self._key: np.ndarray = np.array(self._key_matrix).reshape(self._key_size, self._key_size)
        self._inv_key: np.ndarray = self._validate_key()

    @property
    def inv_key(self) -> np.ndarray:
        return self._inv_key

    @staticmethod
    def _modular_inverse(matrix: np.ndarray, modulus: int) -> np.ndarray:
        det = int(round(np.linalg.det(matrix)))
        det_inv = pow(det % modulus, -1, modulus)
        adjugate = det * np.linalg.inv(matrix)
        return np.round(adjugate * det_inv % modulus).astype(int)

    @staticmethod
    def _text_to_vector(text: str) -> np.ndarray:
        return np.array([ord(char) - ord('a') for char in text])

    @staticmethod
    def _vector_to_text(vector: np.ndarray) -> str:
        return ''.join([chr((int(round(x)) % 26) + ord('a')) for x in vector])

    def _validate_key(self) -> np.ndarray:
        det = int(round(np.linalg.det(self._key))) % 26
        if math.gcd(det, 26) != 1:
            raise ValueError("The key matrix is not invertible modulo 26")
        return self._modular_inverse(self._key, 26)

    def _prepare_text(self, text: str) -> str:
        text = ''.join(filter(lambda x: str.isalnum(x), text.lower()))
        padding = 'x' * ((self._key_size - len(text) % self._key_size) % self._key_size)
        return text + padding

    def encrypt(self, plaintext: str) -> str:
        plaintext = self._prepare_text(plaintext)
        vector = self._text_to_vector(plaintext)
        encrypted = np.dot(self._key, vector.reshape((-1, self._key_size)).T) % 26
        return self._vector_to_text(encrypted.T.flatten())

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = self._prepare_text(ciphertext)
        vector = self._text_to_vector(ciphertext)
        decrypted = np.dot(self._inv_key, vector.reshape((-1, self._key_size)).T) % 26
        return self._vector_to_text(decrypted.T.flatten())


# Example usage:
if __name__ == "__main__":
    key = 'GYBNQKURP'
    cipher = HillCipher(key)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
