class Validators:
    @staticmethod
    def validate_password(password: str, confirm_password: str):
        if confirm_password != password:
            return False
        return True

    @staticmethod
    def validate_password_length(password: str):
        if len(password) >= 10:
            return True
        return False
