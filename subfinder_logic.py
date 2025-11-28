#logic file
import os
import subprocess
import sys
import time
from colors import *
from ui import banner, line


spinner_frames = [
    "⠋","⠙","⠹","⠸",
    "⠼","⠴","⠦","⠧",
    "⠇","⠏"
]

def silent_run(cmd):
    """Run command silently (hide output)"""
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def spinner_line(label, process):
    i = 0
    while process.poll() is None:
        frame = spinner_frames[i % len(spinner_frames)]
        sys.stdout.write(f"\r{label} {frame} \033[K")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1

   
    sys.stdout.write(f"\r[✔] {label} completed\033[K\n")
    sys.stdout.flush()

    
    time.sleep(0.6)
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def subfinder_menu(target):
    os.system("clear")
    banner()

    print(GREEN + "Favourites" + RESET)
    print("""
1. subfinder -d $target -all -recursive -o domain3.txt
2. subfinder -d $target -all -active -rl 20 -o domain4.txt
3. subfinder -d $target -all -active -rl 20 -t 10 -o domain5.txt
4. subfinder -d $target -o domain6.txt
""")

    print(BOLD + CYAN + "Menu:\n" + RESET)
    print(GREEN + "01)" + RESET + "Default / Favourite")
    print(GREEN + "02)" + RESET + "Custom")
    line()

    choice = input(YELLOW + "Select: " + RESET)

    if choice == "1":
        subfinder_run(target)


def subfinder_run(target):

    # Ensure target directory exists
    os.makedirs(f"result/{target}", exist_ok=True)

    commands = [
        f"subfinder -d {target} -all -recursive -o result/{target}/domain3.txt",
        f"subfinder -d {target} -all -active -rl 20 -o result/{target}/domain4.txt",
        f"subfinder -d {target} -all -active -rl 20 -t 10 -o result/{target}/domain5.txt",
        f"subfinder -d {target} -o result/{target}/domain6.txt"
    ]

    print("\n")

    for i, cmd in enumerate(commands, 1):
        label = f"Running {i}/{len(commands)}"
        process = silent_run(cmd)
        spinner_line(label, process)

    print(GREEN + "\n[✔] All Subfinder tasks completed!\n" + RESET)

    # Merge files
    mergcmd = (
        f"cat result/{target}/domain3.txt "
        f"result/{target}/domain4.txt "
        f"result/{target}/domain5.txt "
        f"result/{target}/domain6.txt "
        f"| sort -u > result/{target}/final_subs.txt"
    )

    process_merg = silent_run(mergcmd)
    spinner_line("Creating final file", process_merg)

  # HTTPX COMMAND
    httpxcmd = (
        f'echo "status code 200 and 301" > result/{target}/alive.txt && '
        f'httpx -l result/{target}/final_subs.txt -sc -cl '
        f'| grep -E "200|301" >> result/{target}/alive.txt'
    )

    process_httpx = silent_run(httpxcmd)
    spinner_line("Running httpx", process_httpx)

    print(GREEN + "\n[✔] ALL DONE!\n" + RESET)
