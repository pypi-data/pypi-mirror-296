import logging

import ecies
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

try:
    import pyximport

    pyximport.install()
    from decentnet.modules.convert.byte_to_base64_fast import *  # noqa
except ImportError as ex:
    logger.debug(f"Operating in slow mode because of {ex}")
    logger.warning("Base64 convert module is operating in slow mode")
    from decentnet.modules.convert.byte_to_base64_slow import *


class AsymCrypt:

    @staticmethod
    def generate_key_pair_encryption() -> [bytes, bytes]:
        """Generate a key pair for ECIES."""
        private_key = ecies.utils.generate_key()
        sk_bytes = private_key.secret  # bytes
        pk_bytes = private_key.public_key.format(True)  # bytes
        return sk_bytes, pk_bytes

    @staticmethod
    def generate_key_pair_signing() -> [SigningKey, VerifyKey]:
        """Generate a key pair for Ed25519 (replaces ECDSA)."""
        # Generate a private key (SigningKey)
        private_key = SigningKey.generate()

        # Derive the public key from the private key
        public_key = private_key.verify_key

        return private_key, public_key

    @staticmethod
    def check_encryption_key(public_key: bytes):
        try:
            ecies.encrypt(public_key, b"test")
            return True
        except TypeError:
            return False

    @staticmethod
    def encrypt_message(public_key: bytes, data: bytes) -> bytes:
        """Encrypts data using ECIES."""
        encrypted_data = ecies.encrypt(public_key, data)
        return encrypted_data

    @staticmethod
    def decrypt_message(private_key: bytes, encrypted_data: bytes) -> bytes:
        """Decrypts data using ECIES."""
        decrypted_data = ecies.decrypt(private_key, encrypted_data)
        return decrypted_data

    @staticmethod
    def sign_message(private_key: SigningKey, data: bytes) -> bytes:
        """Signs data using Ed25519 (replaces ECDSA)."""
        signature = private_key.sign(data).signature
        return signature

    @staticmethod
    def verify_signature(*, public_key: VerifyKey, signature: bytes, data: bytes) -> bool:
        """Verifies the signature of data using Ed25519."""
        try:
            public_key.verify(data, signature)
            return True
        except BadSignatureError:
            return False

    @staticmethod
    def key_pair_from_private_key_base64(private_key: str, can_encrypt: bool) -> tuple[
                                                                                     SigningKey, VerifyKey] | \
                                                                                 tuple[bytes, bytes]:
        """
        Returns an Object key pair from base64 str
        :param private_key:
        :param can_encrypt:
        :return: Private Key Object, Public Key object
        """
        if not can_encrypt:
            private_key = SigningKey(base64_to_original(private_key))
            public_key = private_key.verify_key
            return private_key, public_key
        else:
            pk_bytes = base64_to_original(private_key)
            private_key = ecies.PrivateKey(pk_bytes)
            public_key = private_key.public_key.format(True)
            return private_key.secret, public_key

    @staticmethod
    def public_key_from_base64(public_key: str, can_encrypt: bool) -> VerifyKey | bytes:
        """
        Returns Object key from base64 str
        :param public_key:
        :param can_encrypt:
        :return: Private Key Object, Public Key object
        """
        if not can_encrypt:
            return VerifyKey(base64_to_original(public_key))
        else:
            pk_bytes = base64_to_original(public_key)
            return ecies.PublicKey(pk_bytes).format(True)

    @staticmethod
    def encryption_key_to_base64(key: bytes) -> str:
        """
        Converts bytes of public or private key to base64
        :param key:
        :return:
        """
        return bytes_to_base64(key)

    @staticmethod
    def verifying_key_to_string(key: VerifyKey) -> str:
        """
        Converts a verification key into string base64
        :param key:
        :return:
        """
        return bytes_to_base64(key.encode())

    @staticmethod
    def verifying_key_from_string(key: str) -> VerifyKey:
        return VerifyKey(base64_to_original(key))
