from random import randint
import time


def secret_generator():
    """"This function generate Secret Number"""
    secret_number = []
    while len(secret_number) < NUM_LENGTH:
        random_number = randint(1, 9)
        if random_number not in secret_number:
            secret_number.append(random_number)
    return secret_number


def player_number(player_input):
    """This function transform user input at list and check for valid values"""
    player_numb = []
    if len(player_input) == NUM_LENGTH:
        for idx in range(0, NUM_LENGTH):
            if player_input[idx].isdigit():
                player_numb.append(int(player_input[idx]))
            else:
                raise ValueError("You have to input only digits")
    else:
        raise ValueError("You need to input 4 digit number")

    if len(set(player_numb)) != NUM_LENGTH:
        raise ValueError("All digit have to be unique!")
    return player_numb


def calculation(player: list, secret: list):
    """This function calculate how many digit are guessed"""
    bulls = 0
    cows = 0
    for idx in range(0, NUM_LENGTH):
        if player[idx] in secret:
            if player[idx] == secret[idx]:
                bulls += 1
            else:
                cows += 1
    return bulls, cows


def start_game(player, counter):
    """This function:
     -  set timers for start and stop
     - call calculation function
     -  save record to file"""

    secret_num = secret_generator()

    print("NEW GAME was started!")
    game_start_time = time.perf_counter()
    game_stop_time, counter = playing(secret_num, counter)
    game_time = game_stop_time - game_start_time

    file = open("records.txt", "a")
    file.write(f"{player}, {counter}, {game_time},\n")
    file.close()


def playing(secret_num, counter):
    """This function get user input and call calculation function"""
    while True:
        counter += 1
        player_num = player_number(input("Enter digit: "))
        bulls, cows = calculation(player_num, secret_num)
        report(bulls, cows, counter)
        if bulls == 4:
            stop_time = time.perf_counter()
            return stop_time, counter


def report(bulls: int, cows: int, tries_count):
    """This function print messages"""
    if bulls == 4:
        print(f"Congratulation! \n You find the number with {tries_count} tries")
    else:
        print(f"You find {bulls} bulls and {cows} cows. Try again!")


def scoreboard():
    """This function print scoreboard and create sorted file"""
    file = open("records.txt", "r")
    scoreboard_matrix = []
    for line in file:
        scoreboard_matrix.append(line.split(','))

    scoreboard_matrix.sort(key=lambda x: (int(x[1]), float(x[2])))

    print("\n#####    SCOREBOARD  #####")
    print("USERNAME -> #TRIES_COUNT -> TIME")
    for line in scoreboard_matrix:
        print(f"{line[0]} -> {line[1]} -> {float(line[2]):.2f}")

    sorted_file = open("sorted_scoreboard.txt", "w")
    sorted_file.write(f"{scoreboard_matrix}")
    sorted_file.close()


if __name__ == "__main__":
    print("""
    ################################
    ######    BULLS & COWS   #######
    ################################
    
    Welcome, let`s play Bulls & Cows!
    
    Your mission is to guess the secret 4-digit number.
    ENTER 4 digit number with unique number (digit range 1-9).
    Bulls - right digits are in their right positions.
    Cows - right digits are in their different positions.""")

    print("""
        ####    MENU    ####
        Select number of menu:
        1. NEW GAME
        2. Scoreboard
        3. Exit  
        """)
    player_name = None
    NUM_LENGTH = 4
    while True:
        attend_counter = 0

        choose = int(input("Enter your choose: "))
        if choose == 1:
            player_name = input("Enter Player Name: ")
            start_game(player_name, attend_counter)
        elif choose == 0:
            if player_name:
                start_game(player_name, attend_counter)
            else:
                print("You have to enter USERNAME!")
                while not player_name:
                    player_name = input("Enter Player Name: ")
                start_game(player_name, attend_counter)
        elif choose == 2:
            scoreboard()
        elif choose == 3:
            break

        print("""
        ####    MENU    ####
        Select number of menu:
        0. Continue with current username
        1. NEW GAME (new USER)
        2. Scoreboard
        3. Exit  
        """)
