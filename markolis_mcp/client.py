#!/usr/bin/env python3
"""Markolis MCP Stdio-to-HTTP Gateway Bridge.

A robust client bridge that enables local MCP hosts (Claude Desktop,
Cursor, Windsurf, Zed) to communicate seamlessly with the hosted Markolis
market intelligence engine over streaming HTTP.
"""

import json
import os
import ssl
import sys
import urllib.request
import urllib.error

DEFAULT_ENDPOINT = "https://www.markolis.com/api/mcp"


def get_ssl_context() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        return ctx
    except Exception:
        return ssl._create_unverified_context()


def main() -> None:
    endpoint = os.environ.get("MARKOLIS_ENDPOINT", DEFAULT_ENDPOINT)
    api_key = os.environ.get("MARKOLIS_API_KEY", "")
    ssl_context = get_ssl_context()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "markolis-mcp-client/1.0.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req_data = line.encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=req_data,
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as resp:
                result = resp.read().decode("utf-8")
                sys.stdout.write(result + "\n")
                sys.stdout.flush()

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            err_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": e.code,
                    "message": f"Markolis upstream HTTP error: {err_body}",
                },
                "id": None,
            }
            sys.stdout.write(json.dumps(err_response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Bridge internal error: {str(e)}",
                },
                "id": None,
            }
            sys.stdout.write(json.dumps(err_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
