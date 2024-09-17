import numpy as np


class PlayfairCipher:

    def __init__(self, key: str):
        self._key: str = self._prepare_key(key)
        self._matrix: np.ndarray = self._generate_matrix()

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str) -> None:
        self._key = self._prepare_key(key)
        self._matrix = self._generate_matrix()

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix

    @staticmethod
    def _prepare_key(key: str) -> str:
        unique_chars = []
        for char in ''.join(filter(lambda x: str.isalpha(x), key.lower().replace('j', 'i'))):
            if char not in unique_chars:
                unique_chars.append(char)
        for char in "abcdefghiklmnopqrstuvwxyz":
            if char not in unique_chars:
                unique_chars.append(char)
        return ''.join(unique_chars)

    @staticmethod
    def _prepare_text(text: str) -> str:
        text = ''.join(filter(lambda x: str.isalnum(x), text.lower().replace('j', 'i')))
        prepared_text = []
        i = 0
        while i < len(text):
            if i == len(text) - 1 or text[i] == text[i+1]:
                prepared_text.extend([text[i], 'x'])
                i += 1
            else:
                prepared_text.extend([text[i], text[i+1]])
                i += 2
        return ''.join(prepared_text)

    def _generate_matrix(self) -> np.ndarray:
        return np.array([ord(char) - ord('a') for char in self._key]).reshape(5, 5)

    def _get_coordinates(self, char: int) -> (np.ndarray,):
        coordinates = np.where(self._matrix == char)
        if coordinates[0].size == 0 or coordinates[1].size == 0:
            raise ValueError(f"Character {char} not found in matrix")
        return coordinates

    def _process_pair(self, pair: str, encrypt: bool) -> str:
        row1, col1 = self._get_coordinates(ord(pair[0]) - ord('a') if ord(pair[0]) >= 97 else ord(pair[0]) % 26)
        row2, col2 = self._get_coordinates(ord(pair[1]) - ord('a') if ord(pair[1]) >= 97 else ord(pair[1]) % 26)
        if row1 == row2:
            return (chr(int(self._matrix[row1, (col1 + (1 if encrypt else -1)) % 5][0] + ord('a'))) +
                    chr(int(self._matrix[row2, (col2 + (1 if encrypt else -1)) % 5][0] + ord('a'))))
        elif col1 == col2:
            return (chr(int(self._matrix[(row1 + (1 if encrypt else -1)) % 5, col1][0] + ord('a'))) +
                    chr(int(self._matrix[(row2 + (1 if encrypt else -1)) % 5, col2][0] + ord('a'))))
        else:
            return chr(int(self._matrix[row1, col2][0] + ord('a'))) + chr(int(self._matrix[row2, col1][0] + ord('a')))

    def encrypt(self, plaintext: str) -> str:
        plaintext = self._prepare_text(plaintext)
        return ''.join(self._process_pair(plaintext[i:i + 2], True) for i in range(0, len(plaintext), 2))

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = self._prepare_text(ciphertext)
        return ''.join(self._process_pair(ciphertext[i:i+2], False) for i in range(0, len(ciphertext), 2))


# Example usage:
if __name__ == "__main__":
    key = "secret"
    cipher = PlayfairCipher(key)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
