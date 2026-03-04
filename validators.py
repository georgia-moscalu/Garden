def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return False, "Email este obligatoriu!"
    if "@" not in email:
        return False, "Email invalid! (lipseste @)"
    if "." not in email.split("@")[1]:
        return False, "Email invalid! (lipseste domeniu)"
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    if not password:
        return False, "Parola este obligatorie!"
    if len(password) < 4:
        return False, "Parola prea scurta (minim 4 caractere)"
    return True, ""