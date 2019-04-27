from rubiks import *
import sys
import random

def print_menu():
    print("---------------------------------------------")
    print("| RUBIKS CUBE BLINDSOLVE PRACTICE INTERFACE |")
    print("---------------------------------------------")
    print("| Options:                                  |")
    print("|    ~Press 1 for planning practice         |")
    print("|    ~Press 2 for move practice             |")
    print("|    ~Press 3 for the whole shabang         |")
    print("|    ~Press 4 to see stats                  |")
    print("|    ~Press n to quit                       |")
    print("---------------------------------------------")

def happymessage():
    messages = open("happymessages.txt", 'r')
    happymessages = []
    message = messages.readline()
    while message:
        happymessages.append(message)
        message = messages.readline()
    random.shuffle(happymessages)
    print("\n~~ Congrats! ~~")
    print("    " + happymessages[0])

def sadmessage():
    messages = open("sadmessages.txt", 'r')
    sadmessages = []
    message = messages.readline()
    while message:
        sadmessages.append(message)
        message = messages.readline()
    random.shuffle(sadmessages)
    print("\n~~ You Have Failed! ~~")
    print("    " + sadmessages[0])

def scramble(cube, show = False):
    scramble = cube.gen_scramble(n_moves=20)
    for s in scramble:
        cube.move(s)
    if show == True:
        print("Scramble Sequence: ", scramble)
    return scramble

def plan(cube):
    edges = input("Enter the edge letter sequence: ")
    edges = [edges[i] for i in range(len(edges))]
    for edge in edges:
        moves = cube.translate("edges", [edge])
        for move in moves:
            cube.move(move)
        cube.show_cube()
    if cube.checkSolved("edges"):
        happymessage()
        print(" Now, the corners.")
    else:
        sadmessage()
        return 0
    corners = input("Enter the corner letter sequence: ")
    corners = [corners[i] for i in range(len(corners))]
    for corner in corners:
        moves = cube.translate("corners", [corner])
        for move in moves:
            cube.move(move)
        cube.show_cube()
    if cube.checkSolved():
        happymessage()
        return 1
    else:
        sadmessage()
        return 0

def execute(cube, scramble_sequence):
    print("Solving...")
    edge_letters, corner_letters = cube.solve()
    for s in scramble_sequence:
        cube.move(s)
    cube.show_cube()
    print("Edge Letter Sequence: ")
    print(edge_letters)
    correct = input("Did you solve all the edges? (y/n): ")
    if correct == "y":
        happymessage()
        print("Lets do the corners.")
    else:
        sadmessage()
        return 0
    print("Corner Letter Sequence: ")
    print(corner_letters)
    correct = input("Did you solve all the corners? (y/n): ")
    if correct == "y":
        happymessage()
        return 1
    else:
        sadmessage()
        return 0

def main():
    plan_stats = open("plan.txt", "a")
    execute_stats = open("execute.txt", "a")
    solve_stats = open("solve.txt", "a")
    cube = Rubiks()
    cube.show_cube()
    print_menu()
    correct = 0
    trials = 0
    status = input("->")
    if status == "1":
        print("\n")
        print("~~~~~~~~~~~~~~~~~~~~~")
        print("~ PLANNING PRACTICE ~")
        print("~~~~~~~~~~~~~~~~~~~~~")
        scramble_sequence = scramble(cube, show= True)
        cube.show_cube()
        correct= correct + plan(cube)
        trials = trials + 1
        print("   ------------------------------------")
        print("   | ~To go again, press 1.           |")
        print("   | ~To quit, press n.               |")
        print("   | ~To return to main menu, press b.|")
        print("   ------------------------------------")
        status = input("->")
        while status == "1":
            print("\n")
            print("~~~~~~~~~~~~~~~~~~~~~")
            print("~ PLANNING PRACTICE ~")
            print("~~~~~~~~~~~~~~~~~~~~~")
            scramble_sequence = scramble(cube, show=True)
            cube.show_cube()
            correct = correct + plan(cube)
            trials = trials + 1
            print("   ------------------------------------")
            print("   | ~To go again, press 1.           |")
            print("   | ~To quit, press n.               |")
            print("   | ~To return to main menu, press b.|")
            print("   ------------------------------------")
            status = input("->")
        if status == "n":
            if trials >= 2:
                print("accuracy: ", correct/trials)
                print("trials: ", trials)
                date = input("Enter date:")
                if date != "\n":
                    plan_stats.write("<")
                    plan_stats.write(date)
                    plan_stats.write("-")
                    plan_stats.write(str(correct))
                    plan_stats.write("-")
                    plan_stats.write(str(trials))
                    plan_stats.write(">")
                    plan_stats.write("\n")
                    plan_stats.close()
            exit()
        elif status == "b":
            main()

    elif status == "2":
        print("\n")
        print("~~~~~~~~~~~~~~~~~")
        print("~ MOVE PRACTICE ~")
        print("~~~~~~~~~~~~~~~~~")
        scramble_sequence = scramble(cube, show=True)
        cube.show_cube()
        correct = correct + execute(cube, scramble_sequence)
        trials = trials + 1
        print("   ------------------------------------")
        print("   | ~To go again, press 2.           |")
        print("   | ~To quit, press n.               |")
        print("   | ~To return to main menu, press b.|")
        print("   ------------------------------------")
        status = input("->")
        while status == "2":
            print("\n")
            print("~~~~~~~~~~~~~~~~~")
            print("~ MOVE PRACTICE ~")
            print("~~~~~~~~~~~~~~~~~")
            scramble_sequence = scramble(cube, show= True)
            cube.show_cube()
            correct = correct + execute(cube, scramble_sequence)
            trials = trials + 1
            print("   ------------------------------------")
            print("   | ~To go again, press 2.           |")
            print("   | ~To quit, press n.               |")
            print("   | ~To return to main menu, press b.|")
            print("   ------------------------------------")
            status = input("->")
        if status == "n":
            if trials >= 2:
                print("accuracy: ", correct / trials)
                print("trials: ", trials)
                date = input("Enter date:")
                if date != "\n":
                    execute_stats.write("<")
                    execute_stats.write(date)
                    execute_stats.write("-")
                    execute_stats.write(str(correct))
                    execute_stats.write("-")
                    execute_stats.write(str(trials))
                    execute_stats.write(">")
                    execute_stats.write("\n")
                    execute_stats.close()
            exit()
        elif status == "b":
            main()

    #elif status == "3":
    #elif status == "4":
    #elif status == "n":
    else:
        print("Please enter valid option.")
        main()


main()
print("hello mate")
sys.exit()