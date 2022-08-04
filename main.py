#!/usr/bin/python

from urllib.request import Request, urlopen
from os import listdir, getcwd, remove, fsdecode, mkdir
from os.path import exists

NAME = "MCL"
VERSION = "0.0.1"
CWD = getcwd()

EXIT = "exit"
HELP = "help"
FIND = "find"
GET = "get"
LIST = "list"
DEL = "del"
UP = "up"
WIPE = "wipe"
WELCOME = f"Welcome to {NAME} version {VERSION}!"
HELP_SCREEN = f"""{NAME} v{VERSION}
    Commands:
    exit      --  Exits {NAME}.
    {HELP}    --  Prints help command.
    {FIND}    --  Finds a card from the internet.
    {GET}     --  Gets a card's saved data.
    {LIST}    --  Lists all cards saved.
    {UP}      --  Updates all cards saved.
    {DEL}     --  Deletes a saved card.
    {WIPE}    --  Wipes all saved cards.
    """

ERROR = "ERROR! Maybe you internet connection is off?"
HDR = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
SEARCH = "https://mavin.io/search?q="
DECODE = "utf-8"
OPEN = '"articleBody":'
CLOSE = '"image":'
CURRENCY_SIGN = "$"


def find(card, default=None):
    search_card_name = card.replace(" ", "+")
    url = f"{SEARCH}{search_card_name}"
    req = Request(url, headers=HDR)
    page = urlopen(req).read()

    avg_price = ERROR
    low_price = ERROR
    high_price = ERROR
   
    html = page.decode(DECODE)
    average_worth = html.find(OPEN)
    start_index = average_worth + len(OPEN)
    end_index = html.find(CLOSE)
    all_price = html[start_index:end_index]

    count = 0

    for word in all_price.split():
        if CURRENCY_SIGN in word:
            if count == 0:
                low_price = "LOW:" + word

            if count == 1:
                high_price = "HIGH:" + word

            if count == 2:
                avg_price = "AVG:" + word

            count += 1

    print(low_price)
    print(high_price)
    print(avg_price)

    if not exists(f"{CWD}/{card}") and avg_price != ERROR:
        save = input("ASK! Save this data? [y/N] ")

        if save == "y" or save == "Y" or save == "yes" or save == "Yes" or default != None:
            open(f"{CWD}/cards/{card}", "w").write(f"{avg_price}i\n{low_price}\n{high_price}") 

    return [low_price, high_price, avg_price]


def get(card):
    if exists(f"{CWD}/cards/{card}"):
        card_data = open(f"{CWD}/cards/{card}", "r").read()
        print(card_data)

    return card_data


def list_all():
    all_files = " | ".join(listdir(f"{CWD}/cards/"))
    print(" | ".join(listdir(f"{CWD}/cards/")))

    return all_files


def update():
    for file in listdir(f"{CWD}/cards/"):
        filename = fsdecode(file)
        find(filename, default=True)
        print("UPDATED!")


def delete_loc(card):
    are_you_sure = input("ASK! Are you sure you want to delete that card's data? [y/N] ")

    if are_you_sure == "y" or are_you_sure == "Y" or are_you_sure == "yes" or are_you_sure == "Yes" != None:
        remove(f"{CWD}/cards/{card}")


def wipe():
    are_you_sure = input("ASK! Are you sure you want to delete all your card data? [y/N] ")

    if are_you_sure == "y" or are_you_sure == "Y" or are_you_sure == "yes" or are_you_sure == "Yes" != None:
        for card in listdir(f"{CWD}/cards/"):
            remove(f"{CWD}/cards/{card}")
    
        print("WIPED!")


def shell():
    if not exists(f"{CWD}/cards"):
        mkdir(f"{CWD}/cards")

    while True:
        cmd = input("> ")
        head = cmd.split()[0].lower()
        body = " ".join(cmd.split()[1:])

        if head == EXIT:
            exit()

        if head == HELP:
            print(HELP_SCREEN)

        if head == FIND:
            find(body)

        if head == GET:
            get(body)

        if head == LIST:
            list_all()

        if head == UP:
            update()

        if head == DEL:
            delete_loc(body)

        if head == WIPE:
            wipe()


def main():
    print(WELCOME)
    shell()


if __name__ == "__main__":
    main()
