import os
from ui import banner, line
from colors import *
import subfinder_logic


def main_menu():
    os.system("clear")
    banner()

    target = input(YELLOW + "Enter target domain: " + RESET).strip()

    print(BOLD + CYAN + "Main Menu:\n" + RESET)
    print(GREEN + "01)" + RESET + "Subfinder")
    print(GREEN + "02)" + RESET + "Exit")
    line()

    choice = input(YELLOW + "Select: " + RESET)

    if choice == "1":
        subfinder_logic.subfinder_menu(target)
    else:
        main_menu()


main_menu()
