import uuid


def build_test_email():
    return f"user_{uuid.uuid4().hex}@test.com"


def build_test_password():
    return "Str0ngP@assw0rd!"
