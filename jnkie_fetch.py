"""
JNKIE fetch paste the script LINK + the KEY, and it pulls down the
delivered script FOR READING (it does not run it). It does exactly what the
official loader does: a valid key is required, otherwise it stops on LDR-DENIED.

Dependency (to decompress the brotli response):
    pip install brotli
"""

import re
import sys
import requests


def extract_id(link: str) -> str:
    m = re.search(r"[0-9a-fA-F]{64}", link)
    if not m:
        sys.exit("Could not find a script ID in the link.")
    return m.group(0)

def main() -> None:
    link = input("Script link: ").strip()
    key  = input("SCRIPT_KEY:  ").strip()

    script_id = extract_id(link)
    delivery = f"https://api.jnkie.com/api/v1/luascripts/delivery/{script_id}?v=2"

    session = requests.Session()
    session.headers.update({"User-Agent": "Roblox/WinInet", "Accept": "*/*"})

    r = session.post(delivery, data=key.encode(),
                     headers={"Content-Type": "text/plain"})
    print("delivery status:", r.status_code)
    body = r.text

    if r.status_code in (400, 401, 403) and body.startswith("LDR-DENIED"):
        sys.exit(f"Denied: {body}\n(Wrong key, or the endpoint expects an executor.)")

    if r.status_code == 200 and body.startswith("https://cdn.jnkie.com/"):
        r = session.get(body)
        print("cdn status:", r.status_code)
        body = r.text

    if not body:
        sys.exit("Empty response.")

    out = f"{script_id[:12]}.lua"
    with open(out, "w", encoding="utf-8", errors="replace") as f:
        f.write(body)

    print(f"[+] {len(body)} characters saved to: {out}")
    print("=== FIRST 800 CHARACTERS ===")
    print(body[:800])


if __name__ == "__main__":
    main()
