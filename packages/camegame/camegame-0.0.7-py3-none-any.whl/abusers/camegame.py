import abusers.minecraft

isEhhed = False
isJuljung = False
oldPeopleCount = "NaN"

def ehh():
        global isEhhed
        global isJuljung
        if isEhhed == False:
            print("뿌에엥!!!!!!!!!!!!!!!!!!")
            isEhhed = True
        else:
            raise Exception("Majinse cannot ehh while it is already ehhed, Try using stopEhh() to initialize the ehh process")
        
def whereTouch():
     print("<camegame> 어딜 만지세요 어딜만져 헤으응")

def stopEhh():
    global isEhhed
    if isEhhed == True:
        print("마진새는 진정햇다.")
        isEhhed = False
    else:
         raise Exception("Majinse cannot stop ehh while it is not ehhed, Try using ehh() to initialize the ehh process")
    
def touchLoop(touchCount):
    touches = int(touchCount)
    for i in range(touches):
        print("어딜 " + str(i + 1) + "번 만지세요 어딜만져 헤으응")
    
    print("마진새는 파이썬에서도 이 난리를 치고있다. " + str(touches) + "번 만진 결과 마진새는 절정에 도달했다. 역겹다.")

def attackOldPerson(damages):
     global oldPeopleCount
     if(oldPeopleCount == "NaN"):
         raise Exception("Old People's population has been not set. Use setOldPersonCount() to set the population")
     else:
          if(oldPeopleCount > 0):
            print("<camegame> 이 늙은이 같은게!")
            print("마진새는 앞으로 살날이 많지 않은 불쌍한 노년기의 사람들을 " + str(damages) + " 번 공격했다.")
            previousCount = oldPeopleCount
            oldPeopleCount = oldPeopleCount - int(damages)
            if(oldPeopleCount <= 0):
                oldPeopleCount = 0
                print("마진새의 공격으로 인해 남아있던 노인들이 다 사라졌다.")
            else:
                print("노인들의 인구가 " + str(previousCount) + "명에서 " + str(oldPeopleCount) + "명으로 줄었다.")
            print("<camegame> 뭐래 뭐하냐")
          else:
              print("마진새 때문에 더이상 노인들이 없다.")




def setOldPersonCount(count):
    global oldPeopleCount
    oldPeopleCount = int(count)
    
def secretJuJU():
    print("이상한거 하는거 아닙니ㅏㄷ")
    abusers.minecraft.main()