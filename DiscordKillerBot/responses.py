from random import choice
import discord
import Game
import bot
import asyncio

#cli for client, com for command
#return string for message, bool for is TTS messge, bool for is private
def handle_command(user:discord.User, textChannel:discord.TextChannel, com:str) -> tuple:
    c = com.split()[0]
    game = bot.currentGame
    if c == 'help':
        tempStr = "/killer create     :     創建遊戲\n" + "/killer set 職業 數量     :     設定遊戲\n" + "/killer check     :     查看設定及已加入玩家\n" + "/killer register     :     加入遊戲\n" + "/killer unregister     :     離開遊戲\n" + "/killer start     :     開始遊戲\n"
        return tuple((dict(s = ""), False, False, discord.Embed(title = "指令", description = tempStr)))
    elif c == 'create':
        bot.currentGame = Game.KillerGame()
        bot.currentChannel = textChannel
        return tuple((dict(s = "`已創建遊戲 輸入 : /killer set 職業 數量 以設定遊戲`\n" + "請將使用者設定 -> 通知- > 文字朗讀通知設為 '永不' "), False, False, None))
    elif c == 'set':
        if game.pID.__contains__(user.id) == False:
            return tuple((dict(s = "請先加入遊戲後才開始設定"), False, False, None))

        splitedText = str(com.split()[1])

        if game.allOccupation.__contains__(splitedText) == False:
            return tuple((dict(s = "不存在職業"), False, False, None))

        try:
           count = int(com.split()[2])
           game.set_OccupationNumbers(splitedText, count)
           return tuple((dict(s = "`已將" + splitedText + "設定為" + str(count) + "`"), False, False, None))
        except:
            return tuple((dict(s = "數量錯誤"), False, False, None))
    elif c == 'check':
        try:
            return tuple((dict(s = str(game.checkSetting())), False, False, None))
        except:
            return tuple((dict(s = str(f"`未創建遊戲`")), False, False, None))
    elif c == 'register':
        try: 
            if(game.register(user)):
                return tuple((dict(s = str(f"`{user.name}  ID: {user.id}   已 >加入< 遊戲`")), False, False, None))
            else:
                return tuple((dict(s = str(f"`{user.name}  ID: {user.id}   >未能< 加入遊戲   (可能因為你已加入遊戲)`")), False, False, None))
        except:
            return tuple((dict(s = str(f"`未創建遊戲`")), False, False, None))
    elif c == 'unregister':
        try:
            if(game.removeRegister(user)):
                return tuple((dict(s = str(f"`{user.name}  ID: {user.id}   已 >離開< 遊戲`")), False, False, None))
            else:
                return tuple((dict(s = str(f"`{user.name}  ID: {user.id}   >未能< 離開遊戲   (可能因為你尚未加入遊戲)`")), False, False, None))
        except :
            return tuple((dict(s = str(f"`未創建遊戲`")), False, False, None))
    elif c == 'start':
        try:
            totalNumberOfOccupation = int(0)
            for x in game.allOccupation.values():
                totalNumberOfOccupation += int(x)

            if totalNumberOfOccupation != len(game.pID): 
                return tuple((dict(s = str("`遊戲人數與職業數量不符`")), False, False, None))
            
            return tuple((game.startGame(), False, True, None))
        except:
            return tuple((dict(s = str(f"`未創建遊戲`")), False, False, None))
    else:
        print("OTHER SITUATION")



async def handle_CallBack(message):
    con = message.content
    if con == "倒數開始":
        for x in range(10):
            y = 10 - x
            await bot.send_message(bot.currentChannel, str(y), is_TTS = False, emb = None)
            await asyncio.sleep(1)
        await bot.send_message(bot.currentChannel, str("遊戲開始"), is_TTS = False, emb = None)
        await bot.send_message(bot.currentChannel, str("天黑請閉眼"), is_TTS = True, emb = None)

    if con == "天黑請閉眼":
        bot.currentGame.isNight = True
        await asyncio.sleep(5)
        await bot.send_message(bot.currentChannel, str("殺手請開眼"), is_TTS = True, emb = None)
        pollStr = ""
        alivePlayerDict = bot.currentGame.getAlivePlayer()
        ind:int = 0
        for x in alivePlayerDict.keys():
            tempP:discord.User = alivePlayerDict[x]
            pollStr += bot.get_emoji(ind) + " : " + str(tempP.id) + "       " + tempP.display_name + "       " + tempP.name
            pollStr += "\n"
            ind += 1
        await bot.startPoll(ti = "殺手投票", descri = pollStr, choice = len(alivePlayerDict), timeOut = 15)
        await bot.send_message(bot.currentChannel, "殺手請閉眼", is_TTS = True, emb = None)

    if con == "殺手請閉眼":
        await asyncio.sleep(5)
        await bot.send_message(bot.currentChannel, str("警察請開眼"), is_TTS = True, emb = None)
        pollStr = ""
        alivePlayerDict = bot.currentGame.getAlivePlayer()
        ind:int = 0
        for x in alivePlayerDict.keys():
            tempP:discord.User = alivePlayerDict[x]
            pollStr += bot.get_emoji(ind) + " : " + str(tempP.id) + "       " + tempP.display_name + "       " + tempP.name
            pollStr += "\n"
            ind += 1
        await bot.startPoll(ti = "警察投票", descri = pollStr, choice = len(alivePlayerDict), timeOut = 15)
        await asyncio.sleep(13) 
        await bot.send_message(bot.currentChannel, "警察請閉眼", is_TTS = True, emb = None)

    if con == "警察請閉眼":
        await asyncio.sleep(5)
        await bot.send_message(bot.currentChannel, str("天光請開眼"), is_TTS = True, emb = None)
        #region day setting
        bot.currentGame.isNight = False
        bot.currentGame.day += 1
        for a in bot.currentGame.pDieThisNight.values():
            bot.currentGame.pIsDead[a.id] = True
            await bot.send_message(bot.currentChannel, a.display_name + "    " + a.name + "    已死亡", is_TTS = True, emb = None)
        bot.currentGame.pDieThisNight = {}
        #endregion

        try:
            isGoodWin = bot.currentGame.checkEndGame()
            if isGoodWin == True:
                await bot.send_message(bot.currentChannel, str("遊戲結束    好人陣營勝出"), is_TTS = True, emb = None)
            else:
                await bot.send_message(bot.currentChannel, str("遊戲結束    壞人陣營勝出"), is_TTS = True, emb = None)
        except Exception as ex:
            print(ex)

            pollStr = ""
            alivePlayerDict = bot.currentGame.getAlivePlayer()
            ind:int = 0
            for x in alivePlayerDict.keys():
                tempP = alivePlayerDict[x]
                pollStr += bot.get_emoji(ind) + " : " + str(tempP.id) + "       " + tempP.display_name + "       " + tempP.name
                pollStr += "\n"
                ind += 1
            pollStr += bot.get_emoji(ind) + " : " + "    跳過白天    "
            await bot.startPoll(ti = "晨間投票", descri = pollStr, choice = len(alivePlayerDict) + int(1), timeOut = -1)
            
async def handle_dayTimePoll(rea:discord.Reaction, use:discord.User):
    msg:discord.Message = rea.message

    if msg.embeds[0].title != "晨間投票":
        return

    bot.currentGame.currentPoll = msg

    totalCount:int = int(0)
    maxVote:int = int(1)
    maxVoteReaction:discord.Reaction = None

    alivePlayerDict:dict = bot.currentGame.getAlivePlayer()

    for x in msg.reactions:
        totalCount += (x.count - int(1))
        if x.count > maxVote:
            maxVote = x.count
            maxVoteReaction = x

    if totalCount < len(bot.currentGame.pID):
        return

    await bot.send_message(bot.currentChannel, str("晨間投票結束"), is_TTS = True, emb = None)

    if msg.reactions.index(maxVoteReaction) == len(alivePlayerDict):
        await bot.send_message(bot.currentChannel, str("投票結果為跳過白天"), is_TTS = True, emb = None)
    elif  msg.reactions.index(maxVoteReaction) < len(alivePlayerDict):
        userDie:discord.User = list(alivePlayerDict.values())[int(msg.reactions.index(maxVoteReaction))]       
        bot.currentGame.pIsDead[userDie.id] = True
        await bot.send_message(bot.currentChannel, str("投票結果為 ") + userDie.display_name + "    " + userDie.name  + "  被投票殺死", is_TTS = True, emb = None)

    await bot.currentGame.currentPoll.clear_reactions()
    await asyncio.sleep(15)

    try:
        isGoodWin = bot.currentGame.checkEndGame()
        if isGoodWin == True:
            await bot.send_message(bot.currentChannel, str("遊戲結束    好人陣營勝出"), is_TTS = True, emb = None)
        else:
            await bot.send_message(bot.currentChannel, str("遊戲結束    壞人陣營勝出"), is_TTS = True, emb = None)
    except Exception as ex:
        print(ex)

        await bot.send_message(bot.currentChannel, str("天黑請閉眼"), is_TTS = True, emb = None)

        await asyncio.sleep(5)


    


def handle_response(message) -> str:
    p_message = message.content.lower()

    if  p_message == 'hello':
        return 'Hey there!'

    if p_message == 'roll':
        return '/tts ' + str(5)

    if p_message == '!help':
        return "`This is a help message that you can modify`"


    return "I don't know what you said"