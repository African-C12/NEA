from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.crypto import constant_time_compare
import random
import string

class CustomHash(BasePasswordHasher):
    """
    A custom password hasher that demonstrates a simple hashing mechanism.
    """
    algorithm = "custom_hash"

    def salt(self):
        """
        Generate a random salt.
        
        Returns:
            str: A random salt string.
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(8))

    def encode(self, password, salt):
        """
        Encode the password with a salt.
        
        Args:
            password (str): The password to hash.
            salt (str): The salt to use.
        
        Returns:
            str: Encoded password in the format 'algorithm$salt$hash'.
        """
        assert password is not None
        assert salt and '$' not in salt
        
        # Combine password and salt
        combined = password + salt
        
        # Create a simple, educational hashing mechanism
        hash_value = 0
        for char in combined:
            # Rotate and mix the hash value with each character
            hash_value = ((hash_value << 3) - hash_value + ord(char)) & 0xFFFFFFFF
        
        # Convert to hexadecimal and combine with algorithm and salt
        return f"{self.algorithm}${salt}${hash_value:08x}"

    def verify(self, password, encoded):
        """
        Verify a password against an encoded hash.
        
        Args:
            password (str): The password to verify.
            encoded (str): The encoded password to compare against.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        algorithm, salt, hash_value = encoded.split('$', 2)
        assert algorithm == self.algorithm
        
        # Recreate the hash
        new_encoded = self.encode(password, salt)
        
        return constant_time_compare(encoded, new_encoded)

    def safe_summary(self, encoded):
        """
        Provide a safe summary of the hash.
        
        Args:
            encoded (str): The encoded password.
        
        Returns:
            dict: A dictionary with masked hash information.
        """
        algorithm, salt, hash_value = encoded.split('$', 2)
        return {
            'algorithm': algorithm,
            'salt': mask_hash(salt),
            'hash': mask_hash(hash_value),
        }

    def must_update(self, encoded):
        """
        Determine if the hash must be updated.
        
        Args:
            encoded (str): The encoded password.
        
        Returns:
            bool: Always False in this implementation.
        """
        return False