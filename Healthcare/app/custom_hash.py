class CustomHasher:
    def __init__(self, salt_length=16):
        self.salt_length = salt_length

    def generate_salt(self):
        """Generate a random salt"""
        import random
        import string
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(self.salt_length))

    def custom_hash(self, password, salt=None):
        """Custom hashing algorithm implementation"""
        if salt is None:
            salt = self.generate_salt()
        
        # Convert password and salt to bytes
        password_bytes = str(password).encode()
        salt_bytes = str(salt).encode()
        
        # Custom hashing logic
        hash_value = 0
        for i, byte in enumerate(password_bytes + salt_bytes):
            hash_value = ((hash_value << 5) - hash_value) + byte
            hash_value = hash_value & 0xFFFFFFFF  # Keep 32 bits
        
        # Convert to hexadecimal and combine with salt
        final_hash = f"{salt}${hash_value:08x}"
        return final_hash

    def verify(self, password, stored_hash):
        """Verify a password against a stored hash"""
        salt = stored_hash.split('$')[0]
        new_hash = self.custom_hash(password, salt)
        return new_hash == stored_hash 