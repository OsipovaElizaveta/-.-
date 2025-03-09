# -*- coding: cp1251 -*-
from interface import create_interface
from integration import setup_client

def main():
    client = setup_client()
    create_interface(client)

if __name__ == "__main__":
    main()