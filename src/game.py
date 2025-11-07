# Elérhető változók:
# availableCards = egy lista amiben az összes létrehozott sima kártya és vezető fel van sorolva
# availableDungeons = egy lista amiben az összes létrehozott kazamata kártya fel van sorolva
# cardLookup = ez egy lookup table amibe minden névhez a saját listájában lévő pozíciója van tárolva használat: cardLookup["név"]

# Elérhető function-ök
# newCard(name:str, baseDmg:int, baseHp:int, cardType:str) = létrehoz egy új kártyát és beteszi az "availableCards" listába
# newLeader(srcName:str, finName:str, creationType:str) = létrehoz egy új kártyát és beteszi az "availableLeaders" listába
# newDungeon(name:str, size:str, cards:list[str], reward:str) = létrehoz egy új kártyát és beteszi az "availableDungeons" listába

cardLookup:dict[str,int] = {}

class Card:
    # self.name = név
    # self.baseDmg = a kártya sebzési értéke amit a játék mester állított be
    # self.baseHp = a kártya életereje amit a játék mester állított be
    # self.type = a kártya típusa
    # self.isLeader = a kártya leader-e

    def __init__(self, name:str, baseDmg:int, baseHp:int, cardType:str, isLeader:bool)->None:
        self.name = name
        self.baseDmg = baseDmg
        self.baseHp = baseHp
        self.type = cardType
        self.isLeader = isLeader

class Dungeon:
    # self.name = név
    # self.type = típus (egyszerű, kicsi, nagy)
    # self.cards = a benne szereplő karakterek nevének listája
    # self.reward = az jutalom amit a nyereségért kap a felhasználó

    def __init__(self, name:str, size:str, cards:list[str], reward:str)->None:
        self.name = name
        self.type = size
        self.cards = cards
        self.reward = reward

class User:
    # self.cards = a felhasználó kártyái
    # self.selected = a felhasználó paklijában lévő kártyák sorszáma
    # self.cardNames = a felhasználó kártyáinak nevei a sorszámukkal (self.cardnames[név]=szám)

    def __init__(self):
        self.cards:list[Card] = []
        self.selected:list[int] = []
        self.cardNames:dict[str,int] = {}

    def addCardToPack(self, card:str)->None:
        self.selected.append(self.cardNames[card])

    # Nullát ad vissza ha jól futott
    # -1-et ha egyébként se volt benne a kártyák között
    def removeCardFromPack(self, card:str)->int:
        index:int = self.cardNames[card]
        for i in range(len(self.selected)):
            if self.selected[i] == index:
                self.selected.pop(i)
                return 0
        return -1

    def addCard(self, card:str)->None:
        originalCard = availableCards[cardLookup[card]]
        self.cards.append(Card(originalCard.name,originalCard.baseDmg,originalCard.baseHp,originalCard.type,originalCard.isLeader))

    # isStrength = true ha az erősséget kell upgrade-lni
    def upgradeCard(self, card:str, isStrength:bool)->None:
        if isStrength:
            self.cards[self.cardNames[card]].baseDmg += 2
        else:
            self.cards[self.cardNames[card]].baseHp += 2

class Fight:
    # self.dungeonCards = egy lista a kazamata összes kártyájával
    # self.userCards = egy lista a játékos összes kártyájával
    def __init__(self, dungeonIndex:int, user:User):
        self.dungeonCards:list[Card] = []
        for cardName in availableDungeons[dungeonIndex].cards:
            card = availableCards[cardLookup[cardName]]
            self.dungeonCards.append(Card(card.name,card.baseDmg,card.baseHp,card.type,card.isLeader))

        self.userCards:list[Card] = []
        for index in user.selected:
            card = user.cards[index]
            self.userCards.append(Card(card.name,card.baseDmg,card.baseHp,card.type,card.isLeader))

availableCards:list[Card] = []
availableDungeons:list[Dungeon] = []

def newCard(name:str, baseDmg:int, baseHp:int, cardType:str)->None:
    outputCard:Card = Card(name,baseDmg,baseHp,cardType,False)
    cardLookup[name] = len(availableCards)
    availableCards.append(outputCard)

def newLeader(srcName:str, finName:str, creationType:str)->None:
    for character in availableCards:
        if character.name == srcName:
            cardLookup[finName] = len(availableCards)
            if(creationType=="sebzes"):
                availableCards.append(Card(finName,character.baseDmg*2,character.baseHp,character.type,True))
            else:
                availableCards.append(Card(finName,character.baseDmg,character.baseHp*2,character.type,True))
            break


def newDungeon(name:str, size:str, cards:list[str], reward:str)->None:
    cardLookup[name] = len(availableDungeons)
    availableDungeons.append(Dungeon(name,size,cards,reward))


def startFight(dungeonIndex:int)->Fight:
    pass
