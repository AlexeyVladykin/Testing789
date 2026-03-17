import random

lvl = 0
answer = True
left = ["лево1", "лево2"]
right = [" Ghfdj 2","Право 2"]
questions = { "Сколько букв в слове кот? " : 3, "2 + 2?" : 4, "" : 2}
side = "..."

while(True):
    if (answer == False):
        lvl = 0
        print("Вы неправильно ответили на вопрос. Боги вернули вас на исходную позицию...")
    else:
        if(side =="лево" or "Лево" or "ktdj"):
            print(list[lvl])
        if(side =="право" or "Право" or "ghfdj"):
            print(right[lvl])
    side = input("Пожалуйста выбирите в какую сторону вы пойдете: ")
    print("Теперь для прохода ответьте на пару вопросов:")
    num_questions = random.randint(1, 10)
    ask, ans = questions[num_questions]
    print(ask)
    user_answer = input("Введите ответ:")
    if(user_answer == ans):
        answer = True
        
        num_questions = random.randint(1, 10)
        ask, ans = questions[num_questions]
        print(ask)
        user_answer = input("Введите ответ:")
        if(user_answer == ans):
            answer = True

            num_questions = random.randint(1, 10)
            ask, ans = questions[num_questions]
            print(ask)
            user_answer = input("Введите ответ:")
            if(user_answer == ans):
                answer = True
            else:
                answer = False
        else:
            answer = False
    else:
        answer = False
            
        
    
    