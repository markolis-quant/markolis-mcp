#!/usr/bin/env node

/**
 * Markolis MCP Node.js Stdio Bridge.
 * Proxies standard I/O JSON-RPC to the hosted streaming Markolis MCP endpoint.
 */

const https = require('https');
const readline = require('readline');

const DEFAULT_ENDPOINT = 'https://www.markolis.com/api/mcp';
const endpointUrl = new URL(process.env.MARKOLIS_ENDPOINT || DEFAULT_ENDPOINT);
const apiKey = process.env.MARKOLIS_API_KEY || '';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  const payload = Buffer.from(trimmed, 'utf-8');
  const headers = {
    'Content-Type': 'application/json',
    'Content-Length': payload.length,
    'User-Agent': 'markolis-mcp-node/1.0.0'
  };

  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  const req = https.request(
    {
      hostname: endpointUrl.hostname,
      port: endpointUrl.port || 443,
      path: endpointUrl.pathname,
      method: 'POST',
      headers: headers
    },
    (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        process.stdout.write(data + '\n');
      });
    }
  );

  req.on('error', (err) => {
    const errObj = {
      jsonrpc: '2.0',
      error: {
        code: -32603,
        message: `Markolis proxy error: ${err.message}`
      },
      id: null
    };
    process.stdout.write(JSON.stringify(errObj) + '\n');
  });

  req.write(payload);
  req.end();
});
