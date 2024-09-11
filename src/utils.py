import random
import string

def get_random_gender():
    gender_identities = [
        "Trans Male", "Trans Female", "Cis Male", "Cis Female"
    ]
    return random.choice(gender_identities)

def generate_document_id(length=12, prefix="", suffix=""):
    characters = string.digits + string.ascii_uppercase
    random_part = ''.join(random.choice(characters) for _ in range(length))
    return prefix + random_part + suffix

