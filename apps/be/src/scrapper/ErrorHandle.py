class ErrorHandle():

  

        def check_URL(page_url):


                # if page_url(last element) == "-tengwar" replace with "-t" !!!!!  
                # ako smenim "-tengwar" s "-t" kartite v na4aloto koito sa "-tengwar" 6te sprat da rabotqt
                # Cave-Troll-of-Moria-Scourge-of-the-Black-Pit missint "-t" in URL


    
                card_back_img = "https://www.ccgcastle.com/product/lotr-tcg/lotr-complete-sets/mines-of-moria-complete-set" #img for missing cards

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/lotr-promotional/Neekerbreekers--Bog-D"): # handle signel card cus of name
                    page_url = page_url.replace("--","-")
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/The-One-Ring-Isildur-s-Bane-tengwar"):   
                    page_url = card_back_img # handle isildur's bane
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Cave-Troll-of-Moria-Scourge-of-the-Black-Pit-tengwar"):   
                    page_url = page_url.replace("-tengwar","")  # handel Troll. Error in the site URL (tengwar exist but no link created by site creator)
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Ulaire-Enquea-Lieutenant-of-Morgul-tengwar"):   
                    page_url = page_url.replace("-tengwar","-t")
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Ulaire-Otsea-Lieutenant-of-Morgul"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Bilbo-Retired-Adventurer"):   
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/fellowship-of-the-ring/bilbo-baggins-retired-adventurer" # site URL error
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Gloin-Friend-to-Thorin"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == """https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Speak-"Friend"-and-Enter"""):   
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Speak-Friend-and-Enter"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/The-Balrog-Flame-of-Udun"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Gimli-Dwarf-of-the-Mountain-race-M"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Realms-of-the-Elf-lords/Mines-of-Khazad-Dum"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Realms-of-the-Elf-lords/Arwen-Lady-Undomiel"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Realms-of-the-Elf-lords/Forests-of-Lothlorien"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Realms-of-the-Elf-lords/The-Palantir-of-Orthanc"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Realms-of-the-Elf-lords/Tower-of-Barad-dur"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Hides-tengwar"):   
                    page_url = page_url.replace("-tengwar","-t")
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Gimli-Unbidden-Guest"):   
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Gimli-Unbidden-Guest-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Legolas-Dauntless-Hunter-tengwar"):   
                    page_url = page_url.replace("-tengwar","-t")


                return page_url
  