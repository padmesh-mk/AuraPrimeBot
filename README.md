# 🤖 AuraPrime - Multipurpose Python Discord Bot

AuraPrime is a feature-rich and modular Discord bot written in Python. It includes fun minigames, AFK tracking, donation and cookie logging, vote rewards, moderation tools, tag systems, and more — all designed to enhance your server experience.

> 👨‍💻 Developed by [@PadmeshMK](https://github.com/PadmeshMK)

---

## 🔧 Features

- 🎮 Minigames: Rock Paper Scissors, Coin Flip, Guess Number, Roast, and more
- 💤 AFK System with reason + ping logs
- 🛡️ Moderation: Ban, Kick, Timeout, Tempban, Unban, Purge, and more
- 🗳️ Top.gg Vote Tracking with 12-hour role reward
- 🏷️ Custom Tag System (Slash + Prefix support)
- 📦 JSON-based storage (no database needed)
- 🧠 Server and User Info Commands
- 📜 Owner-only test commands
- ⚡ Fast and modular command handling

---

## 📋 Commands

### 💤 AFK
| Command | Description |
|---------|-------------|
| `afk` | Set your status as AFK with an optional reason. |

### 📊 Bot Info
| Command | Description |
|---------|-------------|
| `botinfo` | Displays information about AuraPrime and its features. |

### ❓ Help
| Command | Description |
|---------|-------------|
| `categories` | Lists all command categories. |
| `help` | Shows help information for specific commands or categories. |

### 🔗 Invite
| Command | Description |
|---------|-------------|
| `invite` | Provides the invite link to add AuraPrime to your server. |

### 🛡️ Moderation
| Command | Description |
|---------|-------------|
| `ban` | Bans a user from the server. |
| `kick` | Kicks a user from the server. |
| `purge` | Deletes a specified number of messages in a channel. |
| `tempban` | Temporarily bans a user for a set duration. |
| `timeout` | Timeouts a user for a specified duration. |
| `unban` | Unbans a previously banned user. |
| `untimeout` | Removes timeout from a user. |

### 🏓 Ping
| Command | Description |
|---------|-------------|
| `ping` | Shows bot latency information. |

### ⚙️ Prefix
| Command | Description |
|---------|-------------|
| `prefix` | Displays or changes the command prefix. |

### 🧪 Welcomer
| Command | Description |
|---------|-------------|
| `welcomer set` | Set a welcome channel. |
| `welcomer remove` | Remove a welcome channel. |
| `welcomer test` | Test the welcome message, setted in a channel. |

### 🏠 Server Info
| Command | Description |
|---------|-------------|
| `serverinfo` | Displays information about the current server. |

### 📋 Server List
| Command | Description |
|---------|-------------|
| `serverlist` | Displays a list of all servers the bot is in (admin/owner only). |

### ⏱️ Uptime
| Command | Description |
|---------|-------------|
| `uptime` | Shows how long the bot has been running without restart. |

### 👤 User Info
| Command | Description |
|---------|-------------|
| `userinfo` | Displays information about a user. |

---

## 🚀 Invite & Support

- 🔗 [Invite AuraPrime](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=8)
- 💬 [Join Support Server](https://discord.gg/YOUR_SUPPORT_SERVER)

> Replace the links above with your actual bot/client ID and server invite

---

## 🧪 Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AuraPrime.git
cd AuraPrime
````

### 2. Create and fill the `.env` file

```env
DISCORD_TOKEN=your-bot-token
TOPGG_AUTH=your-topgg-webhook-auth
FORWARD_URL=https://your-bot-domain.com/internal-vote
WEBHOOK_URL=https://discord.com/api/webhooks/your-log-channel
```

> Never commit your `.env` file!

---

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the bot and webhook forwarder

Start Flask vote forwarder:

```bash
python flask_forwarder.py
```

Start the bot:

```bash
python main.py
```

---

## 📁 Project Structure

```
AuraPrime/
├── commands/                         # Command modules (slash + prefix)
│   ├── afk.py
│   ├── tags.py
│   ├── vote.py
│   ├── welcomer.py
│   └── ... (others like roast, 8ball, etc.)
│
├── events/                           # Event handlers (join, message, etc.)
│   ├── welcome_random_embed.py
│   ├── vote_remind.py
│   └── ... (other listeners like cookie, webhook, etc.)
│
├── data/                             # JSON storage
│   ├── afk.json
│   ├── welcomer_channel.json
│   ├── prefixes.json
│   ├── tags.json
│   ├── vote_remind.json
│   ├── votes.json
│   └── version.json
│
├── utils/                            # Utility modules (optional)
│   └── console_logger.py
│
├── main.py                           # Main bot entry
├── flask_forwarder.py                # Flask webhook listener (Top.gg vote forwarding)
├── .env                              # Secret keys (excluded from Git)
├── requirements.txt                  # Python dependencies
└── __pycache__/                      # Compiled cache (ignored)

```

---

## 📜 License

This project is licensed under the **MIT License** — feel free to fork, use, or contribute!

---

## 🙌 Credits

Made with ❤️ by [Padmesh](https://github.com/PadmeshMK)
For bugs or questions, join the support server!

```
