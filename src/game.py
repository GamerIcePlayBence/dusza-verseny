# Elérhető változók:
# availableCards = egy lista amiben az összes létrehozott sima kártya és vezető fel van sorolva
# availableDungeons = egy lista amiben az összes létrehozott kazamata kártya fel van sorolva
# cardLookup = ez egy lookup table amibe minden névhez a saját listájában lévő pozíciója van tárolva használat: cardLookup["név"]

# Elérhető function-ök
# newCard(name:str, baseDmg:int, baseHp:int, cardType:str) = létrehoz egy új kártyát és beteszi az "availableCards" listába
# newLeader(srcName:str, finName:str, creationType:str) = létrehoz egy új kártyát és beteszi az "availableLeaders" listába
# newDungeon(name:str, size:str, cards:list[str], reward:str) = létrehoz egy új kártyát és beteszi az "availableDungeons" listába

cardLookup:dict[str,int] = {}
# cardRelations[water][water] = 1 az első az egyik a második a másik kártya tulajdonsága
cardRelations:dict[str,dict[str,float]] = {
        "levego":{"viz":2,
               "tuz":1/2,
               "fold":2,
               "levego":1},
        "viz":{"viz":1,
                 "tuz":2,
                 "fold":1/2,
                 "levego":2},
        "tuz":{"viz":2,
                "tuz":1,
                "fold":2,
                "levego":1/2},
        "fold":{"viz":1/2,
                 "tuz":2,
                 "fold":1,
                 "levego":2}
        }

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
        self.cardNames[card] = len(self.cards)
        self.cards.append(Card(originalCard.name,originalCard.baseDmg,originalCard.baseHp,originalCard.type,originalCard.isLeader))

    # isStrength = true ha az erősséget kell upgrade-lni
    def upgradeCard(self, card:str, isStrength:bool)->None:
        if isStrength:
            self.cards[self.cardNames[card]].baseDmg += 1
        else:
            self.cards[self.cardNames[card]].baseHp += 2

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


def fight(dungeonIndex:int, user:User)->str:
    out:str = f'harc kezdodik;{availableDungeons[dungeonIndex].name}\n\n'
    dungeonCards:list[Card] = []
    userCards:list[Card] = []

    for cardName in availableDungeons[dungeonIndex].cards:
        card = availableCards[cardLookup[cardName]]
        dungeonCards.append(Card(card.name,card.baseDmg,card.baseHp,card.type,card.isLeader))

    for index in user.selected:
        card = user.cards[index]
        userCards.append(Card(card.name,card.baseDmg,card.baseHp,card.type,card.isLeader))


    playedUserCard:int = -1
    playedDungeonCard:int = -1
    roundcounter = 0
    while len(userCards)>0 and len(dungeonCards)>0:
        roundcounter += 1

        if playedDungeonCard < 0:
            playedDungeonCard = 0
            if len(dungeonCards) == 0:
                out += '\n'
                break
            playedCard = dungeonCards[playedDungeonCard]
            out += f'{roundcounter}.kor;kazamata;kijatszik;{playedCard.name};{playedCard.baseDmg};{playedCard.baseHp};{playedCard.type}\n'
        else:
            assert(playedUserCard >= 0)
            playedbyuser = userCards[playedUserCard]
            playedCard = dungeonCards[playedDungeonCard]
            damagenum = int(playedCard.baseDmg*cardRelations[playedCard.type][playedbyuser.type])
            playedbyuser.baseHp -= damagenum

            out += f'{roundcounter}.kor;kazamata;tamad;{playedCard.name};{damagenum};{playedbyuser.name};'

            if playedbyuser.baseHp <= 0:
                playedUserCard = -1
                out += "0\n"
                userCards.pop(0)
            else:
                out += str(playedbyuser.baseHp)+'\n'



        if playedUserCard < 0:
            playedUserCard = 0
            if len(userCards) == 0:
                out += '\n'
                break
            playedbyuser = userCards[playedUserCard]
            out += f'{roundcounter}.kor;jatekos;kijatszik;{playedbyuser.name};{playedbyuser.baseDmg};{playedbyuser.baseHp};{playedbyuser.type}\n'
        else:
            assert(playedDungeonCard >= 0)
            playedbyuser = userCards[playedUserCard]
            playedCard = dungeonCards[playedDungeonCard]
            damagenum = int(playedCard.baseDmg*cardRelations[playedbyuser.type][playedCard.type])
            playedCard.baseHp -= damagenum

            out += f'{roundcounter}.kor;jatekos;tamad;{playedbyuser.name};{damagenum};{playedCard.name};'

            if playedCard.baseHp <= 0:
                playedDungeonCard = -1
                out += "0\n"
                dungeonCards.pop(0)
            else:
                out += str(playedCard.baseHp)+'\n'

        out += '\n'


    if len(userCards) == 0:
        out += "jatekos vesztett\n"
    else:
        out += "jatekos nyert;"
        if availableDungeons[dungeonIndex].reward != "":
            out += f'{availableDungeons[dungeonIndex].reward};{userCards[0].name}\n'
            user.upgradeCard(userCards[0].name,availableDungeons[dungeonIndex].reward == "sebzes")
        else:
            for character in availableCards:
                name = character.name
                if not (name in user.cardNames):
                    out += name + '\n'
                    user.addCard(name)
                    break;

    return out

if __name__ == "__main__":
    newCard("Corky",2,4,"fold")
    newCard("Kira",2,7,"levego")
    newCard("Sadan",2,4,"levego")
    newCard("LEGEND",68,69,"air")

    newDungeon("Teszt1a Kazamata","nagy",["Sadan"],"")

    user = User()
    user.addCard("Kira")
    user.addCard("Corky")
    user.addCardToPack("Corky")
    user.addCardToPack("Kira")

    print(fight(0,user))

