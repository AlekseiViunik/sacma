import json
import random


class Encoder:
    """
    Класс для шифрования и дешифрования текстовых файлов с использованием
    уникальных кодов.
    """
    def __init__(self):
        pass

    def encrypt_file(self, file_path):
        # Загружаем словарь шифрования
        with open("encryption.json", "r", encoding="utf-8") as f:
            enc_dict = json.load(f)["encryption"]

        encrypted_lines = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.ljust(100)[:100]
                encrypted_line = [
                    random.choice(
                        enc_dict.get(ch, enc_dict[" "])
                    ) for ch in line
                ]
                encrypted_lines.append("".join(encrypted_line))

        # Запись в JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(encrypted_lines, f, indent=4, ensure_ascii=False)

    def decrypt_file(
        self,
        encrypted_file_path,
        output_path="decrypted_file.json"
    ):
        # Загружаем словарь дешифровки
        with open("encryption.json", "r", encoding="utf-8") as f:
            decryption = json.load(f)["decription"]

        # Загружаем зашифрованные строки
        with open(encrypted_file_path, "r", encoding="utf-8") as f:
            encrypted_lines = json.load(f)

        decrypted_lines = []

        for line in encrypted_lines:
            chars = [line[i:i+5] for i in range(0, len(line), 5)]
            decoded = ''.join(
                decryption.get(code, '?') for code in chars
            ).rstrip()
            decrypted_lines.append(decoded)

        # Сохраняем результат
        with open(encrypted_file_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(decrypted_lines))

    def decrypt_data(
        self,
        data: list[str],
    ) -> dict:
        # Загружаем словарь дешифровки
        with open("configs/encryption.json", "r", encoding="utf-8") as f:
            decryption = json.load(f)["decription"]

        decrypted_text = []

        for line in data:
            chunks = [line[i:i+5] for i in range(0, len(line), 5)]
            decoded = ''.join(
                decryption.get(code, '?') for code in chunks
            ).rstrip()
            decrypted_text.append(decoded)

        # Пробуем собрать обратно словарь
        try:
            return json.loads(''.join(decrypted_text))
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON"}

    def encrypt_data(self, data_dict):
        with open("configs/encryption.json", "r", encoding="utf-8") as f:
            encryption = json.load(f)["encryption"]

        json_lines = json.dumps(
            data_dict, indent=4, ensure_ascii=False
        ).splitlines()

        encrypted_lines = []

        for line in json_lines:
            line = line.ljust(100)[:100]
            encrypted_line = [
                random.choice(
                    encryption.get(ch, encryption[" "])
                ) for ch in line
            ]
            encrypted_lines.append("".join(encrypted_line))

        return encrypted_lines


if __name__ == "__main__":
    pass
