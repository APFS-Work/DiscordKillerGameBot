from random import choice
import discord
import responses
import Game
import asyncio
from discord.ext import commands

#ctx is the context that contatin channel\author and other stuff , stringMessage is the string
async def send_message(textChannel:discord.TextChannel, stringMessage:str, is_TTS:bool, emb:discord.Embed):
    try:
        if emb != None:
            await textChannel.send(stringMessage, tts = is_TTS, embed = emb)
        else:
            await textChannel.send(stringMessage, tts = is_TTS)
    except Exception as e:
        print(e)

async def send_private_message(user:discord.User, stringMessage, is_TTS):
    try:
        await user.send(stringMessage, tts = is_TTS)
    except Exception as e:
        print(e)

async def send_temp_message(textChannel:discord.TextChannel, stringMessage:str, is_TTS:bool, emb:discord.Embed, timeOut:int):
    try:
        msg:discord.Message = None
        if emb != None:
            msg = await textChannel.send(stringMessage, tts = is_TTS, embed = emb)
        else:
            msg = await textChannel.send(stringMessage, tts = is_TTS)
        await asyncio.sleep(timeOut)
        await msg.delete()
    except Exception as e:
        print(e)

currentGame:Game.KillerGame = None
currentChannel:discord.TextChannel = None
currentGuild:discord.Guild = None

def  run_discord_bot():
    #TOKEN = 
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.typing = True
    intents.members = True
    intents.reactions = True
    bot = commands.Bot(command_prefix = '/', intents = intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.command(pass_context = True)
    async def killer(context, arg):
        print(f"process command : '{arg}'")

        currentGuild = context.guild

        try:
            spStr = context.message.content.replace("/killer ", "")
            print(f"split  message : {spStr}")
            tempTuple = responses.handle_command(context.author, context.message.channel, spStr)
            print(tempTuple)
            stringReturn = tempTuple[0]
            isTTS = bool(tempTuple[1])
            isPrivate = bool(tempTuple[2])
            em = tempTuple[3]

            if currentGame == None:
                print("current game is none")

            if isPrivate == False:                
                print(f"string return  :  {stringReturn['s']}")
                await send_message(context.channel, str(stringReturn['s']), is_TTS = isTTS, emb = em)
            else:
                for x in stringReturn.keys():
                    use = None
                    for a in currentGuild.members:
                        if a.id == int(x):
                            use = a
                            break      

                    await send_private_message(user = use, stringMessage = str(stringReturn[int(x)]), is_TTS = isTTS)

                if len(stringReturn) == len(currentGame.pID):
                    print("It   should  be   a    start    game    message")
                    await send_message(context.channel, str("倒數開始"), is_TTS = True, emb = None)
        except :
            await send_message(context.channel, "無效的指令", False)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            
            await responses.handle_CallBack(message)

            return

        await bot.process_commands(message)

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: ' {user_message} ' ({channel})")

        if user_message == "poll123":
            await startPoll(ti = "test Poll Title", descri = "test poll descri \n one \n two \n three" + get_emoji(0), choice = 11,timeOut = 10)
            
    @bot.event
    async def on_reaction_add(react:discord.Reaction, user:discord.User):
        print(user.name + "   add reaction  ")
        await responses.handle_dayTimePoll(rea = react, use = user)

    @bot.event
    async def on_reaction_clear(messag:discord.Message, reactions:list):
        print(str(len(reactions)) + "   Reaction deleted")
        await currentGame.receivePollResult(msg = messag, reactList = reactions)

    bot.run(TOKEN)




#template
#await startPoll(ti = "test Poll Title", descri = "test poll descri \n one \n two \n three", choice = 11,timeOut = 10)
# timeOut = -1 to not delete
async def startPoll(ti:str, descri:str, choice:int,timeOut:int):
    emb = discord.Embed(title = ti, description = descri)
    msg = await currentChannel.send(embed = emb)

    for a in range(choice):
        await msg.add_reaction(get_emoji(a))

    if ti == "晨間投票":
        currentGame.currentPoll = msg

    if timeOut == -1:
        return

    for x in range(timeOut):
        y = timeOut - x
        await asyncio.sleep(1)
    await msg.clear_reactions()



def get_emoji(intID:int) -> str:
    match intID:
            case 0:
                return "0️⃣"
            case 1:
                return "1️⃣"
            case 2:
                return "2️⃣"
            case 3:
                return "3️⃣"
            case 4:
                return "4️⃣"
            case 5:
                return "5️⃣"
            case 6:
                return "6️⃣"
            case 7:
                return "7️⃣"
            case 8:
                return "8️⃣"
            case 9:
                return "9️⃣"
            case 10:
                return "🔟"



#0️⃣
#1️⃣
#2️⃣
#3️⃣
#4️⃣
#5️⃣
#6️⃣
#7️⃣
#8️⃣
#9️⃣
#🔟