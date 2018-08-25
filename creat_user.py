#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys, os
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from instance.config import Config
from app.models import User_admin
def main():
    """Main entry point for script."""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind = engine)
    session = Session()
    user_list = session.execute("SELECT * from user_admin").fetchall()
    print(user_list)
    if user_list:
        print('A user already exists! Create another? (y/n):')
        create = input()
        if create == 'n':
            return

    print('Enter username: ')
    username = input()
    password = getpass()
    assert password == getpass('Password (again):')

    user = User_admin(username,generate_password_hash(password))
    session.add(user)
    session.commit()
    print('User added.')

if __name__ == '__main__':
    sys.exit(main())