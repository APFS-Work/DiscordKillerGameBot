from enum import Enum
import discord
import random
import bot

class KillerGame():
    #int players ID, discord.User user
    pID = {}
    #int players ID, string occupation
    pOccu = {}
    #int players ID, bool is dead
    pIsDead = {}
    #int players ID, discord.User user die at this night
    pDieThisNight = {}

    allOccupation = {
         "平民" : 0,
         "殺手" : 0,
         "警察"  : 0,
        }

    day = 0
    isNight = False

    #the ongoing poll  just for daytime poll
    currentPoll:discord.Message = None
    

    #reset the whole game
    def reset(self):
        self.pID = {}
        self.pOccu = {}
        self.pIsDead = {}
        self.allOccupation = {
        "平民" : 0,
        "殺手" : 0,
        "警察" : 0,
        }
        self.day = 0
        self.isNight = False

    #register the client
    def register(self, user:discord.User) -> bool:
        if (bot.currentGame == None):
            raise Exception("未創建遊戲")
        if (self.pID.__contains__(user.id) == False):
            self.pID[user.id] = user
            return True
        else:
            return False

    #remove register of the client
    def removeRegister(self, user:discord.User) -> bool:
        if self.pID.__contains__(user.id) == True:
            self.pID.pop(user.id)
            return True
        else:
            return False

    #set the amounts of each occupation
    def set_OccupationNumbers(self, occupation, numbers):
        self.allOccupation[occupation] = numbers

    #check the current occupation settin
    def checkSetting(self) -> str:
        outString = ""
        for y in self.allOccupation.keys():
            outString += str(y) + " : "
            outString += str(self.allOccupation[y]) + "\n"

        print("break here 0")
        outString += str("\n")
        outString += str("已加入玩家 : \n")
        for z in self.pID.keys():
            outString += "`" + self.pID[z].name + " : "
            outString += str(z) + "`\n"
        print("break here 1")
        return outString

    #start the game
    def startGame(self) -> dict:
        tempOccuDict = self.allOccupation.copy()
        outPutDict = {}

        for y in self.pID.keys():
            
            self.pIsDead[int(y)] = False

            while True:
                currentKey = list(tempOccuDict)[random.randint(0, len(tempOccuDict) - 1)]
                if tempOccuDict[currentKey] > 0:
                    self.pOccu[y] = currentKey
                    tempOccuDict[currentKey] -= 1
                    outPutDict[y] = "你是" + str(currentKey)
                    break

        return outPutDict

    #get list of alive player [int id] [discord.User user]
    def getAlivePlayer(self) -> dict:
        tempDict = {}

        for x in self.pIsDead.keys():
            if self.pIsDead[x] == False:
                tempDict[x] = self.pID[x]


        print(str(len(tempDict)) + "         人未死")
        return tempDict

    #return good if the occupation of the player is good
    def determineIsGood(self, user:discord.User) -> bool:
        occu = self.pOccu[user.id]
        if occu == "殺手":
            return False
        else:
            return True

    #return true if good guys win   return  false if bad guys win      raise exception  not end if game is not end
    def checkEndGame(self) -> bool:
        alivePlayers = self.getAlivePlayer()

        goodCounts:int = 0
        badCounts:int = 0
        
        for p in alivePlayers.values():
            if self.determineIsGood(user = p) == True:
                goodCounts += int(1)
            else:
                badCounts += int(1)

        if badCounts >= goodCounts:
            return False

        if badCounts == int(0):
            return True

        raise Exception("遊戲未完結")

    #receive poll result
    async def receivePollResult(self, msg:discord.Message, reactList:list):
        titleOfPoll = ""
        emb = None
        #[int userID][int count]
        resultDict = {}

        for x in msg.embeds:
            emb:discord.Embed = x
            titleOfPoll = emb.title
            break

        if titleOfPoll == "晨間投票":
            return

        ind:int = 0
        for y in emb.description.splitlines():
            #0 emoji 1 : 2 id 3 display_name 4 name
            resultDict[int(y.split()[2])] = int(reactList[ind].count)
            print (str(ind) + "  have     " + str(reactList[ind].count))
            ind += int(1)

        if titleOfPoll == "殺手投票":
            mostVote:int = 0
            mostVoteKey:int = 0
            for z in resultDict.keys():
                if resultDict[z] > mostVote:
                    mostVoteKey = z
                    mostVote = resultDict[z]

            if mostVote <= int(1):
                print("殺手      沒有     投票")
            else:
                tempUser:discord.User = self.pID[mostVoteKey]
                self.pDieThisNight[tempUser.id] = tempUser

        if titleOfPoll == "警察投票":
            mostVote = int(0)
            mostVoteKey:int = 0
            for z in resultDict.keys():
                if resultDict[z] > mostVote:
                    mostVoteKey = z
                    mostVote = resultDict[z]

            if mostVote <= int(1):
                print("警察      沒有     投票")
                await bot.send_temp_message(bot.currentChannel,stringMessage = str("投票不成立") ,is_TTS = False , emb = None , timeOut = 10)
            else:
                tempUser:discord.User = self.pID[mostVoteKey]
                await bot.send_temp_message(bot.currentChannel,stringMessage = str(tempUser.display_name) + str("是") + str(self.pOccu[tempUser.id]) ,is_TTS = False , emb = None , timeOut = 10)


           