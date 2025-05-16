import requests
import os
import time
import random
import string
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def set_console_title(total, checked):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    os.system(f"title {timestamp} {checked}/{total} checked")

def log_hit(username):
    with open("hits.txt", "a") as f:
        f.write(username + "\n")

def check_username(username):
    url = f"https://apim.rec.net/accounts/account?username={username}"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }

    try:
        start = time.perf_counter()
        response = requests.get(url, headers=headers, timeout=5)
        elapsed = int((time.perf_counter() - start) * 1000)  # ms

        if response.status_code == 200:
            return f"{RED}[+] TAKEN {username} ({elapsed}ms){RESET}", False
        elif response.status_code == 404:
            return f"{GREEN}[+] AVAILABLE {username} ({elapsed}ms){RESET}", True
        else:
            return f"{YELLOW}[+] ERROR {username} ({response.status_code}, {elapsed}ms){RESET}", False
    except Exception as e:
        return f"{YELLOW}[+] FAIL {username} ({str(e)}){RESET}", False

def generate_username():
    prefix = random.choice(string.ascii_lowercase + string.digits)
    separator = random.choice(['-', '_'])
    suffix = random.choice(string.ascii_lowercase + string.digits)
    return prefix + separator + suffix

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("1. One username")
    print("2. Wordlist")

    option = input("Select: ").strip()
    usernames = []

    if option == "1":
        usernames.append(input("Username: ").strip())
    elif option == "2":
        path = input("Wordlist: ").strip()
        if not os.path.exists(path):
            print("File not found.")
            return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            usernames = [line.strip() for line in f if line.strip()]
    elif option == "3":
        amount = int(input("How many usernames to generate? ").strip())
        usernames = [generate_username() for _ in range(amount)]
    else:
        print("Invalid option.")
        return

    total = len(usernames)
    checked = 0

    for name in usernames:
        result, available = check_username(name)
        checked += 1
        set_console_title(total, checked)
        print(result)
        if available:
            log_hit(name)
        time.sleep(0.4)  # faster delay

    print(f"\n{GREEN}Done. Hits saved to hits.txt{RESET}")

if __name__ == "__main__":
    main()
