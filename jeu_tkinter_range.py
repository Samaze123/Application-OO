import random
from tkinter import *
from tkinter import font


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


url: str = "games_saved.txt"


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


class Window:
    def __init__(self) -> None:
        self.number_random: int = 0
        self.counter_guess: int = 0
        self.window_range: Tk | None = None
        self.label_error_range_message: StringVar | None = None
        self.window: Tk | None = None
        self.button_reset: Button | None = None
        self.maximum: int | StringVar = 0
        self.minimum: int | StringVar = 0
        self.number_entered: int | StringVar = 0
        self.police: str = "courier 15"
        self.title: str = "Guess the right number"
        self.pseudo: str | StringVar = ""
        self.reset_game()

    def reset_game(self, window_to_destroy: Tk | None = None):
        self.number_random: int = 0
        self.counter_guess: int = 0
        self.number_entered: int | StringVar = 0
        if window_to_destroy:
            window_to_destroy.destroy()
        self.window_range = Tk()
        self.window_range.title("Get the range")
        self.window_range.option_add("*Font", self.police)
        self.minimum: StringVar = StringVar()
        self.maximum: StringVar = StringVar()
        self.pseudo: StringVar = StringVar()
        for i in range(3):
            self.window_range.columnconfigure(i, weight=1)
        for i in range(4):
            self.window_range.rowconfigure(i, weight=1)
        label_pseudo: Label = Label(self.window_range, text="Enter your pseudo (optional) : ")
        label_pseudo.grid(column=0, row=0)
        entry_pseudo: Entry = Entry(self.window_range, textvariable=self.pseudo)
        entry_pseudo.grid(column=1, row=0)
        label_minimum: Label = Label(self.window_range, text="Enter the minimum : ")
        label_minimum.grid(column=0, row=1)
        entry_minimum: Entry = Entry(self.window_range, textvariable=self.minimum)
        entry_minimum.grid(column=1, row=1)
        label_maximum: Label = Label(self.window_range, text="Enter the maximum : ")
        label_maximum.grid(column=0, row=2)
        entry_maximum: Entry = Entry(self.window_range, textvariable=self.maximum, )
        entry_maximum.grid(column=1, row=2)
        button_accept_game: Button = Button(self.window_range, text="Accept",
                                            command=lambda: self.validate_range(self.minimum.get(), self.maximum.get()))
        button_accept_game.grid(column=2, row=0, rowspan=2)
        self.window_range.mainloop()

    def validate_range(self, minimum: str, maximum: str):
        text = ""
        if maximum.isdigit() and minimum.isdigit():
            maximum = int(maximum)
            minimum = int(minimum)
            if maximum > minimum:
                self.number_random = random.randint(minimum, maximum)
                self.create_basic_window(self.window_range)
                return
            text = "Please enter max > min"
        else:
            text = "Please enter correct numbers"
        label_error_range: Label = Label(self.window_range, text=text)
        label_error_range.grid(column=0, row=2, columnspan=3)

    def guess(self):
        text = ""
        if self.number_entered.get().isdigit():
            number_entered: int = int(self.number_entered.get())
            self.counter_guess += 1
            if number_entered < self.number_random:
                text = "the number is too small"
            elif number_entered > self.number_random:
                text = "the number is too big"
            else:
                text = "you win the game !!"
                if self.pseudo.get():
                    save_game(self.pseudo.get(), self.counter_guess)
        else:
            text = "please enter a number"
        label_info: Label = Label(self.window, text=text)
        label_info.grid(row=0, column=1, sticky=NSEW)

    # The main display function for the application.
    def create_basic_window(self, window_to_destroy: Tk) -> None:
        window_to_destroy.destroy()
        self.window: Tk = Tk()
        self.window.title(self.title)
        self.window.option_add("*Font", self.police)
        self.window.config(bg="white")

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)

        for i in range(4):
            self.window.rowconfigure(i, weight=1)

        button_exit: Button = Button(self.window, text="Exit", command=self.window.destroy,
                                     font=font.Font(family='Helvetica', size=15, weight='bold'))
        button_exit.grid(column=2, row=0, sticky=NSEW)
        label_entry: Label = Label(self.window, text="Enter a number :")
        label_entry.grid(column=0, row=1, sticky=NSEW)
        self.number_entered = StringVar()
        entry_number: Entry = Entry(self.window, textvariable=self.number_entered, relief=RAISED)
        entry_number.grid(column=1, row=1, sticky=NSEW)
        button_guess: Button = Button(self.window, text="Guess the number", command=self.guess)
        button_guess.grid(column=2, row=1, sticky=NSEW)
        button_reset: Button = Button(self.window, text="Reset", command=lambda: self.reset_game(self.window),
                                      font=font.Font(family='Helvetica', size=15, weight='bold'))
        button_reset.grid(column=0, row=3, sticky=NSEW)
        self.window.mainloop()


# It will launch the application
Window()
