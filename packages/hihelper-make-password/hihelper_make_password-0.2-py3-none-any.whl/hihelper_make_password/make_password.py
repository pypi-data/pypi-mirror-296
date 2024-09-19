import random
import string

def generate_password(length: int) -> str:
    if length < 1:
        raise ValueError("패스워드 길이는 1 이상이어야 합니다.")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

if __name__ == "__main__":
    pw = generate_password(10)
    print(pw)
