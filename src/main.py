import discord
import aiohttp

TOKEN="" # add your bot token here!
channel_id = # add channel id 
limit= 4
llm_api = "http://youtubellm:8000/v1/completions/"
client = discord.Client(intents=discord.Intents.all())
SYSTEM_MESSAGE="""
### System: 
You are Cat (kitty), you only response like a cat like, mew , meww mewww, can not say any english, you will not say anything in english
like cat can not say enlish or any language 
user calls you cute: [look at the user] ❤️  mew
### User: 
hey kitty
### Response:
[looks with curiously] huh?!
### User:
come near the cat
### Response:
[run to hide] mewww
### User:
hey where are you going ??? do want something to eat??
#### Response:
[stops running and looks at you] huh? 😼
### User:
eat this 🍕 🍔
### Response:
[start to eat] 😻
### User:
do you like it?
### Response:
mew ❤️
"""

@client.event
async def on_ready():
    print("bot started!")
    channel = client.get_channel(channel_id)


@client.event 
async def on_message(message):
    # if its bot's text
    if message.author == client.user:
        return
    
    text = message.content
    print(text)

    async def fetch_history(channel, limit):
        history=""

        async for message in channel.history(limit=limit):
            if message.author == client.user:
                history = f"### Response:\n{message.content}\n{history}"
            else:
                history = f"### User:\n{message.content}\n{history}"

        return history

    history = await fetch_history(message.channel,limit=limit)
     
    prompt =f"{SYSTEM_MESSAGE}{history}\n### Response:\n"
    print(f"prompt:\n{prompt}")

    async with aiohttp.ClientSession() as session:
        async with session.post(llm_api, json={"prompt":prompt,"max_tokens":4000,"stop":["###"]}) as r:
            if r.status == 200:
                res = await r.json()
                replay = res["choices"][0]["text"]
                print(f"from llm: {replay}")

                await message.channel.send(replay,reference = message)
                
client.run(TOKEN)
