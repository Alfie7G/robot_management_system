from app.auth.security import hash_password, verify_password


def test_hash_password_does_not_store_plaintext():
    password = "Password123"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_password_accepts_correct_password():
    password = "Password123"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_wrong_password():
    password = "Password123"

    hashed_password = hash_password(password)

    assert verify_password("WrongPassword", hashed_password) is False