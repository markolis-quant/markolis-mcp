#!/usr/bin/env node

/**
 * Markolis MCP Node.js Stdio Bridge.
 * Proxies standard I/O JSON-RPC serially in FIFO order to the hosted Markolis MCP endpoint.
 */

const http = require('http');
const https = require('https');
const readline = require('readline');

const DEFAULT_ENDPOINT = 'https://www.markolis.com/api/mcp';
const REQUEST_TIMEOUT_MS = 30000;
const endpointUrl = new URL(
  process.env.MARKOLIS_ENDPOINT || process.env.MARKOLIS_MCP_URL || DEFAULT_ENDPOINT
);
const apiKey =
  process.env.MARKOLIS_AGENT_KEY ||
  process.env.MARKOLIS_AGENT_TOKEN ||
  process.env.MARKOLIS_API_KEY ||
  '';
const transport = endpointUrl.protocol === 'http:' ? http : https;
const defaultPort = endpointUrl.protocol === 'http:' ? 80 : 443;

function emitJsonRpcError(id, code, message) {
  const errObj = {
    jsonrpc: '2.0',
    error: { code, message },
    id: id === undefined ? null : id,
  };
  process.stdout.write(JSON.stringify(errObj) + '\n');
}

function forwardSsePayloads(rawBody) {
  const blocks = rawBody.split(/\r?\n\r?\n/);
  for (const block of blocks) {
    const dataLines = block
      .split(/\r?\n/)
      .filter((l) => l.startsWith('data:'))
      .map((l) => l.slice(5).trimStart())
      .filter(Boolean);
    if (dataLines.length === 0) continue;
    const joined = dataLines.join('\n').trim();
    if (!joined || joined === '[DONE]') continue;
    process.stdout.write(joined + '\n');
  }
}

function sendLine(trimmed) {
  return new Promise((resolve) => {
    let isNotification = false;
    let requestId = null;
    try {
      const parsed = JSON.parse(trimmed);
      if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
        isNotification = !('id' in parsed) || parsed.id === undefined;
        requestId = 'id' in parsed ? parsed.id : null;
      }
    } catch {
      // Let upstream return a standard JSON-RPC parse error.
    }

    const payload = Buffer.from(trimmed, 'utf-8');
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'MCP-Protocol-Version': '2025-03-26',
      'Content-Length': payload.length,
      'User-Agent': 'markolis-mcp-node/2.10.0',
    };

    if (apiKey) {
      headers['Authorization'] = `Bearer ${apiKey}`;
    }

    const req = transport.request(
      {
        hostname: endpointUrl.hostname,
        port: endpointUrl.port || defaultPort,
        path: `${endpointUrl.pathname}${endpointUrl.search}`,
        method: 'POST',
        headers,
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          const body = data.trim();
          const statusCode = res.statusCode || 200;
          const contentType = String(res.headers['content-type'] || '').toLowerCase();

          if (isNotification || statusCode === 202 || statusCode === 204 || !body) {
            resolve();
            return;
          }

          if (statusCode >= 400) {
            try {
              const parsedErr = JSON.parse(body);
              if (parsedErr && parsedErr.jsonrpc === '2.0') {
                process.stdout.write(JSON.stringify(parsedErr) + '\n');
                resolve();
                return;
              }
            } catch {
              // Fall through to synthesized JSON-RPC error.
            }
            emitJsonRpcError(requestId, -32000, `Markolis upstream HTTP ${statusCode}: ${body}`);
            resolve();
            return;
          }

          if (contentType.includes('text/event-stream')) {
            forwardSsePayloads(data);
            resolve();
            return;
          }

          process.stdout.write(body + '\n');
          resolve();
        });
      }
    );

    req.setTimeout(REQUEST_TIMEOUT_MS, () => {
      req.destroy(new Error('Request timed out'));
    });

    req.on('error', (err) => {
      if (!isNotification) {
        emitJsonRpcError(requestId, -32603, `Markolis proxy error: ${err.message}`);
      }
      resolve();
    });

    req.write(payload);
    req.end();
  });
}

const lineQueue = [];
let draining = false;
let stdinClosed = false;

async function drainQueue() {
  if (draining) return;
  draining = true;
  try {
    while (lineQueue.length > 0) {
      const next = lineQueue.shift();
      await sendLine(next);
    }
  } finally {
    draining = false;
    if (stdinClosed && lineQueue.length === 0) {
      process.exit(0);
    }
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
});

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;
  lineQueue.push(trimmed);
  void drainQueue();
});

rl.on('close', () => {
  stdinClosed = true;
  if (!draining && lineQueue.length === 0) {
    process.exit(0);
  }
});
