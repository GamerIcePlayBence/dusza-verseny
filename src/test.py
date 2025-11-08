from pathlib import Path
from src import game

def export(typein, user, destination, test_des):

    if typein == "vilag":
        kartya = []
        kartyav = []
        kazamata = []
        for kty in game.availableCards:
            if not kty.isLeader:
                kartya.append([
                kty.name,
                kty.baseDmg,
                kty.baseHp,
                kty.type
                ])
            else:
                kartyav.append([
                    kty.name,
                    kty.baseDmg,
                    kty.baseHp,
                    kty.type
                ])

        for kaz in game.availableDungeons:
            kaz_cards_list = kaz.cards  # az összes kártya

            # neve alapján szétválasztjuk a vezért és a sima kártyákat
            leaders = [c for c in kaz_cards_list if c in [v[0] for v in kartyav]]
            normal_cards = [c for c in kaz_cards_list if c not in [v[0] for v in kartyav]]

            # ha van vezér, azt rakjuk a sor végére
            if leaders:
                kaz_cards_str = ",".join(normal_cards) + ";" + leaders[0]
            else:
                kaz_cards_str = ",".join(normal_cards)

            kazamata.append([
                kaz.type,
                kaz.name,
                kaz_cards_str,
                kaz.reward
            ])



        with open(Path(test_des + "/" +destination), 'w', encoding="ASCII") as out:
            for ktyf in kartya:
                out.write("kartya;")
                out.write(";".join(map(str, ktyf)) + "\n")

            out.write("\n")

            for ktyf2 in kartyav:
                out.write("vezer;")
                out.write(";".join(map(str, ktyf2)) + "\n")

            out.write("\n")

            for ktyf3 in kazamata:
                out.write("kazamata;")
                out.write(";".join(map(str, ktyf3)) + "\n") 

    elif typein == "jatekos":
        gyujtemeny = []
        pakli = []
        for i in range(len(user.cards)):
            gyujtemeny.append([user.cards[i].name, user.cards[i].baseDmg, user.cards[i].baseHp, user.cards[i].type])
        
        for i2 in range(len(user.selected)):
           usersect = user.selected[i2]
           pakli.append(user.cards[usersect].name)

        with open(Path(test_des + "/" +destination), 'w', encoding="ASCII") as out:
            for gyuj in gyujtemeny:
                out.write("gyujtemeny;")
                out.write(";".join(map(str, gyuj)) + "\n")

            out.write("\n")

            for pack in pakli:
                out.write("pakli;")
                out.write(pack + "\n")

def TESTMain(test_dir_path):
    if Path(test_dir_path + '/in.txt').is_file():
        user = game.User()
        with open(Path(test_dir_path) / 'in.txt', 'r', encoding="ASCII") as f:
            kereses = False
            for row in f:
                row = row.strip()
                if row.find(";") != -1:
                    character = row.split(";")
                    if character[0] == "uj kartya":
                        game.newCard(character[1], character[2], character[3], character[4])
                        kereses = True
                    elif row.startswith("uj vezer"):
                        if len(character[1]) <= 16:
                            game.newLeader(character[2], character[1], character[3])
                            kereses = True
                        else:
                            kereses = False
                    elif row.startswith("uj kazamata"):
                        kazamanta_name = character[2]
                        kazamanta_size = character[1]
                        cards = character[3].split(",")
                        if len(kazamanta_name) <= 20:
                            if len(character) == 6:
                                cards.append(character[4])
                                game.newDungeon(kazamanta_name, kazamanta_size, cards, character[5])
                            else:
                                game.newDungeon(kazamanta_name, kazamanta_size, cards, character[4])
                            kereses = True
                        else:
                            kereses = False
                    elif row.startswith("uj jatekos"):
                        kereses = True
                        continue
                    elif row.startswith("felvetel gyujtemenybe"):
                        user.addCard(character[1])
                    elif row.startswith("uj pakli"):
                            if len(user.cards) % 2 == 0:
                                 mkp = len(user.cards) / 2
                            else:
                                mkp = len(user.cards) + 1
                            mkp = int(mkp)
                            pack_k = character[1].split(",")
                            if len(pack_k) <= mkp:
                                for pack_k2 in pack_k:
                                    user.addCardToPack(pack_k2)
                                kereses = True
                            else:
                                kereses = False
                    elif row.startswith("export vilag"):
                        export("vilag", user, character[1], test_dir_path)
                    elif row.startswith("export jatekos"):
                        export("jatekos", user, character[1], test_dir_path)
        if not kereses:
            print("Hibás in.txt fálj!")
        pass
    else:
        print("Hibás útvonal! Kérjük a megfelelő útvonalat írja be! (pl.: C:/dusza/)")