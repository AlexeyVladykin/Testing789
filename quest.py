def questionOne():
    flag = True
while flag:
    print("Какая самая высокая гора в мире?")
    answer = input("ввод: ")
    try:
        if answer.lower() == "эверест":
            True
            print("верно, можете идти дальше")
        else:
            print("неправильно, начни с начала:)")
            flag = False
    except ValueError:
        print("ввод недействителен. ошибка")
        
def questionTwo():
        flag = True
while flag:
        print("Как звали главного бога славян?")
        answer = input("ввод: ")
        try:
            if answer.lower() == "перун":
                True
                print("верно, можете идти дальше")
            else:
                print("неправильно, начни с начала:)")
                flag = False
        except ValueError:
            print("ввод недействителен. ошибка")
        
def questionThree():
     flag = True
while flag:
    print("Какой самый большой по площади материк?")
    answer = input("ввод: ")
    try:
        if answer.lower() == "евразия":
            True
            print("верно, можете идти дальше")
        else:
            print("неправильно, начни с начала:)")
            flag = False
    except ValueError:
        print("ввод недействителен. ошибка")

def game(answer):
     flajok = True
    
     print("вы просыпаетесь среди леса, перед вами 3 тропы\n путь налево, прямо и направо\n ")
    
     answer = input("куда пойти (1-3): ")
     if answer == "1":
         questionOne()
    
def main():     
    answer = ""
    game(answer)


main()
