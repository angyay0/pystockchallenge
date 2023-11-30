import bcrypt


def hash_salt(text):
    ec = text.encode("UTF-8")
    return bcrypt.hashpw(ec, bcrypt.gensalt(10)).decode(encoding="UTF-8")


def hash_match(text, hash):
    ec = text.encode("UTF-8")
    hash = hash.encode("UTF-8")
    return bcrypt.checkpw(ec, hash)
