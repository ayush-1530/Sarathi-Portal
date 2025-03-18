import redis 
import random


def generate_otp():
        return str(random.randint(100000, 999999))


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class redis_ops():
    def __init__(self):
        self.redis_client = redis_client

    def redis_set(self, key, expiry, val):
        return self.redis_client.setex(key, expiry, val)

    def redis_get(self, key): 
        return self.redis_client.get(key)           

    def redis_del(self, key):   
        return self.redis_client.delete(key)                 



# if __name__ == "__main__":
# otp = redis_ops()
# user_id = "test_user_123"


# otp = generate_otp()
# op.redis_set(user_id, 2, otp)
# print(f"Generated OTP for {user_id}: {otp}")
# # entered_otp = input("Enter otp: ")
# fetched_otp = op.redis_get(user_id)
# print(f"Fetched OTP for {user_id}: {fetched_otp}")
# otp_verification_status = bool(entered_otp == fetched_otp)
# print(f"OTP Verification Status (correct): {otp_verification_status}")




