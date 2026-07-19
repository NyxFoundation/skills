---
name: mordred-hermes-setup
description: Workflows for installing, configuring, and pairing the Mordred-Hermes plugin and browser extension.
---

# Mordred-Hermes Setup & Pairing

This skill governs the installation and operational setup of the `InternetMaximalism/mordred-hermes` plugin, specifically the pairing flow between the Hermes CLI and the browser extension.

## Trigger Conditions
- User asks to install or configure the Mordred plugin.
- User needs a pairing number/code for the Mordred browser extension.
- `hermes mordred extension pair` fails with import errors.

## Core Workflow

### 1. Installation & Dependency Resolution
The plugin requires the `extension` extra for pairing and server capabilities. If `hermes mordred extension pair` fails with an `ExtensionGatewayUnavailable` or `ImportError`, the dependencies are missing.

**Correct Installation Path:**
```sh
cd ~/.hermes/plugins/mordred-hermes
uv sync --extra extension
```

### 2. Executing Pairing
Pairing must be done via the CLI to generate a code that the extension consumes.

**Command:**
```sh
# Using the plugin's venv directly (recommended for reliability)
~/.hermes/plugins/mordred-hermes/.venv/bin/hermes-mordred extension pair
```

**Expected Result:**
- A pairing code in the format `MORT-XXXXXXXX-XXXXXXXX`.
- A terminal-based QR code (requires `qrcode` package).
- The command will block and poll for the extension to connect.

### 3. Verification & Server State
The pairing command only works if a WebSocket server is actively listening for the code.
- **Requirement**: Run `hermes-mordred extension serve` (or a full Hermes gateway) in a separate process.
- **Default Endpoint**: `ws://localhost:7788/ext`

## Pitfalls & Troubleshooting

- **ImportError / ModuleNotFoundError**: This usually means the `extension` extra was not synced. Run `uv sync --extra extension` inside the plugin directory.
- **"Waiting for the extension to connect..." (Infinite loop)**: 
    - Check if the `extension serve` process is running.
    - Verify the browser extension is installed and the code is entered exactly.
    - Ensure no firewall/VPN is blocking `localhost:7788`.
- **QR Code Missing**: If `qrcode` is not installed, the CLI falls back to plaintext. The code is still valid.

## Verification
- Successful pairing is confirmed when the CLI prints `Paired (YYYY-MM-DD HH:MM:SS).`
- The user should be able to chat from the extension immediately after.
