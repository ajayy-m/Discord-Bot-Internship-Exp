# 🎉 Discord Fun Bot

A simple and fun Discord bot made using `discord.py`!  
This bot includes basic commands to entertain users like telling jokes, rolling dice, and making choices.

## 🔗 Repository
**GitHub:** [ajayy-m/Discord-Fun-Bot](https://github.com/ajayy-m/Discord-Fun-Bot)



## 📌 Features

| Command       | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `/joke`       | Sends a random joke from a collection of tech & pun-based jokes             |
| `/roll`       | Rolls a standard 6-sided die and returns a random number                    |
| `/eightball`  | Magic 8-Ball style response to yes/no questions                             |
| `/choose`     | Randomly chooses from a list of given options                               |



## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ajayy-m/Discord-Fun-Bot.git
cd Discord-Fun-Bot
````

### 2. Install dependencies

Make sure you have Python 3.8+ installed.

```bash
pip install -U discord.py
```

### 3. Set up your bot token

Replace `"Token"` at the bottom of the code with your actual Discord bot token.
Never share your token publicly.

```python
bot.run("YOUR_DISCORD_BOT_TOKEN")
```

### 4. Run the bot

```bash
python bot.py
```



## ⚙️ Intents Note

This bot uses `message_content` intent.
Ensure you enable it in your [Discord Developer Portal](https://discord.com/developers/applications) under **Bot > Privileged Gateway Intents**.



## 🧠 Code Overview

* Written using `discord.ext.commands` for modular command handling
* Uses Python's `random` module to keep replies fresh and fun
* Beginner-friendly and easy to expand with more commands


## 🙏 Acknowledgements

* [discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)
* Inspiration from countless Discord community bots
