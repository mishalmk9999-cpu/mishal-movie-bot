from pyrogram import Client, filters
import configparser

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")

api_id = int(config["telegram"]["api_id"])
api_hash = config["telegram"]["api_hash"]
bot_token = config["telegram"]["bot_token"]
admin_ids = [int(x) for x in config["bot"]["admin_ids"].split(",")]

bot = Client("CinemaWorldBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start message
@bot.on_message(filters.command("start"))
def start(client, message):
    first = message.from_user.first_name
    welcome = config["bot"]["welcome_message"].format(first_name=first)
    message.reply_text(welcome)

# Help message
@bot.on_message(filters.command("help"))
def help_command(client, message):
    message.reply_text("🎬 Commands:\n/start - Welcome message\n/help - Show help\n/upload - Admin upload movie")

# Admin movie upload
@bot.on_message(filters.command("upload") & filters.user(admin_ids))
def upload_movie(client, message):
    message.reply_text("📁 Please send the movie file now...")

# Any file received
@bot.on_message(filters.document | filters.video)
def handle_file(client, message):
    message.forward(chat_id=message.chat.id)
    message.reply_text("✅ Movie uploaded successfully!")

print("🚀 Starting Cinema World Bot...")
bot.run()