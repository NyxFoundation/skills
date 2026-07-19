---
name: mcp-tools
description: |
  Work with MCP (Model Context Protocol) servers and tools in Hermes.
  Covers the built-in native MCP client (stdio/HTTP transports, auto-discovery, reconnection)
  and the mcporter CLI bridge for ad-hoc server configuration and tool calling.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, model-context-protocol, tools, integrations, mcporter, native-mcp, servers]
---

# MCP Tools

This skill covers how to discover, configure, and use MCP (Model Context Protocol) servers as native Hermes tools.

## What is MCP?

MCP is an open protocol that lets AI models call tools exposed by external servers. Hermes supports two paths:

| Path | Transport | Use Case |
|------|-----------|----------|
| **Native MCP** | stdio or HTTP, auto-discovered | Servers declared in `config.yaml`; tools appear automatically |
| **mcporter CLI** | HTTP or stdio, ad-hoc | One-off servers, testing, debugging, type generation |

---

## Native MCP Client

Hermes has a built-in MCP client that connects to servers declared in your `config.yaml`.

### Configuration

Add MCP servers under `mcp.servers` in `~/.hermes/config.yaml`:

```yaml
mcp:
  servers:
    my-server:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      # or for HTTP:
      # url: http://localhost:3000/sse
```

### Behaviors
- **Auto-discovery**: Hermes queries the server on startup and registers its tools.
- **Auto-reconnection**: if the server crashes, Hermes restarts it.
- **Security filtering**: tools can be allowlisted/denylisted.
- **Zero-config**: no code changes needed to use MCP tools.

### Verification
```bash
hermes tools list | grep mcp_
```

---

## mcporter CLI

For ad-hoc MCP server interaction — testing, debugging, or servers not in `config.yaml`.

### Installation
```bash
npm install -g mcporter
```

### Key Commands
```bash
# List configured servers
mcporter list

# Add a server
mcporter add my-server npx -y @modelcontextprotocol/server-filesystem /path/to/dir

# Call a tool directly
mcporter call my-server tool_name '{"arg": "value"}'

# Generate TypeScript types for a server's tools
mcporter types my-server
```

### When to Use mcporter
- Debugging a server that won't register in Hermes
- Testing a new server before adding it to `config.yaml`
- Calling tools in CI/scripts where Hermes isn't running
- Generating types for typed tool consumption

---

## General Workflow

1. **Find a server**: check the MCP server registry or write your own.
2. **Test with mcporter**: `mcporter call` to verify it works.
3. **Add to config.yaml**: for permanent use in Hermes.
4. **Restart Hermes**: native MCP tools are discovered at startup.
5. **Use the tools**: they appear as native Hermes tools (prefixed by server name).

## Pitfalls
- MCP servers run as separate processes — they consume memory even when idle.
- stdio servers block on startup if they print to stdout before the MCP handshake.
- HTTP servers need persistent URLs; ephemeral ports break on restart.
- Tool name collisions: two MCP servers may expose tools with the same name. Hermes prefixes them.
