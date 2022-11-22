import os
import jwt
import logging
from datetime import datetime

from web3 import Web3
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from eth_account.messages import encode_defunct


class DbWrapper:
    def __init__(self, db_name: str):
        try:
            logging_file_name = str(datetime.timestamp(datetime.now())).split(".")[0]
            logging.basicConfig(
                filename=f"./app/logs/{logging_file_name}.log",
                format="%(asctime)s %(message)s",
                filemode="w",
            )
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)

            load_dotenv(find_dotenv())
            self.logger.info(".env file was loaded.")

            self.client = MongoClient(os.environ.get("MONGODB_PWD"))
            if self.client:
                self.logger.info("Connected to MongoDB Successfully.")
                self.db_name = db_name  # If connected to MongoDB, set db_name
            else:
                self.logger.error("Failed to connect to MongoDB.")

            self.web3 = Web3()
            self.admins = list(os.environ.get("ADMINS").split(","))
            self.logger.info(f"Initialized Admins: {self.admins}")

            self.logger.info("DbWrapper Initialized Successfully.")

        except Exception as e:
            self.logger.error(f"Failed to initialize DbWrapper: {e}")
            raise e

    def get_database_names(self) -> list:
        """
        :return: a list of all database names.
        """

        try:
            self.logger.info("Getting database names:")
            return self.client.list_database_names()

        except Exception as e:
            self.logger.error(f"Failed to get database names: {e}")
            return None

    def get_database(self, db_name: str) -> MongoClient:
        """
        :param db_name: name of database to get
        :return: database object
        """
        try:
            self.logger.info(f"Getting database: {db_name}")
            return self.client[db_name]

        except Exception as e:
            self.logger.error(f"Failed to get database: {e}")
            return None

    def get_collection_names(self) -> list:
        """
        :return: a list of all collection names
        """
        try:
            self.logger.info(f"Getting collection names from database: {self.db_name}")
            return self.get_database(self.db_name).list_collection_names()

        except Exception as e:
            self.logger.error(f"Failed to get collection names: {e}")
            return None

    def get_collection(self, collection_name: str) -> MongoClient:
        """
        :param collection_name: name of collection to get
        :return: collection object
        """
        try:
            self.logger.info(f"Getting collection: {collection_name}")
            return self.get_database(self.db_name)[collection_name]

        except Exception as e:
            self.logger.error(f"Failed to get collection: {e}")
            return None

    # User related functions
    def get_users(self) -> list:
        """
        :return: a list of all users
        """
        try:
            self.logger.info("Getting all users")
            return self.get_collection("users").find()

        except Exception as e:
            self.logger.error(f"Failed to get users: {e}")
            return None

    def get_user_by_public_address(self, user_public_address: str) -> dict:
        """
        :param user_public_address: public address of user
        :return: user info
        """
        try:
            self.logger.info(f"Getting user by public address: {user_public_address}")
            return self.get_collection("users").find_one(
                {"publicAddress": user_public_address}
            )

        except Exception as e:
            self.logger.error(f"Failed to get user by public address: {e}")
            return None

    def user_exists(self, user_public_address: str) -> bool:
        """
        :param user_public_address: public address of user
        :return: True if user exists, False otherwise
        """
        try:
            self.logger.info(f"Checking if user exists: {user_public_address}")
            user = self.get_collection("users").find_one(
                {"publicAddress": user_public_address}
            )
            return user is not None

        except Exception as e:
            self.logger.error(f"Failed to check if user exists")
            return False

    def set_user(self, user_info: dict) -> str:
        """
        :param user_info: the user info to set
        :return: the user id
        """
        """
        user_info = {
            "publicAddress": "0x1234567890",
            "nonce": 0,
            "name": "John Doe", (optional)
            "email": "random@gmail.com", (optional)
            "instagram": "random", (optional)
            "twitter": "random", (optional)
            "discordId": "723465298346523654", (optional)
            "opensea": "random", (optional)
            "bio": "I am the best", (optional)
            "profileImage": "https://random.com/random.png", (optional)
            "points": 0 (optional)
        }
        """
        try:
            if not self.user_exists(user_info["publicAddress"]):
                self.logger.info(f"Setting user: {user_info['publicAddress']}")
                return self.get_collection("users").insert_one(user_info).inserted_id
            else:
                self.logger.critical("User already exists.")
                return None

        except Exception as e:
            self.logger.error(f"Failed to set user: {e}")
            return None

    def update_user(self, user_info: dict) -> bool:
        """
        :param user_info: the user info to set
        :return: boolean indicating success status
        """
        """
        user_info = {
            "publicAddress": "0x1234567890",
            "nonce": 0,
            "name": "John Doe", (optional)
            "email": "random@gmail.com", (optional)
            "instagram": "random", (optional)
            "twitter": "random", (optional)
            "discordId": "723465298346523654", (optional)
            "opensea": "random", (optional)
            "bio": "I am the best", (optional)
            "profileImage": "https://random.com/random.png", (optional)
            "points": 0 (optional)
        }
        """
        try:
            if not self.user_exists(user_info["publicAddress"]):
                self.logger.critical("User does not exist.")
                return False
            else:
                self.logger.info(f"Updating user: {user_info['publicAddress']}")
                self.get_collection("users").update_one(
                    {"publicAddress": user_info["publicAddress"]}, {"$set": user_info}
                )
                return True

        except Exception as e:
            self.logger.error(f"Failed to update user: {e}")
            return False

    def update_user_nonce(self, user_public_address: str, nonce: int) -> bool:
        """
        :param user_public_address: public address of user
        :param nonce: nonce to set
        :return: boolean indicating success status
        """
        try:
            if not self.user_exists(user_public_address):
                self.logger.critical("User does not exist. Nonce cannot be updated.")
                return False
            else:
                self.logger.info(f"Updating user nonce: {user_public_address}")
                self.get_collection("users").update_one(
                    {"publicAddress": user_public_address}, {"$set": {"nonce": nonce}}
                )
                return True

        except Exception as e:
            self.logger.error(f"Failed to update user nonce: {e}")
            return False

    def delete_user(self, user_public_address: str) -> bool:
        """
        :param user_public_address: public address of user
        :return: boolean indicating success status
        """
        try:
            if not self.user_exists(user_public_address):
                self.logger.critical("User does not exist. Cannot be deleted.")
                return False
            else:
                self.logger.info(f"Deleting user: {user_public_address}")
                self.get_collection("users").delete_one(
                    {"publicAddress": user_public_address}
                )
                return True

        except Exception as e:
            self.logger.error(f"Failed to delete user: {e}")
            return False

    def signature(self, user_public_address: str, signature: str):
        """
        :param user_public_address: public address of user
        :param signature: signature of user
        :return: boolean indicating success status
        """
        try:  # Check if the user exists, if not, create a new user and set nonce to
            # 0 else increase the nonce by 1
            if not self.user_exists(user_public_address):
                if self.web3.isAddress(user_public_address):
                    self.logger.info(
                        "User does not exist. Creating user with signature."
                    )

                    self.logger.info(f"User Signature: {user_public_address}")

                    sign_message = f"""
                    Authenticating user {user_public_address} with nonce {0}
                    """
                    message_hex = encode_defunct(text=sign_message)

                    expected_address = self.web3.eth.account.recover_message(
                        message_hex, signature=signature
                    )

                    if expected_address == user_public_address:
                        self.logger.info(f"Signature is valid: {user_public_address}")
                        self.logger.info(f"Creating user: {user_public_address}")

                        created_user_id = self.set_user(
                            {"publicAddress": user_public_address, "nonce": 0}
                        )

                        self.update_user_nonce(user_public_address, 1)
                        token = jwt.encode(
                            {
                                "publicAddress": user_public_address,
                                "signature": signature,
                                "nonce": 0,
                                "exp": int(
                                    str(datetime.timestamp(datetime.now())).split(".")[
                                        0
                                    ]
                                )
                                + (60 * 60 * 24 * 7)  # 7 days
                                # (seconds * minutes * hours * days)
                            }
                        )

                        return {"token": token}
                    else:
                        self.logger.error(
                            f"Signature is invalid: {user_public_address}"
                        )
                        return False
                else:
                    self.logger.error("Invalid public address.")
                    return False
            else:
                if self.web3.isAddress(user_public_address):
                    self.logger.info(f"User Signature: {user_public_address}")

                    user = self.get_user_by_public_address(user_public_address)

                    sign_message = f"""
                    Authenticating user {user['publicAddress']} with nonce {user['nonce']}
                    """
                    message_hex = encode_defunct(text=sign_message)

                    expected_address = self.web3.eth.account.recover_message(
                        message_hex, signature=signature
                    )

                    if expected_address == user_public_address:
                        self.logger.info(f"Signature is valid: {user_public_address}")

                        self.update_user_nonce(user_public_address, user["nonce"] + 1)
                        token = jwt.encode(
                            {
                                "publicAddress": user_public_address,
                                "signature": signature,
                                "nonce": user["nonce"],
                                "exp": int(
                                    str(datetime.timestamp(datetime.now())).split(".")[
                                        0
                                    ]
                                )
                                + (60 * 60 * 24 * 7)  # 7 days
                                # (seconds * minutes * hours * days)
                            }
                        )

                        return {"token": token}
                    else:
                        self.logger.error(
                            f"Signature is invalid: {user_public_address}"
                        )
                        return False

                    return True
                else:
                    self.logger.error(f"Invalid public address: {user_public_address}")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to delete user: {e}")
            return False

    def verify(self, token: str) -> bool:
        """
        :param token: token of user
        :return: boolean indicating success status
        """
        try:
            self.logger.info(f"Verifying user token: {token}")

            decoded = jwt.decode(
                token, key=os.environ.get("JWT_SECRET"), algorithms=["HS256"]
            )

            if decoded["exp"] > int(
                str(datetime.timestamp(datetime.now())).split(".")[0]
            ):
                jwt_signature = decoded["signature"]

                sign_message = f"""
                Authenticating user {decoded["publicAddress"]} with nonce 
                {decoded["nonce"]}
                """
                message_hex = encode_defunct(text=sign_message)
                user_public_address = self.web3.eth.account.recover_message(
                    message_hex, signature=jwt_signature
                )

                self.logger.info(
                    f"Decoded User Signature Public Address:" f" {user_public_address}"
                )
                decoded["publicAddress"] = user_public_address

                return decoded
            else:
                return False

        except Exception as e:
            self.logger.error(f"Failed to verify user token: {e}")
            return False

    # For Admin Dashboard Functions
    def admin_signature(self, user_public_address: str, signature: str):
        """
        :param user_public_address: public address of user
        :param signature: signature of user
        :return: boolean indicating success status
        """
        try:
            if not self.user_exists(user_public_address):
                self.logger.critical("Admin does not exist. Cannot generate signature.")
                return False
            else:
                self.logger.info(f"Admin Signature: {user_public_address}")

                user = self.get_user_by_public_address(user_public_address)

                sign_message = f"""
                Authenticating Admin {user['publicAddress']} with nonce {user['nonce']}
                """
                message_hex = encode_defunct(text=sign_message)

                expected_address = self.web3.eth.account.recover_message(
                    message_hex, signature=signature
                )

                if expected_address == user_public_address:
                    self.logger.info(f"Signature is valid: {user_public_address}")
                    token = jwt.encode(
                        {
                            "publicAddress": user_public_address,
                            "nonce": user["nonce"],
                            "signature": signature,
                            "exp": int(
                                str(datetime.timestamp(datetime.now())).split(".")[0]
                            )
                            + (60 * 60 * 24 * 7)  # 7 days
                            # (seconds * minutes * hours * days)
                        }
                    )

                    return {"token": token}
                else:
                    self.logger.error(f"Signature is invalid: {user_public_address}")
                    return False

                return True

        except Exception as e:
            self.logger.error(f"Failed to sign Admin: {e}")
            return False

    def admin_verify(self, token: str) -> bool:
        """
        :param token: token of user
        :return: boolean indicating success status
        """
        try:
            self.logger.info(f"Verifying user token: {token}")

            decoded = jwt.decode(
                token, key=os.environ.get("JWT_SECRET"), algorithms=["HS256"]
            )

            if decoded["exp"] > int(
                str(datetime.timestamp(datetime.now())).split(".")[0]
            ):
                if decoded["publicAddress"] in os.environ.get("ADMINS"):
                    jwt_signature = decoded["signature"]

                    sign_message = f"""
                    Authenticating user {decoded["publicAddress"]} with nonce 
                    {decoded["nonce"]}
                    """
                    message_hex = encode_defunct(text=sign_message)
                    user_public_address = self.web3.eth.account.recover_message(
                        message_hex, signature=jwt_signature
                    )

                    self.logger.info(
                        f"Decoded User Signature Public Address:"
                        f" {user_public_address}"
                    )
                    decoded["publicAddress"] = user_public_address

                    return decoded
                else:
                    return False
            else:
                return False

        except Exception as e:
            self.logger.error(f"Failed to verify Admin token: {e}")
            return False
