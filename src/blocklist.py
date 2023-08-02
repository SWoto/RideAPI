import redis
import os

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.

if os.getenv("UNITTEST", "-1") == "1":
    redis_ip = "localhost"
else:
    redis_ip = "redis"

print("redis_ip: {}".format(redis_ip))
jwt_redis_blocklist = redis.StrictRedis(
    host=redis_ip, port=6379, db=0, decode_responses=True
)
