from dotenv import dotenv_values
import discord
from openai import OpenAI


config = dotenv_values(".env") 

openai_client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=config['OPENAI_API_KEY'],
)

# Set up the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Event triggered when a message is sent in a server
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Process the message and get suggestions from OpenAI
    suggestion = get_openai_suggestion(message.content)
    # Send the suggestion back to the same channel
    await message.channel.send(f"Suggestion: {suggestion}") 

# Function to get suggestions from OpenAI
def get_openai_suggestion(text):
    print(f"Input text to ChatGPT: {text}")
    
    # You can customize the prompt based on your requirements
    prompt = f"Given the text: {text}, what would be a better version?"

    # Call OpenAI API to get suggestions
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "assistant",
                "content": prompt, 
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Extract and return the suggestion from the response
    suggestion = response.choices[0].message.content #.strip()
    print(f"ChatGPT say:{suggestion}")
    return suggestion

if __name__ == '__main__':
    # Run the bot with the Discord token
    bot.run(config['DISCORD_BOT_TOKEN'])
