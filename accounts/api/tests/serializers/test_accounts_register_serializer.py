from accounts.api.serializers.account_register_serializer import (
    AccountRegisterSerializer,
)


def test_accounts_register_serializer_valid_data():
    data = {"email": "user1@example.com", "password": "password123#_"}
    serializer = AccountRegisterSerializer(data=data)
    assert serializer.is_valid() is True


def test_accounts_register_serializer_invalid_email():
    """
    GIVEN a invalid email data
    WHEN serializer is_valid() is called
    THEN is_valid is False returned
    """
    # GIVEN
    data = {"email": "user1@example", "password": "password123#_"}

    # WHEN/ THEN
    serializer = AccountRegisterSerializer(data=data)
    assert serializer.is_valid() is False


def test_accounts_register_serializer_missing_email():
    """
    GIVEN a missing email value
    WHEN serializer is_valid() is called
    THEN is valid is False returned
    """
    data = {"email": "", "password": "password123#_"}
    serializer = AccountRegisterSerializer(data=data)
    assert serializer.is_valid() is False


def test_accounts_register_serializer_missing_password():
    """
    GIVEN a missing password value
    WHEN serializer is_valid() is called
    THEN is valis is False returned
    """
    data = {"email": "user1@example.com", "password": ""}
    serializer = AccountRegisterSerializer(data=data)
    assert serializer.is_valid() is False
