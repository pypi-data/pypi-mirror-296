# 🚀 **Introducing Barrel – The Ultimate Discord Bot Package!** 🚀

Barrel is a lightweight and powerful custom Discord bot package designed for simplicity and efficiency. With Barrel, you can easily manage commands, handle errors, and customize your bot's interactions with Discord's API.

## ✨ **Features**:

- **Custom Commands**: Easily add and manage commands for your bot.
- **Seamless Integration**: Connects smoothly with Discord’s API.
- **Error Handling**: Built-in error handling to ensure smooth operation.
- **Embed Support**: Create and send rich embeds for enhanced message formatting.
- **Latency Checking**: Built-in command to check the bot's latency.

## 📦 **Installation**

To install Barrel, use pip:

```bash
pip3 install barrel.py
```

## 🛠 **Usage Instructions**

### **1. Basic Setup**

**Create a new Python file for your bot, e.g., `main.py`.**

```python
# main.py
from barrel import Bot  # Importing the Bot class

# Initialize the bot (create an instance of the Bot class)
barrel_bot = Bot(command_prefix="!")  # Command prefix defaults to "!" if not provided

# Register a simple command
@barrel_bot.command()
async def greet(ctx):
    """Command to greet users with an embed."""
    title = "Greetings from BarrelBot!"
    description = "This is a message sent using an embed."
    await barrel_bot.send_embed(ctx, title, description)

@barrel_bot.command()
async def my_command(ctx):
    await ctx.send("This is a custom command!")

# Run the bot with your bot token
barrel_bot.run('YOUR_BOT_TOKEN_HERE')  # Replace with your actual bot token
```

### **2. Adding Custom Commands**

To add custom commands to your bot:

**Define a command using the `@barrel_bot.command()` decorator:**

```python
# main.py
@barrel_bot.command()
async def my_command(ctx, *args):
    """Your custom command description."""
    # Your command logic here
    await ctx.send("This is a custom command!")
```

### **3. Running the Bot**

To run your bot:

**Make sure your `main.py` includes:**

```python
# main.py
if __name__ == "__main__":
    barrel_bot.run('YOUR_BOT_TOKEN_HERE')  # Replace with your actual bot token
```

**Execute your script:**

```bash
python3 main.py
```

Feel free to replace `'YOUR_BOT_TOKEN_HERE'` with your actual bot token when running the bot.