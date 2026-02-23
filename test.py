import time
import threading

import base64
import hmac
import hashlib
import secrets
import time


class Snowflake:
    def __init__(self, worker_id=1, process_id=1):
        self.worker_id = worker_id
        self.process_id = process_id
        self.increment = 0
        self.lock = threading.Lock()
        self.epoch = 1767225600000

    def generate(self):
        with self.lock:
            timestamp = int(time.time() * 1000) - self.epoch
            self.increment = (self.increment + 1) & 4095
            return (
                (timestamp << 22) |
                (self.worker_id << 17) |
                (self.process_id << 12) |
                self.increment
            )

user_id = Snowflake().generate()

SECRET_KEY = b"super_secret_key_here"

def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def generate_token(user_id: int):
    user_part = b64(str(user_id).encode())
    timestamp = str(int(time.time()))
    time_part = b64(timestamp.encode())

    payload = f"{user_part}.{time_part}".encode()

    signature = hmac.new(
        SECRET_KEY,
        payload,
        hashlib.sha256
    ).digest()

    sig_part = b64(signature)

    token = f"{user_part}.{time_part}.{sig_part}"
    return token

def verify_token(token: str):
    try:
        user_part, time_part, sig_part = token.split(".")
        payload = f"{user_part}.{time_part}".encode()

        expected_sig = hmac.new(
            SECRET_KEY,
            payload,
            hashlib.sha256
        ).digest()

        expected_sig_b64 = b64(expected_sig)

        if not hmac.compare_digest(expected_sig_b64, sig_part):
            return None

        user_id = int(base64.urlsafe_b64decode(user_part + "==").decode())
        return user_id
    except:`
        return None


`