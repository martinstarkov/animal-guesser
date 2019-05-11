file = open("database.dat","r")
#collect strings from database file
lines = file.readlines()
file.close()

data = []

#format and add columns from database into data array
for index, line in enumerate(lines):
    if len(line.strip()) > 0:
        column = line.split("---")
        question = column[1].strip().capitalize()
        if question[-1] != "?":
            question += "?"
        #row[2] is yes-path, row[3] is no-path
        row = [index, question, column[2].strip().lower().capitalize(), column[3].strip().lower().capitalize()]
        data.append(row)

#run custom functions based on user input to yes or no questions
def askQuestion(question, function, index, param):
    userInput = input(question)
    if userInput.strip()[0] == "y":
        function(2, index, param)
    elif userInput.strip()[0] == "n":
        function(3, index, param)
    else:
        print("Please only answer with ""yes"" or ""no"".")
        askQuestion(question, function, index, param)

#determine if final answer was correct, if not: prompt the user to add the answer to the database
def decide(answer, index, previousAnswer):
    if answer == 2:
        print("Yay, I'm a genius!")
    else:
        correct = input("What was the correct animal? ")
        #get user input for correct answer properties
        newAnimal = [str(len(data)), input('Provide a (yes/no) question to distinguish "' + data[index][previousAnswer].capitalize() + '" from "' + correct.strip().capitalize() + '": ').strip().capitalize(), input("What is the yes answer? ").strip().capitalize(), input("What is the no answer? ").strip().capitalize()]
        if newAnimal[1][-1] != "?":
            newAnimal[1] += "?"
        #clear database file and refill with formatted lists
        f = open("database.dat","w")
        for idx, animal in enumerate(data):
            #change the computer's wrong guess to the digit that corresponds to the added question's index
            if idx == index:
                if previousAnswer == 2:
                    animal[2] = str(len(data))
                else:
                    animal[3] = str(len(data))
            animal[0] = str(idx)
            f.writelines(" --- ".join(animal) + "\n")
  
        f.writelines(" --- ".join(newAnimal) +"\n")
        f.close()
        print("Thank you for improving the database!")

#check if answer corresponds to a path digit or final answer
def processInput(answer, index, param):
    if data[index][answer].isdigit():
        askTheUser(int(data[index][answer]))
    else:
        askQuestion('Is "' + data[index][answer].capitalize() + '" correct? (yes/no): ', decide, index, answer)

#ask the user (yes/no) database questions
def askTheUser(index):
    if (index > len(data) - 1):
        print("Error in database: Question " + str(index) + " doesn't exist")
    else:
        askQuestion(data[index][1] + " (yes/no): ", processInput, index, 0)

askTheUser(0)