from pathlib import Path
from src import game

def TESTMain(test_dir_path):
    if Path(test_dir_path + '/in.txt').is_file():
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
                            game.newLeader(character[1], character[2], character[3])
                            kereses = True
                        else:
                            kereses = False
                    elif row.startswith("uj kazamata"):
                        kazamanta_name = character[2]
                        kazamanta_size = character[1]
                        cards = character[3].split(",")
                        if len(kazamanta_name) <= 20:
                            game.newDungeon(kazamanta_name, kazamanta_size, cards, character[4])
                            kereses = True
                        else:
                            kereses = False
                    elif row.startswith("uj jatekos"):
                        kereses = True
                        continue
        if not kereses:
            print("Hibás in.txt fálj!")
        pass
    else:
        print("Hibás útvonal! Kérjük a megfelelő útvonalat írja be! (pl.: C:/dusza/)")