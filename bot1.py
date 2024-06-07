import telebot
import os
import google.generativeai as genai
from dotenv import load_dotenv
import markdown
# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
  "temperature": 0.75,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,

  system_instruction="AI Assistant is tasked with providing accurate, high-quality, and expertly written responses. The key objectives are to be informative and logical, actionable and well-formatted, positive, interesting, entertaining, and engaging, while also being short, crisp, and noteworthy. The assistant will use emojis and bulleted text when necessary and provide links to related topics and messages like Tony Stark.",
)


# Initialize the Telegram bot
bot = telebot.TeleBot("7127850802:AAEC_6AEltPVEoyeDuYXkTSSI2edCwrHGGc", parse_mode=None)
#profile photo

# Handle /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! I'm your friendly AI assistant. How can I help you today?")

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Get the user's message
    user_message = message.text
    
    # Create a chat session with the Generative AI model
    chat_session = model.start_chat(history=[{"role": "user", "parts": [user_message]}])
    
    # Get the AI's response
    response = chat_session.send_message(user_message)
    for chunk in response:
         bot.reply_to(message,chunk.text)

# Start the bot
bot.infinity_polling()
