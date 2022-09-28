class ErrorHandle():

  

        def check_URL(page_url):





    
                card_back_img = "https://www.ccgcastle.com/product/lotr-tcg/lotr-complete-sets/mines-of-moria-complete-set" #img for missing cards


                #cards with uniqe URL
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/lotr-promotional/Neekerbreekers--Bog-D"): # handle signel card cus of name
                    page_url = page_url.replace("--","-")

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-helms-deep/Legolas--Sword"): # handle signel card cus of name
                    page_url = page_url.replace("--","-")  

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-helms-deep/I-d-Make-You-Squeak"): #unique URL  
                    page_url = page_url + "-1" 

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/The-One-Ring-The-Answer-To-All-Riddles-tengwar"):   
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/the-two-towers-anthology/the-one-ring-answer-to-all-riddles-t"

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Called"):   
                    page_url = page_url + "-Away"

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Cave-Troll-of-Moria-Scourge-of-the-Black-Pit-tengwar"):   
                    page_url = page_url.replace("-tengwar","")  # handel Troll. Error in the site URL (tengwar exist but no link created by site creator)

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Bilbo-Retired-Adventurer"):   
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/fellowship-of-the-ring/bilbo-baggins-retired-adventurer" # site URL error

                if(page_url == """https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Speak-"Friend"-and-Enter"""): #remove "" from the URL  
                    page_url = "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Speak-Friend-and-Enter"

                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/The-One-Ring-Isildur-s-Bane-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Fellowship-of-the-Ring/Ulaire-Otsea-Lieutenant-of-Morgul"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Mines-of-Moria/Gloin-Friend-to-Thorin"):   
                    page_url = card_back_img # non-exicting card
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
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-helms-deep/Grishnakh-Orc-Captain-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-helms-deep/Sting-Baggins-Heirloom-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/The-One-Ring-Such-A-Weight-To-Carry-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Anduril-Flame-of-the-West-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Ulaire-Cantea-Faster-Than-Winds-tengwar"):   
                    page_url = card_back_img # non-exicting card
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/The-Witch-king-Morgul-King-tengwar"):   
                    page_url = card_back_img # non-exicting card
                
                

                
                #image only on FOIL
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Ranks-Without-Number"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Gimli-Unbidden-Guest"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Gimli-Unbidden-Guest"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/The-Two-Towers/Fight-for-the-Villagers"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-helms-deep/Gollum-Nasty-Treacherous-Creature"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Battle-Tested"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Careful-Study"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Clever-Hobbits"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Corrupt"):   
                    page_url = page_url + "-foil"
                if(page_url == "https://www.ccgcastle.com/product/lotr-tcg/Battle-of-Helms-Deep/Ulaire-Otsea-Black-Mantled-Wraith"):   
                    page_url = page_url + "-foil"
                
                
               
                        
               


                return page_url
  