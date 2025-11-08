from pathlib import Path

def TESTMain(test_dir_path):
    if Path(test_dir_path + '/in.txt').is_file():
        with open(Path(test_dir_path) / 'in.txt', 'r') as f:
            print("TEST")
        
        pass
    else:
        print("Hibás útvonal! Kérjük a megfelelő útvonalat írja be! (pl.: C:/dusza/)")