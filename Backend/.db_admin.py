#!/usr/bin/env python3
"""
Tooth Manager - Database & User Administration Utility
Use this script to create initial admin accounts, list users, or reset passwords.
"""

import sys
import argparse
from database.db import (
    init_db,
    create_user,
    get_all_users,
    get_user_by_username,
    update_user_permission,
    update_user_password,
    delete_user_by_username,
)
from core.security import hash_password


def interactive_add_user():
    print("\n🦷 Tooth Manager - Create New User")
    print("-----------------------------------")
    firstname = input("First Name: ").strip()
    lastname = input("Last Name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    print("\nPermission Tiers:")
    print("  1 = Practice Administrator (Full document & user access)")
    print("  2 = Practice Staff (View & download documents)")
    print("  3 = Pending Approval (No document access)")
    tier_input = input("Select Tier (1, 2, or 3) [default: 1]: ").strip() or "1"

    try:
        tier = int(tier_input)
    except ValueError:
        tier = 1

    if not all([firstname, lastname, username, password]):
        print("❌ Error: All fields are required.")
        return

    pwd_hash = hash_password(password)
    user = create_user(firstname, lastname, username, pwd_hash, tier)
    if user:
        role_name = "Admin" if tier == 1 else "Staff" if tier == 2 else "Pending"
        print(f"\n✅ User '{user['username']}' created successfully as {role_name} (Tier {tier})!")
    else:
        print(f"\n❌ Error: User '{username}' could not be created. Username might already exist.")


def list_users():
    users = get_all_users(include_passwords=False)
    print("\n🦷 Registered Users Roster:")
    print("----------------------------------------------------------------------")
    print(f"{'ID':<4} {'Username':<16} {'Name':<22} {'Tier':<8} {'Created At'}")
    print("----------------------------------------------------------------------")
    if not users:
        print("  (No users registered yet)")
    for u in users:
        tier_name = "Admin (1)" if u['permission_tier'] == 1 else "Staff (2)" if u['permission_tier'] == 2 else "Pending (3)"
        full_name = f"{u['firstname']} {u['lastname']}"
        created = u.get('created_at', 'N/A')
        print(f"{u['id']:<4} {u['username']:<16} {full_name:<22} {tier_name:<12} {created}")
    print("----------------------------------------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(description="Tooth Manager User Admin")
    parser.add_argument("--list", action="store_true", help="List all registered users")
    parser.add_argument("--add", action="store_true", help="Interactively add a new user")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--firstname", help="First name")
    parser.add_argument("--lastname", help="Last name")
    parser.add_argument("--password", help="Password")
    parser.add_argument("--tier", type=int, default=1, choices=[1, 2, 3], help="Permission tier (1=Admin, 2=Staff, 3=Pending)")

    args = parser.parse_args()

    init_db()

    if args.list:
        list_users()
    elif args.username and args.password:
        pwd_hash = hash_password(args.password)
        fn = args.firstname or "Practice"
        ln = args.lastname or "User"
        user = create_user(fn, ln, args.username, pwd_hash, args.tier)
        if user:
            print(f"✅ User '{user['username']}' created successfully (Tier {args.tier})!")
        else:
            print(f"❌ Failed to create user '{args.username}'")
    else:
        # Default behavior: interactive wizard
        interactive_add_user()


if __name__ == "__main__":
    main()
