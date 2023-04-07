import os
import discord
import requests
from dotenv import load_dotenv

# load env file, and get the discord token and gif endpoint
load_dotenv()
discord_token = os.getenv('DISCORD_BOT_TOKEN')
GIF_ENDPOINT = os.getenv("GIF_ENDPOINT")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
#intents.threads = True
client = discord.Client(intents=intents)

# make a printdebugging function to print the string passed to the function. 
# The function should also check for the DEBUG environment variable and only print if it is set to true.
def printdebug(string):
    if os.getenv('DEBUG') == "true":
        # print DEBUG: before the string
        print("DEBUG: " + string)

# function to print the string passed to the function with INFO: before the string
def info(string):
    print("INFO: " + string)

# function to print the string passed to the function with warn: before the string
def warn(string):
    print("WARN: " + string)

# function to print the string passed to the function with ERROR: before the string
def die(string):
    print("ERROR: " + string)
    exit(1)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    printdebug(f"Received message: {message.content}")

    # Respond with an online message if the message is the @ the bot user and !online
    if message.content == f"<@{client.user.id}> !online":
        await message.channel.send("I am online and receiving messages!")
        return

    # 

    # Handle gifbot command
    if message.content.startswith(f"<@{client.user.id}> "):
        # Extract the GIF filename from the message content
        gif_filename = message.content.replace(f"<@{client.user.id}> ", "")

        # Print the filename for debugging purposes
        printdebug(f"GIF filename: {gif_filename}")

        # Generate the GIF URL based on the filename
        gif_url = f"https://gifs.techup.dev/{gif_filename}"
        printdebug(f"GIF URL: {gif_url}")

        # Download the GIF file to a temporary file on the server with the original filename
        response = requests.get(gif_url)

        # Check if the response code is in the 2xx range
        if response.status_code >= 200 and response.status_code < 300:
            with open(gif_filename, "wb") as f:
                f.write(response.content)

            # Send the GIF as an attachment
            await message.channel.send(file=discord.File(gif_filename))

            # Delete the temporary file
            os.remove(gif_filename)
        else:
            warn(f"Received status code {response.status_code} for URL: {gif_url}")
            await message.channel.send(f"Sorry, I couldn't find a GIF with the name {gif_filename}.")



client.run(discord_token)
