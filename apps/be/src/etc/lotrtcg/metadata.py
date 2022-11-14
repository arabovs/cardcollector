class HsMetadata():

    rarity_dict = {
      "R": "Rare",
      "U": "Uncommon",
      "C": "Common",
      "P": "Promo",
      "RF": "Rare Foil",
      "S": "Special Foil" # BUG with data 
    }
    # used for translating edition code to url path
    editions_dict = {
      "1": "The Fellowship of the Ring",
      "2": "Mines of Moria",
      "3": "Realms of the Elf lords",
      "4": "The Two Towers",
      "5": "Battle of helms deep",
      "6": "Ents of Fangorn",
      "7": "Battle of Helms Deep",
      "8": "The Return of the King",
      "9": "Siege of Gondor", 
      "10": "Reflections",
      "11": "Mount Doom",
      "12": "Shadows",
      "13": "Black Rider",
      "14": "Bloodlines",
      "15": "Expanded Middle-earth",
      "16": "The Hunters",
      "17": "The Wraith Collection",
      "18": "Rise of Saruman", 
      "19": "Treachery and Deceit",
      "0": "Promotional",
      "lotr promotional": "Promotional",
      "T": "Tengwar",
      "": "empty",
    }
    
    def __init__(self):
        print("Fetching status")
        
    