#!/usr/bin/env python3
"""Markolis MCP Stdio-to-HTTP Gateway Bridge.

A robust client bridge that enables local MCP hosts (Claude Desktop,
Cursor, Windsurf, Zed, Antigravity) to communicate seamlessly with the hosted
Markolis market intelligence engine over Streamable HTTP.
"""

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any, Optional

DEFAULT_ENDPOINT = "https://www.markolis.com/api/mcp"
REQUEST_TIMEOUT_SECONDS = 30


def get_ssl_context() -> ssl.SSLContext:
    """Return a strict verified TLS SSLContext (no unverified bypass)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass

    for ca_path in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
    ):
        if os.path.exists(ca_path):
            return ssl.create_default_context(cafile=ca_path)

    return ssl.create_default_context()


def _emit_jsonrpc_error(req_id: Any, code: int, message: str) -> None:
    err_response = {
        "jsonrpc": "2.0",
        "error": {"code": code, "message": message},
        "id": req_id,
    }
    sys.stdout.write(json.dumps(err_response) + "\n")
    sys.stdout.flush()


def _forward_sse_payloads(raw_body: str) -> None:
    for block in raw_body.split("\n\n"):
        data_lines = [
            line[5:].lstrip()
            for line in block.splitlines()
            if line.startswith("data:")
        ]
        if not data_lines:
            continue
        joined = "\n".join(data_lines).strip()
        if not joined or joined == "[DONE]":
            continue
        sys.stdout.write(joined + "\n")
        sys.stdout.flush()


def main() -> None:
    endpoint = (
        os.environ.get("MARKOLIS_ENDPOINT")
        or os.environ.get("MARKOLIS_MCP_URL")
        or DEFAULT_ENDPOINT
    )
    api_key = (
        os.environ.get("MARKOLIS_AGENT_KEY")
        or os.environ.get("MARKOLIS_AGENT_TOKEN")
        or os.environ.get("MARKOLIS_API_KEY")
        or ""
    )
    ssl_context = get_ssl_context()
    is_https = endpoint.lower().startswith("https://")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-03-26",
        "User-Agent": "markolis-mcp-python/2.10.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        is_notification = False
        request_id: Optional[Any] = None
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                is_notification = "id" not in parsed
                request_id = parsed.get("id")
        except Exception:
            # Let upstream return a standard JSON-RPC parse error.
            pass

        try:
            req_data = line.encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=req_data,
                headers=headers,
                method="POST",
            )

            open_kwargs = {"timeout": REQUEST_TIMEOUT_SECONDS}
            if is_https:
                open_kwargs["context"] = ssl_context

            with urllib.request.urlopen(req, **open_kwargs) as resp:
                status = getattr(resp, "status", 200)
                raw_body = resp.read().decode("utf-8")
                body = raw_body.strip()
                content_type = str(resp.headers.get("Content-Type", "")).lower()

                if is_notification or status in (202, 204) or not body:
                    continue

                if "text/event-stream" in content_type:
                    _forward_sse_payloads(raw_body)
                    continue

                sys.stdout.write(body + "\n")
                sys.stdout.flush()

        except urllib.error.HTTPError as e:
            if is_notification:
                continue
            err_body = e.read().decode("utf-8", errors="replace").strip()
            try:
                parsed_err = json.loads(err_body)
                if isinstance(parsed_err, dict) and parsed_err.get("jsonrpc") == "2.0":
                    sys.stdout.write(json.dumps(parsed_err) + "\n")
                    sys.stdout.flush()
                    continue
            except Exception:
                pass
            _emit_jsonrpc_error(request_id, -32000, f"Markolis upstream HTTP {e.code}: {err_body}")
        except Exception as e:
            if is_notification:
                continue
            _emit_jsonrpc_error(request_id, -32603, f"Bridge internal error: {str(e)}")


if __name__ == "__main__":
    main()
