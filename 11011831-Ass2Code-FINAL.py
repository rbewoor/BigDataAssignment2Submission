import pandas as pd
import random
global globalNumberOfCharacteritics
global globalIpFileTrumpCardsData

globalNumberOfCharacteritics = 6
globalIpFileTrumpCardsData = "D:/EverythingD/01SRH-BDBA Acads/Blk6-BigDataProg1/Ass2/CardsSetupData.txt"
# 
##############################################################################################################
#
# Please create a .TXT file with comma separated values and specify its location in the global variable above
# Input data for 10 cards with 6 charactersitics - pick up with the header row.
# The file lines are enclosed between the three apostrophe marked lines
#
'''
RatingSc,ActingSc,StorySc,OriginalitySc,PositiveReviews,Budget,Movie,CardNo
8.2,7.8,8.94,8.8,45,1.55,Primer,1
5.5,8.25,8.4,7.6,68,2.56,TheMist,2
7.55,8.75,8.7,7.75,94,1.45,Oculus,3
8.89,9.75,9.2,9.42,115,14.5,Seven,4
9.34,9.72,8.65,8.12,190,18.56,BicentennialMan,5
9.14,9.52,7.95,8.32,164,57.67,ApocalypseNow,6
9.34,9.48,8.15,9.32,267,7.56,She,7
3.54,5.57,4.55,2.32,156,69.42,TigerZindaHai,8
7.97,9.09,8.66,8.63,36,12.34,TheThing,9
9.24,9.28,9.15,9.59,182,38.92,BladeRunner,10
'''
# 
##############################################################################################################
# 
# For all characteristics, while comparing characteristics to decide winning card, a higher value always wins
# RatingSc, ActingSc, StorySc, OriginalitySc, PositiveReviews, Budget are the 6 characteristics.
# Topmost card in a deck is referred to as position 0.
# 
##############################################################################################################
class cTrumpCard:
#   #####
    def __init__(self):
        self.name = ""
        self.characteristics = []
#   #####
    def add_characteristic(self, charName, charValue):
        self.characteristics.append({charName: charValue})
#   #####
    def extract_characteristic(self, charReq):
        for ele in self.characteristics:
            for key, value in ele.items():
                if (charReq == key):
                    return(True, charReq, value)
        return (False, charReq, "GarbageValue")
#   #####    
    def displayCardToConsoleClassCardMethod(self):
        sNum = 0
        print(f"Card name: {self.name}")
        for idx in range(0, globalNumberOfCharacteritics ):
            for key, value in self.characteristics[idx].items():
                print(f"SN = {sNum}\t::\tCharacteristic = {key}\t::\tValue = {value}")
                sNum += 1
#   #####
#####################################
class cDeckOfCards:
#   #####
    def __init__(self):
        self.deckName = ""
        self.cardsInDeck = []
        self.countOfCardsInDeck = 0
#   #####
    def shuffleDeck(self):
        random.shuffle(self.cardsInDeck)
#   #####
    def distributeCardsToPlayers(self, p1, p2):
        ''' Shuffle the full deck first. Then distribute the cards to the two player objects p1 and p2 player equally '''
        self.shuffleDeck()
        for idx in range(0, self.countOfCardsInDeck, 2):
            p1.playerDeck.addCardToDeckAtTop(self.cardsInDeck[idx])
            p2.playerDeck.addCardToDeckAtTop(self.cardsInDeck[idx + 1])
        p1.playerDeck.countOfCardsInDeck = p2.playerDeck.countOfCardsInDeck = int(self.countOfCardsInDeck / 2)
        return (p1, p2)
#   #####
    def removeTopCardFromDeck(self):
        ''' Remove the card at the top of the deck and return the card; Position=0 means top of the deck '''
        self.countOfCardsInDeck -= 1
        return( self.cardsInDeck.pop(0) )
#   #####
    def removeSpecificPositionCardFromDeck(self, cardPos2Remove):
        ''' Remove the card at the position specified by cardPos2Remove parameter and return the card; Position=0 means top of the deck '''
        self.countOfCardsInDeck -= 1
        return( self.cardsInDeck.pop(cardPos2Remove) )       
#   #####
    def addCardToDeckAtTop(self, cardToAdd):
        ''' Will add to the top of deck i.e. position indexed by 0 '''
        self.cardsInDeck.insert(0, cardToAdd)
        self.countOfCardsInDeck += 1
#####################################
class cPlayer:
#   #####
    def __init__(self, playerName):
        self.points = 0
        self.playerName = playerName
        self.playerDeck = cDeckOfCards()
        self.flagUsedGodSpell = False
        self.flagUsedResurrectSpell = False
#   #####
    def rollDiceOnce(self):
        return( random.choice([1, 2, 3, 4, 5, 6]) )
#   #####    
    def displayFullCardToConsoleClassPlayerMethod(self, posNo):
        sNum = 0
        print(f"\nCard at {posNo} th position in {self.playerName}'s deck:")
        print(f"Card name:: {self.playerDeck.cardsInDeck[posNo].name}")
        for idx in range(0, globalNumberOfCharacteritics ):
            for key, value in self.playerDeck.cardsInDeck[posNo].characteristics[idx].items():
                print(f"SN = {sNum}\t::\tCharacteristic = {key}\t::\tValue = {value}")
                sNum += 1
        return
#   #####
    def showCardAndTakeInputForCharacteristicToBePlayedInRound(self, posNo):
        ''' Show the card at topmost position. Acccept and validate the characteristic to be played in round '''
        self.displayFullCardToConsoleClassPlayerMethod(0)    # show the card details for the topmost card
        messageToShow = "\nWhat characteristic do you want to play?\nEnter number from 0 to %d:\nYour choice: " %(globalNumberOfCharacteritics-1)
        validValuesList = list(range(globalNumberOfCharacteritics))
        choiceCharSerNum = getActualInputAndCheckValidity(validValuesList, messageToShow)
        keyValuePairTuple = list( self.playerDeck.cardsInDeck[posNo].characteristics[choiceCharSerNum].items() )
        charChosenName = keyValuePairTuple[0][0]
        return charChosenName, choiceCharSerNum
#   #####
    def showRoundOptionsAndInputPlayersSelection(self, playerTypeWinnerFlag, oOutdatedDeck, winnerChoiceSelection = 100):
        '''
        Actions done by this function:
            1) Displays the options available to the player based on whether:
                a) whether the player is the starting or second player (calling parameters specify this)
                b) spells not played and still available
                c) whether Outdated deck has cards in it to allow Resurrect spell to be played
                d) if God/ Resurrect selected, then sets the Usage Flag to False in the player object properties
            2) Validates the input and asks to re-enter if invalid inputs.
        Calling parameters explanation:
            To show options for the Winner i.e. person starting the round
                    call(self, True, Outdateddeck)      Note: Omit winnerChoiceSelection parameter, will be ignored anyway
            To show options for the Loser i.e. person playing second in the round
                    call(self, False, Outdateddeck, <Winnners Choice of Playtype>)
        Returns:
            The choice of play type selected by the player
        Allowed choices for game play, with check that the spells can only be invoked once by each player:
            Winner = 1(Regular)   followed by Loser = 1(Regular)
            Winner = 1(Regular)   followed by Loser = 1(Resurrect)
            Winner = 2(God)       followed by Loser = 1(Regular)
            Winner = 2(God)       followed by Loser = 1(Resurrect)
            Winner = 3(Resurrect) followed by Loser = 1(Regular)
            Winner = 3(Resurrect) followed by Loser = 1(Resurrect)
            Winner = <anything>   followed by Loser = <God> is NOT ALLOWED
        '''
        if playerTypeWinnerFlag == True: # winning players choice selection logic
            if self.flagUsedGodSpell == False and self.flagUsedResurrectSpell == False and oOutdatedDeck.countOfCardsInDeck > 0:
                # both spells are NOT USED, also Outdated Deck must not be empty
                messageToShow = "Enter Round play Type: RegularMode = 1, GodSpell = 2, Resurrect = 3\nYour Choice:: "
                validValuesList = [1, 2, 3]
                playTypeChoice = getActualInputAndCheckValidity(validValuesList, messageToShow)
            elif self.flagUsedGodSpell == False and self.flagUsedResurrectSpell == True:
                # Resurrect used already, God NOT used
                messageToShow = "Enter Round play Type: RegularMode = 1, GodSpell = 2\nYour Choice:: "
                validValuesList = [1, 2]
                playTypeChoice = getActualInputAndCheckValidity(validValuesList, messageToShow)
            elif self.flagUsedGodSpell == True and self.flagUsedResurrectSpell == False and oOutdatedDeck.countOfCardsInDeck > 0:
                # God spell used already, Resurrect NOT used and Outdated Deck is not empty
                messageToShow = "Enter Round play Type: RegularMode = 1, Resurrect = 3\nYour Choice:: "
                validValuesList = [1, 3]
                playTypeChoice = getActualInputAndCheckValidity(validValuesList, messageToShow)
            elif self.flagUsedGodSpell == True and self.flagUsedResurrectSpell == True:
                # both spells have been used already, so 1(Regular) is the only possible option now
                print(f"No spells remaining....your play type defaulted to REGULARmode")
                playTypeChoice = 1
            elif self.flagUsedGodSpell == False and self.flagUsedResurrectSpell == False and oOutdatedDeck.countOfCardsInDeck == 0:
                # both spells are NOT USED but its the first round so only Regular and GodSpell
                messageToShow = "Enter Round play Type: RegularMode = 1, GodSpell = 2\nYour Choice:: "
                validValuesList = [1, 2]
                playTypeChoice = getActualInputAndCheckValidity(validValuesList, messageToShow)
            else:
                print(f"EXITING program:: FATAL LOGIC ERROR - Winning player choice selection condition is accounted for.")
                exit(500)
        else:
            ### losing player's choice selection logic
            if winnerChoiceSelection == 100:
                print(f"EXITING program:: FATAL LOGIC ERROR - Losing players choice selection impossible without Winners Choice specified explicity.")
                exit(300)

            if self.flagUsedResurrectSpell == False and oOutdatedDeck.countOfCardsInDeck > 0:
                messageToShow = "Enter Round play Type: RegularMode = 1, Resurrect = 3\nYour Choice:: "
                validValuesList = [1, 3]
                playTypeChoice = getActualInputAndCheckValidity(validValuesList, messageToShow)
            else:
                # 1(Regular) is the only possible option now
                print(f"No spells remaining or no choice available....your play type defaulted to REGULARmode")
                playTypeChoice = 1
        # if any of the spells selected then update the spell flags to be ready for the next round evaluation
        if playTypeChoice == 2:
            self.flagUsedGodSpell = True
        elif playTypeChoice == 3:
            self.flagUsedResurrectSpell = True
        return (playTypeChoice)
#   #####
    def winningPlayerPlaysRESURRECT(self, oOutdatedDeck):
        winPlayerCharChosen = "Garbage"
        randomCardPosToGetFromOutDeck = random.choice(list(range(oOutdatedDeck.countOfCardsInDeck)))
        randomCardFromOutdeck = oOutdatedDeck.removeSpecificPositionCardFromDeck(randomCardPosToGetFromOutDeck)
        self.playerDeck.addCardToDeckAtTop(randomCardFromOutdeck)
        print(f"\nResurrected card from Outdeck and placed at top of players deck.")
        winPlayerCharChosen, charChosenIndexInCharArray = self.showCardAndTakeInputForCharacteristicToBePlayedInRound(0) # 0 to show the top card
        winnerCardToBeThrown = self.playerDeck.removeTopCardFromDeck()
        return (winPlayerCharChosen, charChosenIndexInCharArray, winnerCardToBeThrown, self)
#   #####
    def winningPlayerPlaysREGULAR(self):
        winPlayerCharChosen = "Garbage"
        winPlayerCharChosen, charChosenIndexInCharArray = self.showCardAndTakeInputForCharacteristicToBePlayedInRound(0) # 0 to show the top card
        winnerCardToBeThrown = self.playerDeck.removeTopCardFromDeck()
        return (winPlayerCharChosen, charChosenIndexInCharArray, winnerCardToBeThrown, self)
#   #####
    def winningPlayerPlaysGODSPELL(self, countOfCardsInLosingPlayerDeck):
        winPlayerCharChosen = "Garbage"
        winPlayerCharChosen, charChosenIndexInCharArray = self.showCardAndTakeInputForCharacteristicToBePlayedInRound(0) # 0 to show the top card
        winnerCardToBeThrown = self.playerDeck.removeTopCardFromDeck()
        messageToShow = "\nGod spell invoked. Which card position should opponent play?\nChoose a number between 0 and %d.\nYour choice:: " %(countOfCardsInLosingPlayerDeck-1)
        validValuesList = list(range(countOfCardsInLosingPlayerDeck))
        winPlayerChoice4Loser = getActualInputAndCheckValidity(validValuesList, messageToShow)
        return (winPlayerCharChosen, charChosenIndexInCharArray, winnerCardToBeThrown, self, winPlayerChoice4Loser)
#   #####
    def losingPlayerPlaysRESURRECTSpell(self, oOutdatedDeck):
        randomCardPosToGetFromOutDeck = random.choice(list(range(oOutdatedDeck.countOfCardsInDeck)))
        randomCardFromOutdeck = oOutdatedDeck.removeSpecificPositionCardFromDeck(randomCardPosToGetFromOutDeck)
        self.playerDeck.addCardToDeckAtTop(randomCardFromOutdeck)
        print(f"\nResurrected card from Outdeck and placed at top of players deck.")
        losingCardToBeThrown = self.playerDeck.removeTopCardFromDeck()
        return (losingCardToBeThrown, self)
#   #####
    def losingPlayerPlaysREGULAR(self):
        losingCardToBeThrown = self.playerDeck.removeTopCardFromDeck()
        return (losingCardToBeThrown, self)
#   #####
    def losingPlayerPlaysREGULARButWinningPlayerPlayedGodspell(self, winningPlayerCardChoice4LosingPlayerToThrow):
        losingCardToBeThrown = self.playerDeck.removeSpecificPositionCardFromDeck(winningPlayerCardChoice4LosingPlayerToThrow)
        return (losingCardToBeThrown, self)
#   #####
    def losingPlayerPlaysRESURRECTButWinningPlayerPlayedGodspell(self, oOutdatedDeck, winningPlayerCardChoice4LosingPlayerToThrow, winPlayerObject):
        randomCardPosToGetFromOutDeck = random.choice(list(range(oOutdatedDeck.countOfCardsInDeck)))
        randomCardFromOutdeck = oOutdatedDeck.removeSpecificPositionCardFromDeck(randomCardPosToGetFromOutDeck)
        self.playerDeck.addCardToDeckAtTop(randomCardFromOutdeck)
        print(f"\nResurrected card from Outdeck and placed at top of players deck.")
        print(f"\nGodSpell was invoked by the Winning player....option to change card....")
        print(f"\n{winPlayerObject.playerName}, your original chosen card position was {winningPlayerCardChoice4LosingPlayerToThrow}.\nDo you want to change the card for opponent to throw?")
        newChoiceDecision = input(f"Press 1 to CHANGE to resurrected card....or ANY OTHER KEY to retain your original choice.\nYour Choice:: ")
        if newChoiceDecision.isdigit():
            newChoiceDecision = int(newChoiceDecision)
            if newChoiceDecision == 1:
                winningPlayerCardChoice4LosingPlayerToThrow = 0
            else:
                winningPlayerCardChoice4LosingPlayerToThrow += 1  # after adding the resurrected card the index is up by one
        else:
            winningPlayerCardChoice4LosingPlayerToThrow += 1  # after adding the resurrected card the index is up by one

        losingCardToBeThrown = self.playerDeck.removeSpecificPositionCardFromDeck(winningPlayerCardChoice4LosingPlayerToThrow)
        return (losingCardToBeThrown, self)
#####################################
def getActualInputAndCheckValidity(allowedValuesList, entryInstructionMessage):
    playChoice = 0
    validFlag = False
    while validFlag == False:
        playChoice = input(entryInstructionMessage)
        if playChoice.isdigit():
            playChoice = int(playChoice)
            for value in allowedValuesList:
                if value == playChoice:
                    validFlag = True
                    break
        if validFlag == False:
            print(f"\nInvalid value entered...")
    return(playChoice)
#####################################
def decideWinnerByDiceRoll(p1, p2):
    p1RollValue = p2RollValue = 0
    print("\nBoth players to throw dice now to decide who will start the round.\n")
    while p1RollValue == p2RollValue:
        input(f"{p1.playerName}, please press any key to roll die")
        p1RollValue = p1.rollDiceOnce()
        print(f"{p1.playerName} rolled {p1RollValue} on dice throw\n")
        input(f"{p2.playerName}, please press any key to roll die")
        p2RollValue = p2.rollDiceOnce()
        print(f"{p2.playerName} rolled {p2RollValue} on dice throw\n")
        if p1RollValue == p2RollValue:
            print(f"\nBoth rolled same value, need to roll AGAIN...\n")
    if p1RollValue > p2RollValue:
        print(f"\nPlayer 1, {p1.playerName}, you have won dice round and will start the game. Good luck both of you!")
        return(1)
    else:
        print(f"\nPlayer 2, {p2.playerName}, you have won dice round and will start the game. Good luck both of you!")
        return(2)
#####################################
def performInitialSetupForGame():
    ''' Actions performed related to initial setup for the game:
    #       a) Reads the trump card data from the input file and creates an AllCards Deck
    #       b) Input the players names and creates objects of class Player
    #       c) calls the function for dice rolling to decide the starting player
    # returns: (the undealt deck of cards as object, player 1 object, player 2 object)
    '''
    try:
        # note that globalIpFileTrumpCardsData is a global variable defined at the top of the program
        ipFileData = pd.read_csv(globalIpFileTrumpCardsData, sep=",")
    except:
        print(f'\nEXITING program:: FATAL ERROR - Input data file for setup of trump cards not found at location :: ' + '"' + globalIpFileTrumpCardsData + '"')
        print(f"Please check the input file location specified in global variable <<globalIpFileTrumpCardsData>> at start of the program.\n")
        exit(100)
    oOutdatedDeck = cDeckOfCards()
    oOutdatedDeck.deckName = "OutdatedDeck"
    oAllCardsDeck = cDeckOfCards()
    oAllCardsDeck.deckName="AllCardsDeck"
    for rowIdx, rowData in ipFileData.iterrows():
        # create a new TrumpCard and assign the values
        tempCard = cTrumpCard()
        tempCard.name = rowData["Movie"]
        # note that globalNumberOfCharacteritics is global variable defined at top of program
        for colIdx in range(globalNumberOfCharacteritics):
            tempCard.add_characteristic(ipFileData.columns[colIdx], rowData[colIdx])
        oAllCardsDeck.addCardToDeckAtTop(tempCard)  # add the newly created card to the top of the deck
    if ( oAllCardsDeck.countOfCardsInDeck % 2 ) == 1:
        print(f"EXITING program:: FATAL DATA ERROR - Input data file has ODD data rows for trump cards. Unable to distribute cards evenly to both players.")
        exit(200)
    
    player1Name = input("Please enter name of Player 1:\n")
    player2Name = input("\nPlease enter name of Player 2:\n")
    oPlayer1 = cPlayer(player1Name)
    oPlayer1.playerDeck.deckName="Player1CardsDeck"
    oPlayer2 = cPlayer(player2Name)
    oPlayer2.playerDeck.deckName="Player2CardsDeck"

    winnerFlag = decideWinnerByDiceRoll(oPlayer1, oPlayer2)     # will be set to 1 if player 1 wins dice roll, else 2 for player 2
    oPlayer1, oPlayer2 = oAllCardsDeck.distributeCardsToPlayers(oPlayer1, oPlayer2)

    return(oAllCardsDeck, oPlayer1, oPlayer2, winnerFlag, oOutdatedDeck)
#####################################
def compareCharacteristicsBetweenCards(winningCardThrown, losingCardThrown, characteristicChosen4Comparison):
    ''' Takes the two cards from the winning player and the losing player.
        Using the characteristic specified, compares the values on these cards and indicates which card has higher value.
    Returns:
        Result: indicates who won or if there was some error condition detected
        winCardCharValue: value of the characteristic for the winning card
        loseCardCharValue: value of the characteristic for the losing card
    Result variable - possible values:
        1:   if the winningCardThrow has a higher value for the characteristic compared
        2:   if the losingCardThrow  has a higher value for the characteristic compared
        100: default value to indicate unkonwn error
        101: invalid characteristic - characteristic given as input to function was not found on one or both cards
        102: both cards had the same value for the characteristic, not allowed as per the data rules
    '''
    result = 100  # default the return value to indicate unknown error
    winCardFlagCharFound, winCardCharacteristic, winCardCharValue = winningCardThrown.extract_characteristic(characteristicChosen4Comparison)
    loseCardFlagCharFound, loseCardCharacteristic, loseCardCharValue = losingCardThrown.extract_characteristic(characteristicChosen4Comparison)
    if winCardFlagCharFound == False or loseCardFlagCharFound == False:
        result = 101      # problem - characteristic not found
    elif winCardCharValue == loseCardCharValue:
        result = 102      # problem - both cards had the same value for characteristic
    else:
        if winCardCharValue > loseCardCharValue:
            result = 1
        else:
            result = 2
    
    return (result, winCardCharValue, loseCardCharValue)
#####################################
def addJustThrownCardsToOutdatedDeck(winningCardThrown, losingCardThrown, oOutdatedDeck):
    if random.choice([0,1]) == 1:
        oOutdatedDeck.addCardToDeckAtTop(winningCardThrown)
        oOutdatedDeck.addCardToDeckAtTop(losingCardThrown)
    else:
        oOutdatedDeck.addCardToDeckAtTop(losingCardThrown)
        oOutdatedDeck.addCardToDeckAtTop(winningCardThrown)
    return oOutdatedDeck
#####################################
def playOneRound(oPlayer1, oPlayer2, winnerFlag, oOutdatedDeck):
    if winnerFlag == 1:
        oWinningPlayer = oPlayer1
        oLosingPlayer = oPlayer2
    else:
        oWinningPlayer = oPlayer2
        oLosingPlayer = oPlayer1
    print(f"\nWinner based on previous round/ dice throw is {oWinningPlayer.playerName}.")
    print(f"\n{oWinningPlayer.playerName} to choose Type of Play and the Characteristic for the round....\n")
    winningPlayerRoundTypeSelected = oWinningPlayer.showRoundOptionsAndInputPlayersSelection(True, oOutdatedDeck)
    if winningPlayerRoundTypeSelected == 1: # winning player chose Regular
        # get top card from the players deck, get choice of the characteristic to play in this round
        winningPlayerCharacteristicChosen4Round, chosenCharIndexInCharArray, winningCardToBeThrown, oWinningPlayer = oWinningPlayer.winningPlayerPlaysREGULAR()
    elif winningPlayerRoundTypeSelected == 3: # winning player chose Resurrect Spell
        # get a random card from the Outdated deck, make it the top card of the players deck, get choice of the characteristic to play in this round
        winningPlayerCharacteristicChosen4Round, chosenCharIndexInCharArray, winningCardToBeThrown, oWinningPlayer = oWinningPlayer.winningPlayerPlaysRESURRECT(oOutdatedDeck)
    else: # winning player chose God Spell
        # get top card from the players deck, get choice of the characteristic to play in this round, get choice from winner for which card of loser to be thrown
        winningPlayerCharacteristicChosen4Round, chosenCharIndexInCharArray, winningCardToBeThrown, oWinningPlayer, winningPlayerGodspellCardChoice4LosingPlayerToThrow = oWinningPlayer.winningPlayerPlaysGODSPELL(oLosingPlayer.playerDeck.countOfCardsInDeck)
    
    print(f"\n{oWinningPlayer.playerName} chose Type of Play = {'REGULAR' if winningPlayerRoundTypeSelected==1 else 'GODspell' if winningPlayerRoundTypeSelected==2 else 'RESURRECT'} and round characteristic = {winningPlayerCharacteristicChosen4Round}" )
    print(f"\n{oLosingPlayer.playerName} to choose Type of Play....\n")
    losingPlayerRoundTypeSelected = oLosingPlayer.showRoundOptionsAndInputPlayersSelection(False, oOutdatedDeck, winningPlayerRoundTypeSelected)
    if losingPlayerRoundTypeSelected == 1: # losing player chose Regular
        if winningPlayerRoundTypeSelected == 2: # winning player has played Godspell
            # get card chosen by winning player from the losing players deck
            losingCardToBeThrown, oLosingPlayer = oLosingPlayer.losingPlayerPlaysREGULARButWinningPlayerPlayedGodspell(winningPlayerGodspellCardChoice4LosingPlayerToThrow)
        else:
            # get top card from the players deck
            losingCardToBeThrown, oLosingPlayer = oLosingPlayer.losingPlayerPlaysREGULAR()
    else: # losing player chose Resurrect Spell  i.e. losingPlayerRoundTypeSelected MUST BE = 3 if all ok with logic
        if winningPlayerRoundTypeSelected == 2: # winning player has played Godspell
            # give option to winning player to change choice of card to be thrown
            losingCardToBeThrown, oLosingPlayer = oLosingPlayer.losingPlayerPlaysRESURRECTButWinningPlayerPlayedGodspell(oOutdatedDeck, winningPlayerGodspellCardChoice4LosingPlayerToThrow, oWinningPlayer)
        else:
            # get a random card from the Outdated deck and make it the top card of the players deck
            losingCardToBeThrown, oLosingPlayer = oLosingPlayer.losingPlayerPlaysRESURRECTSpell(oOutdatedDeck)
    
    # if the winning card value > losing card value, resultRet4mComparison = 1, else it is 2, any result > 2 is a problem
    resultRet4mComparison, winCardCharValue4Comparison, loseCardCharValue4Comparison = compareCharacteristicsBetweenCards(winningCardToBeThrown, losingCardToBeThrown, winningPlayerCharacteristicChosen4Round)
    #print(f"\nresultRet4mComparison = {resultRet4mComparison}")
    if resultRet4mComparison > 2:
        # winnerFlag should have had a value of 1 or 2 if all was ok
        print(f"ERROR in logic during comparison of characteristics of the cards. Function return code = {winnerFlag} . EXITING program.")
        exit(400)
    else:
        print(f"\nCharacteristic chosen for the round:::  {winningPlayerCharacteristicChosen4Round}")
        print(f"\nCard played by the starting player:::")
        winningCardToBeThrown.displayCardToConsoleClassCardMethod()
        print(f"\nCard played by the second player:::")
        losingCardToBeThrown.displayCardToConsoleClassCardMethod()

        oOutdatedDeck = addJustThrownCardsToOutdatedDeck(winningCardToBeThrown, losingCardToBeThrown, oOutdatedDeck)
    
    # the winnerFlag should be changed from 1 to 2 or vice versa, ONLY IF the winningCard object has lost this round
    if resultRet4mComparison == 2:
        if winnerFlag == 1:
            winnerFlag = 2
        else:
            # the winnerFlag is 2 currently, change it to 1
            winnerFlag = 1
    return (oPlayer1, oPlayer2, winnerFlag, winningPlayerCharacteristicChosen4Round, winCardCharValue4Comparison, loseCardCharValue4Comparison, oOutdatedDeck)
#####################################
#
##  Main logic starts here
#
oAllCardsDeck, oPlayer1, oPlayer2, winnerFlag, oOutdatedDeck = performInitialSetupForGame()
roundNumber = 1
while oPlayer1.playerDeck.countOfCardsInDeck != 0   and   oPlayer2.playerDeck.countOfCardsInDeck != 0 :
    print(f"\n\n:::::::::::::::::::::     Starting round number     :::::     {roundNumber}     :::::::::::::::::::::")
    oPlayer1, oPlayer2, winnerFlag, comparisonCharacteristicUsed, winCardCharValue, loseCardCharValue, oOutdatedDeck = playOneRound(oPlayer1, oPlayer2, winnerFlag, oOutdatedDeck)
    print(f'\nCharacteristic for comparison = "{comparisonCharacteristicUsed}". The card values were:')
    print(f"For startingPlayer = {winCardCharValue}\t\tFor secondPlayer = {loseCardCharValue}")
    if winnerFlag == 1:
        print(f"\nRound {roundNumber} won by {oPlayer1.playerName}")
        oPlayer1.points += 1
    else:
        print(f"\nRound {roundNumber} won by {oPlayer2.playerName}")
        oPlayer2.points += 1
    print(f"\nPoints Tally at end of Round #{roundNumber}  :::  {oPlayer1.playerName} has {oPlayer1.points} points ----  {oPlayer2.playerName} has {oPlayer2.points} points")
    print(f'{oPlayer1.playerName + "in lead" if oPlayer1.points > oPlayer2.points else oPlayer2.playerName + "in lead" if oPlayer2.points > oPlayer1.points else "Both players have equal points"}')
    roundNumber += 1
    input("\n\nPress any key to start the next round....")

print(f"\n\nFINAL RESULT of game:")
if oPlayer1.points > oPlayer2.points:
    print(f"\nPlayer 1 has won the game. Congratulations {oPlayer1.playerName}")
elif oPlayer1.points == oPlayer2.points:
    print(f"\nIt is a draw!")
else:
    print(f"\nPlayer 2 has won the game. Congratulations {oPlayer2.playerName}")

print(f"EXITING program - Normal exit.")
exit(0)