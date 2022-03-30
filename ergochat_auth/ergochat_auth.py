#!/usr/bin/env python3

import os, sys, json
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import check_password_hash

load_dotenv()


def main():
    raw_input = sys.stdin.readline()
    ergo_user = json.loads(raw_input)
    account_name = ergo_user.get("accountName")
    passphrase = ergo_user.get("passphrase")

    if account_name is None or passphrase is None:
        print(json.dumps({"success": False, "error": "User or password missing."}))
        sys.exit(1)

    client = MongoClient(os.getenv("MONGO_URI"))
    users = client.suprachat.users

    api_user = users.find_one({"nick": account_name})

    if api_user is None:
        print(
            json.dumps({"success": False, "error": f"User {account_name} not found."})
        )
        sys.exit(1)

    if check_password_hash(api_user["password"], passphrase):
        print(
            json.dumps({"success": True, "message": "User found and passwords match."})
        )
    else:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": f"User {account_name} found but passwords don't match.",
                }
            )
        )


if __name__ == "__main__":
    main()
