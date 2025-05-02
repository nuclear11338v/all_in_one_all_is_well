<p align="center">
  <img src="BotForgeHub.jpg" alt="BotForgeHub Logo" width="400"/>
</p>

<h1 align="center">BotForgeHub</h1>

<p align="center">
  A powerful and feature-rich Telegram bot framework built with Python.
</p>

<p align="center">
  <a href="https://t.me/OFFICIAL_BOTFORGEHUB">Official Bot</a> •
  <a href="https://t.me/TEAM_X_OG">Support Group</a>
</p>

---

## ✨ Features

- **User-to-Admin Communication**: Forwards messages, media, and files from users to admins.
- **Bot Cloning**: Easily create a clone of this bot using `/clone`. (Limit: 1 per user).
- **Admin Tools**:
  - Reply to users, broadcast messages, manage bans.
  - Approve clone bots via `/approve_clone`.
- **Custom Commands & Filters**:
  - Add auto-response triggers using `/filter` and `/addcommand`.
- **Multilingual Support**: Currently supports English (`en`) and Hindi (`hi`).
- **Ban System**: Bans users with reasons; restricts access automatically.
- **Clone Expiry**: Cloned bots run for 3 days by default (can be extended by admin).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Install dependencies:
- ```bash
  pip install pyTelegramBotAPI
  ```

## Installation

```shell
git clone https://github.com/your-username/BotForgeHub.git
cd BotForgeHub
```

1. **Set Bot Token**:
   Create a `.env` file or edit `config.py`:

   ```env
   BOT_TOKEN=your-bot-token-here
   ```
### 
2. **Ensure these directories exist**:
```shell
   * `user_data/`
   * `clones/`
   * `broadcasting/`
   * `banned/`
```
2. **Run the bot**:

   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

* **Admin IDs** in `config.py`:

  ```python
  ADMIN_IDS = {123456789}
  ```

* **Customize the `/start` message**:

  ```bash
  /editstart Welcome to my bot!
  ```

---

## 📖 Commands

### User Commands

* `/start` – Show welcome message.
* `/help` – Help menu.
* `/clone` – Start the cloning process.

### Admin Commands

```lua
* `/reply <username/user_id> <message>` – Reply to users.
* `/broadcast <message>` – Send message to all users.
* `/users` – List all users.
* `/ban <user>` – Ban a user.
* `/unban <user>` – Unban a user.
* `/banned` – List banned users.
* `/addcommand <command> <response>` – Add custom command.
* `/filter <trigger> <response>` – Auto-reply on keyword.
* `/stopfilter <trigger>` – Delete a filter.
* `/filters` – List all filters.
* `/approve_clone <bot_username>` – Extend a cloned bot’s access.
```
### Bot Cloning Steps

1. Use `/clone`
2. Provide valid BotFather token
3. Enter your admin ID
4. Confirm setup
5. Clone lives for 3 days (extendable)

---

## 📁 Project Structure

```
BotForgeHub/
├── main.py             # Main bot logic
├── config.py           # Settings and admin configuration
├── help.py             # Help command handler
├── clone.py            # Clone logic
├── start.py            # Start & command/filter management
├── ban.py              # Ban system
├── broadcast.py        # Broadcast handling
├── user_data/          # Stores user data
├── clones/             # Cloned bot data
├── broadcasting/       # Broadcast files
├── banned/             # Banned users data
```

---

## 🛠 Contributing

Contributions welcome!

1. Fork the repo
2. Create a branch
3. Add your changes
4. Submit a pull request

---

## ⚠️ Notes

* Cloned bots expire in 3 days unless approved.
* Back up `user_data/` and `clones/` to prevent data loss.
* Ensure the bot has necessary Telegram permissions.

---

## 📬 Contact

For issues, join our [Support Group](https://t.me/TEAM_X_OG) or open an issue on GitHub.
Official Bot: [@OFFICIAL\_BOTFORGEHUB](https://t.me/OFFICIAL_BOTFORGEHUB)

---

<p align="center">
  Built with ❤️ by <a href="https://t.me/TEAM_X_OG">TEAM_X_OG</a>
</p>
