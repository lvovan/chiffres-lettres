import re

def areNameGroupValid(name, group):
    # Check name and group validity
    if not re.fullmatch("^[A-Za-z0-9\-]{1,32}$", name):
        return "'name' must be alphanumeric only, no spaces and up to 32 characters"
    if not re.fullmatch("^[A-Za-z0-9\-]{0,32}$", group):
        return "'group' must be empty or alphanumeric only, no spaces and up to 32 characters"
    return None
