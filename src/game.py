# Elérhető változók:
# availableCards = egy lista amiben az összes létrehozott sima kártya fel van sorolva
# availableDungeons = egy lista amiben az összes létrehozott kazamata kártya fel van sorolva
# availableLeaders = egy lista amiben az összes létrehozott vezér kártya fel van sorolva
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

    def __init__(self, name:str, baseDmg:int, baseHp:int, cardType:str)->None:
        self.name = name
        self.baseDmg = baseDmg
        self.baseHp = baseHp
        self.type = cardType

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



availableCards:list[Card] = []
availableDungeons:list[Dungeon] = []
availableLeaders:list[Card] = []

def newCard(name:str, baseDmg:int, baseHp:int, cardType:str)->None:
    outputCard:Card = Card(name,baseDmg,baseHp,cardType)
    cardLookup[name] = len(availableCards)
    availableCards.append(outputCard);

def newLeader(srcName:str, finName:str, creationType:str)->None:
    for character in availableCards:
        if character.name == srcName:
            cardLookup[finName] = len(availableLeaders)
            if(creationType=="sebzes"):
                availableLeaders.append(Card(finName,character.baseDmg*2,character.baseHp,character.type))
            else:
                availableLeaders.append(Card(finName,character.baseDmg,character.baseHp*2,character.type))
            break;


def newDungeon(name:str, size:str, cards:list[str], reward:str)->None:
    cardLookup[name] = len(availableDungeons)
    availableDungeons.append(Dungeon(name,size,cards,reward))
