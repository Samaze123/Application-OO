import random
import argparse
import sys

url: str = "games_saved.txt"


def check_number_input(string: str, minimum: int = None, maximum: int = None) -> bool:
    """
    This function check if the string is convertible into integer
    If minimum and/or maximum are given, check also if it's between them
    :param string: A string that will be checked for a number
    :type string: str
    :param minimum: An integer number
    :type string: int
    :param maximum: An integer number
    :type string: int
    :returns: True if the string is convertible to digit and respect the minimum and the maximum
    :rtype: bool
    """
    if not string.isdigit():
        return False
    if maximum is not None and minimum is not None:
        if maximum >= int(string) >= minimum:
            return True
        return False
    elif maximum is not None:
        if maximum >= int(string):
            return True
        return False
    elif minimum is not None:
        if int(string) >= minimum:
            return True
        return False
    return True


def save_game(pseudo: str, score: int):
    try:
        with open(url, "rt") as file_read:
            lines: list = file_read.readlines()
        list_pseudo: list = []
        for line in lines:
            line: str
            player = Player(line.split()[0], int(line.split()[1]))
            list_pseudo.append(player)
        player: Player = Player.pseudo_in_list(list_pseudo, pseudo)
        if not player:
            with open(url, "at") as file_write:
                file_write.write(f"{pseudo} {score}\n")
        elif player.score > score:
            for i in range(len(lines)):
                if lines[i].split()[0] == player.pseudo:
                    lines[i] = f"{pseudo} {score}\n"
                    break
            with open(url, "wt") as file_write:
                for line in lines:
                    file_write.write(line)
        return None
    except FileNotFoundError:
        open(url, "x")
        save_game(pseudo, score)


class Player:
    def __init__(self, pseudo: str, score: int = 0):
        self.__pseudo: str = pseudo
        self.__score: int = score

    @property
    def pseudo(self):
        return self.__pseudo

    @property
    def score(self):
        return self.__score

    @staticmethod
    def pseudo_in_list(list_player: list, pseudo: str):
        for player in list_player:
            if player.pseudo == pseudo:
                return player
        return None


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="game where you have to find a number")
    parser.add_argument("minimum", type=int, help="minimum number of the game")
    parser.add_argument("maximum", type=int, help="maximum number of the game")
    parser.add_argument("--pseudo", type=str, help="optional pseudo of the player (if given the game will be saved)")
    args: argparse.ArgumentParser.parse_args = parser.parse_args()

    minimum: int = args.minimum
    maximum: int = args.maximum

    if maximum < minimum:
        min_temp: int = minimum
        minimum = maximum
        maximum = min_temp

    elif maximum == minimum:
        print("You have entered the same number for the min and the max")
        sys.exit()

    found: bool = False
    counter: int = 0
    number_random = random.randint(minimum, maximum)
    while not found:
        guess: str = ""
        while not check_number_input(guess):
            guess = input("Please enter a number :\n -> ")
        counter += 1
        if number_random == int(guess):
            print("You have won the game !!\n")
            if args.pseudo:
                save_game(args.pseudo, counter)
                print("Your game has been saved\n")
            found = True
        elif number_random < int(guess):
            print("You have entered a too big number\n")
        else:
            print("You have entered a too small number\n")


if __name__ == "__main__":
    main()
