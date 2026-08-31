Fetch and **save** a Jnkie delivered Lua script so you can *read it before
running it* instead of blindly `loadstring(game:HttpGet(...))()`-ing an
unverified script into your executor.

## What it does

Roblox scripts protected with [JNKIE](https://jnkie.com) are usually shared as
a tiny loader:

```lua
getgenv().SCRIPT_KEY = "..."
loadstring(game:HttpGet("https://api.jnkie.com/.../<id>/download"))()
```

That `/download` endpoint only returns the **loader stub**. The real script is
delivered separately: the loader POSTs your `SCRIPT_KEY` to the `/delivery`
endpoint, receives a `cdn.jnkie.com` URL, downloads the script, and runs it.

This tool reproduces that same flow — you paste the **link** and your **key**
but at the end it **writes the delivered script to a file** instead of executing
it, so you can inspect what you're about to run.

## What it is **not**

This is **not** a ripper or a protection bypass:

- It requires a **valid key** you already have (90% of password is: "DO NOT REMOVE OR CHANGE" :) ) . Without one it simply stops on
  `LDR-DENIED` — the same as the official loader.
- There is **no executor-fingerprint spoofing** and **no key cracking**.
- It does **not** deobfuscate anything. Delivered payloads are typically
  JNKIE-obfuscated, so expect obfuscated Lua, not clean source.

Only use it for scripts you legitimately have access to. Respect script authors'
protection and JNKIE's terms of service.

## Requirements

- Python 3
- `pip install requests brotli`

(`brotli` matters the responses are Brotli-compressed, and `requests` won't
decode `br` without it.)

## Usage

```bash
python jnkie_fetch.py
```

Then paste the script link and the key when prompted. The delivered script is
saved next to the tool as `<first-12-chars-of-id>.lua`.

## Why read before running

Executors run arbitrary Lua with broad access, and shared scripts often carry a
"not verified use at your own risk" warning. Reading the code first is the
responsible move.
