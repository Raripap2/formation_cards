import hashlib


def sha256_hash(text):
    # Создаем объект хеша SHA-256
    sha256_hash = hashlib.sha256()

    # Преобразуем текст в байты (хеш работает с байтами, а не со строками)
    sha256_hash.update(text.encode('utf-8'))

    # Получаем шестнадцатеричное представление хеша
    hex_digest = sha256_hash.hexdigest()

    return hex_digest

if __name__ == '__main__':
    print(sha256_hash(''))