from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM


def hash_password(password: str):
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str):
    return checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_id_from_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if not isinstance(payload, dict) or (payload_id := payload.get("id")) is None:
            raise ValueError("Invalid token")

        return payload_id
    except JWTError:
        raise ValueError("Invalid or expired token")