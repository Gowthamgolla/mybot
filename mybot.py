from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re
import json

# Load or initialize the custom referral links
def load_links():
    try:
        with open('custom_links.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_links(custom_links):
    with open('custom_links.json', 'w') as f:
        json.dump(custom_links, f)

custom_links = load_links()  # Load saved links on startup

# Function to modify referral links
def modify_link(text):
    for key, custom_link in custom_links.items():
        # Pattern to match the specific referral link based on the keyword
        pattern = re.compile(rf"https:\/\/t\.me\/{key}_app_bot\/\S+")
        # Replace the matched link with your custom link
        text = re.sub(pattern, custom_link, text)
    return text

# /start command
def start(update, context):
    update.message.reply_text("Send me a referral link, and I'll replace it with your custom link if it matches any!")

# /addlink command to dynamically add custom referral links
def add_link(update, context):
    try:
        # Extract keyword and link from the command arguments
        keyword = context.args[0]
        new_link = context.args[1]
        
        # Add or update the link
        custom_links[keyword] = new_link
        save_links(custom_links)  # Save to file
        
        update.message.reply_text(f"Link for '{keyword}' has been added/updated!")
    except IndexError:
        update.message.reply_text("Usage: /addlink <keyword> <your_referral_link>")

# Handle incoming messages with potential referral links
def handle_message(update, context):
    user_message = update.message.text
    
    # Modify the message if it contains a referral link
    modified_message = modify_link(user_message)
    
    if user_message != modified_message:
        update.message.reply_text(f"Here is your modified message:\n{modified_message}")
    else:
        update.message.reply_text("No matching referral link found.")

def main():
    # Bot token from BotFather
    API_TOKEN = 'YOUR_BOT_API_TOKEN'

    # Create Updater and attach dispatcher
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("addlink", add_link))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
