isEhhed = False
isJuljung = False

def ehh():
        global isEhhed
        global isJuljung
        if isEhhed == False:
            print("뿌에엥!!!!!!!!!!!!!!!!!!")
            isEhhed = True
        else:
            raise Exception("Majinse cannot ehh while it is already ehhed, Try using stopEhh() to initialize the ehh process")