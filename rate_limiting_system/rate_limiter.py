import redis
import time
from flask import request, jsonify
from functools import wraps

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


class _RateLimiter:
    def __init__(self, user_token, max_tokens, seconds_per_token):
        self.user_token = user_token
        self.max_tokens = max_tokens
        self.seconds_per_token = seconds_per_token
        self.bucket_key = f"bucket:{user_token}"
        self.last_refill_time_key = f"bucket_last_refill:{user_token}"

    def is_allowed(self) -> bool:
        last_refill_time = redis_client.get(self.last_refill_time_key)
        if last_refill_time is None:
            redis_client.set(self.bucket_key, self.max_tokens-1)
            redis_client.set(self.last_refill_time_key, time.time())
            return True
        elapsed_time = time.time() - float(last_refill_time)
        if elapsed_time < self.seconds_per_token:
            tokens = int(redis_client.get(self.bucket_key))
            if tokens < 1:
                return False
            redis_client.set(self.bucket_key, tokens-1)
            redis_client.set(self.last_refill_time_key, time.time())
            return True        
        tokens_to_add = min(int(elapsed_time / self.seconds_per_token), self.max_tokens)
        redis_client.set(self.bucket_key, tokens_to_add-1)
        redis_client.set(self.last_refill_time_key, time.time())
        return True

def rate_limiter(max_tokens: int, seconds_per_token: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_token = request.headers.get("User-Token")
            if user_token is None:
                return jsonify({"error": "Missing user token"}), 401
            limiter = _RateLimiter(user_token=user_token, max_tokens=max_tokens, seconds_per_token=seconds_per_token)
            if not limiter.is_allowed():
                return jsonify({"error": "Too many requests. Rate limit exceeded."}), 429
            return f(*args, **kwargs)
        return decorated_function
    return decorator
