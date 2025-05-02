<p align="center">
  <img src="BotForgeHub.jpg" alt="BotForgeHub Logo" width="400"/>
</p>

# BotForgeHub

Welcome to **BotForgeHub**, a powerful and feature-rich Telegram bot framework built with Python and the `python-telegram-bot` library. This bot allows users to communicate with admins, supports bot cloning for custom deployments, and provides advanced features like broadcasting, user management, and content filtering. Whether you're a developer looking to create your own Telegram bot or an admin managing user interactions, BotForgeHub has you covered!

## ✨ Features

- **User-to-Admin Communication**: Users can send text, photos, videos, and more, which are forwarded to admins for seamless interaction.
- **Bot Cloning**: Create your own bot instance with a custom token and admin ID using the `/clone` command (limited to 1 clone per user).
- **Admin Tools**:
  - Reply to users with `/reply <username or user_id> <message>` or directly respond to forwarded messages.
  - Broadcast messages to all users with `/broadcast <message>` (supports text, media, and more).
  - Manage users with `/users`, `/ban`, `/unban`, and `/banned` commands.
  - Approve cloned bots for extended use with `/approve_clone <bot_username>`.
- **Custom Commands and Filters**:
  - Add custom commands with `/addcommand <command> <response>`.
  - Set message filters with `/filter <trigger> <response>` to auto-respond to specific keywords.
- **Multilingual Support**: Help messages available in English (`en`) and Hindi (`hi`).
- **User Data Management**: Stores user data securely in JSON files for easy access and management.
- **Ban System**: Admins can ban/unban users with reasons, and banned users are restricted from using the bot.
- **Clone Expiry**: Cloned bots run for 3 days by default, with an option for admins to extend via approval.

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Dependencies**: Install required packages using:
  ```bash
  pip install pyTelegramBotAPI
  ```

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/BotForgeHub.git
   cd BotForgeHub
   ```

2. **Set Up Environment**:
   - Create a `.env` file or set the `BOT_TOKEN` environment variable with your Telegram Bot Token from [BotFather](https://t.me/BotFather).
     ```bash
     BOT_TOKEN=your-bot-token-here
     ```

3. **Directory Structure**:
   - Ensure the following directories exist: `user_data`, `clones`, `broadcasting`, and `banned`.
   - The bot will create these automatically if they don't exist.

4. **Run the Bot**:
   ```bash
   python main.py
   ```

### Configuration

- **Admin IDs**: Update the `ADMIN_IDS` set in `config.py` with the Telegram user IDs of admins.
  ```python
  ADMIN_IDS = {your_admin_id_here}
  ```
- **Bot Token**: Set the `BOT_TOKEN` in `config.py` or via environment variables.
- **Custom Start Message**: Use `/editstart <message>` to customize the bot's start message.

## 📖 Usage

### User Commands
- `/start`: Displays the welcome message.
- `/help`: Shows help messages (in English or Hindi).
- `/clone`: Initiates the bot cloning process (requires a valid BotFather token and admin ID).

### Admin Commands
- `/reply <username or user_id> <message>`: Send a message to a specific user.
- `/broadcast <message>`: Send a message or media to all users.
- `/users`: List all registered users.
- `/ban <username or user_id> [reason]`: Ban a user.
- `/unban <username or user_id>`: Unban a user.
- `/banned`: List all banned users.
- `/addcommand <command> <response>`: Add a custom command.
- `/filter <trigger> <response>`: Add a message filter.
- `/stopfilter <trigger>`: Remove a filter.
- `/filters`: List all active filters.
- `/approve_clone <bot_username>`: Approve a cloned bot for extended use.

### Cloning a Bot
1. Use `/clone` and provide a valid BotFather token.
2. Enter the admin ID for the cloned bot.
3. Confirm the cloning process.
4. The cloned bot will be active for 3 days unless approved by an admin.

## 📂 Project Structure

MAIN/
├── main.py           # Main bot script
├── config.py         # Configuration (bot token, admin IDs)
├── help.py           # Help messages and command
├── clone.py          # Bot cloning functionality
├── start.py          # Start message and custom command/filter management
├── ban.py            # User ban/unban system
├── broadcast.py      # Broadcasting and user listing
├── user_data/        # Stores user data in JSON files
├── clones/           # Stores cloned bot instances
├── broadcasting/     # Broadcasting-related files
├── banned/           # Ban-related files

## 🛠️ Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## ⚠️ Notes
- Cloned bots expire after 3 days unless approved by an admin.
- Ensure the bot has sufficient permissions to forward messages and interact with users.
- Regularly back up the `user_data` and `clones` directories to prevent data loss.

## 📬 Contact

For support or inquiries, contact the admin via the bot or open an issue on GitHub.

---

<p align="center">
  Built with ❤️
  t.me/TEAM_X_OG
  t.me/OFFICIAL_BOTFORGEHUB
</p>
