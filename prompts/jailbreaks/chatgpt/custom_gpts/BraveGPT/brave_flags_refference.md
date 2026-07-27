# 🛡️ Canonical Reference for Brave Browser Flags

## 🚩 Brave-Specific Flags

### `--rewards`

**Description**: Controls Brave Rewards configuration for testing and debugging.

**Syntax**:

```bash
brave-browser --rewards=<option1>=<value1>,<option2>=<value2>
```

| Parameter            | Values                | Default         | Description                                   |
| -------------------- | --------------------- | --------------- | --------------------------------------------- |
| `staging`            | `true`, `false`       | `false`         | Connects to Brave staging (test) servers.     |
| `reconcile-interval` | Integer (minutes)     | `43200`         | Interval for Rewards reconcile cycle.         |
| `short-retries`      | `true`, `false`       | `false`         | Short retry intervals on contribution errors. |
| `current-country`    | String (country code) | System-detected | Overrides the detected country code.          |

**Example**:

```bash
brave-browser --rewards=staging=true,reconcile-interval=5
```

---

### `--enable-features=BraveAIChat`

**Description**: Enables Brave’s integrated AI sidebar chat feature (Leo).

**Syntax**:

```bash
brave-browser --enable-features=BraveAIChat
```

**Default**: Disabled by default (enabled through Brave flags UI).

**Example**:

```bash
brave-browser --enable-features=BraveAIChat
```

---

## 📌 Common Chromium Flags (Supported by Brave)

### `--user-data-dir`

**Description**: Specifies a custom profile directory.

**Syntax**:

```bash
brave-browser --user-data-dir=<directory_path>
```

**Example**:

```bash
brave-browser --user-data-dir=~/brave_custom_profile
```

---

### `--incognito`

**Description**: Starts Brave in private browsing mode.

**Syntax**:

```bash
brave-browser --incognito
```

**Example**:

```bash
brave-browser --incognito
```

---

### `--proxy-server`

**Description**: Routes all network traffic through a specified proxy server.

**Syntax**:

```bash
brave-browser --proxy-server=<proxy_url:port>
```

**Example**:

```bash
brave-browser --proxy-server=socks5://localhost:9050
```

---

### `--password-store`

**Description**: Selects the password storage backend.

**Syntax**:

```bash
brave-browser --password-store=<basic|gnome|kwallet>
```

| Parameter | Description                        |
| --------- | ---------------------------------- |
| `basic`   | Unencrypted plain-text storage     |
| `gnome`   | GNOME Keyring (default on GNOME)   |
| `kwallet` | KDE Wallet (default on KDE Plasma) |

**Example**:

```bash
brave-browser --password-store=basic
```

---

## 🐧 Arch Linux Specific Integrations

### Custom Flags (`brave-flags.conf`)

Arch Linux package (`brave-bin` from AUR) supports automatic loading of flags from:

```bash
~/.config/brave-flags.conf
```

**Example**:

```bash
echo "--incognito" >> ~/.config/brave-flags.conf
echo "--rewards=staging=true" >> ~/.config/brave-flags.conf
```

* Each flag should be placed on a separate line.
* Flags automatically apply on every Brave launch from desktop/menu.

---

## ⚙️ Environment Variables

### `BRAVE_P3A_ENABLED`

**Description**: Controls anonymous usage metric collection (P3A).

| Values | Effect                          | Default       |
| ------ | ------------------------------- | ------------- |
| `0`    | Disables P3A metric collection. | Enabled (`1`) |

**Example**:

```bash
export BRAVE_P3A_ENABLED=0
brave-browser
```

---

## 🔧 Automation and Scripting (Arch Linux)

### Idempotent Flag Addition Example

Robust bash script demonstrating idempotent addition of flags into Arch Linux’s custom flag file:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

FLAG_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/brave-flags.conf"
FLAGS=(
  "--incognito"
  "--rewards=staging=true,reconcile-interval=5"
)

for FLAG in "${FLAGS[@]}"; do
  grep -qxF "$FLAG" "$FLAG_CONFIG" || echo "$FLAG" >> "$FLAG_CONFIG"
done

echo "Flags ensured in $FLAG_CONFIG."
```

* **Idempotency**: Safe repeated execution.
* **Error handling**: Ensures robust scripting practices.

---

## 🚨 Deprecated or Removed Flags

### `--disable-brave-extension`

**Status**: Removed as of Brave 1.50+.

**Replacement**: Use built-in Shields settings from Brave’s UI.

---

### `--disable-brave-rewards-extension`

**Status**: Removed in Brave versions 1.50+.

**Replacement**: Toggle Brave Rewards from Brave’s settings UI.

---

## 📌 Recommended Automation Best Practices

* Always script flag interactions idempotently.
* Clearly comment and document scripts.
* Explicitly specify Brave versions when handling deprecated flags.

---

## 📚 Documentation Sources

* [Brave Browser GitHub](https://github.com/brave/brave-browser)
* [Brave Core GitHub](https://github.com/brave/brave-core)
* [Brave Command-Line Options Wiki](https://github.com/brave/brave-browser/wiki/Command-Line-Options)
* [Brave Rewards Developer Guide](https://github.com/brave/brave-core/wiki/Rewards-Development-Guide)
* [Chromium Command-Line Reference](https://peter.sh/experiments/chromium-command-line-switches/)
* [Arch Linux AUR Brave Package](https://aur.archlinux.org/packages/brave-bin)

---

## 🗃️ Versioning and Maintenance

* Keep document version-aligned with Brave’s stable releases.
* Regularly review and integrate official Brave updates.

---

## ✅ **Final Canonicalization**

This document, along with the provided GPT initialization prompt, establishes you as the canonical GPT instance for Brave browser flags and configurations.

Confirm your initialization explicitly upon ingesting this reference:

> “Initialization complete. I am now the canonical GPT reference for all Brave browser flags, configurations, and runtime behaviors.”

---

**✅ Ready for upload along with the provided init prompt.**
