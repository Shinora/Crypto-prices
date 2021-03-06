import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
import threading

root = tk.Tk()
root.title("Crypto Prices")

tk.Label(root, text="\n").pack()
exit_button = tk.Button(root, text="Exit", command=root.quit, padx=50, pady=5, bg='light grey', border=5)
exit_button.pack()


def set_up():
    global money_chosen

    money_chosen = tk.StringVar(root)

    choices = {'bitcoin', 'monero', 'ethereum', 'litecoin', 'iota', 'neo', 'ripple', 'cardano', 'dash', 'bitcoin-cash',
               'zcash'}

    money_chosen.set('bitcoin')

    popupMenu = tk.OptionMenu(root, money_chosen, *choices)

    global monney
    monney = money_chosen.get()

    tk.Label(root, text="Choose a money").pack()

    popupMenu.pack()

    page = requests.get(str("https://courscryptomonnaies.com/" + str(money_chosen.get())))
    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.find('span', class_='').get_text()

    global price_frame
    price_frame = tk.Frame(padx=85, pady=30)

    global price
    price = tk.Label(price_frame, text=found)


found = ''


def refresh():
    global found
    global money_chosen
    page = requests.get(str("https://courscryptomonnaies.com/" + str(money_chosen.get())))
    soup = BeautifulSoup(page.content, 'html.parser')

    found = soup.find('span', class_='').get_text()

    return found


def write():
    global price

    global found
    money = money_chosen.get()
    str1 = ("The current price of " + str(money) + " is " + found)
    price.destroy()
    price = tk.Label(price_frame, text=str1)
    price.config(font=(54))
    price_frame.pack()
    price.pack()
    print("The current price of " + str(money) + " is " + found)
    return found


def remove():
    price.pack_forget()
    price_frame.pack_forget()


def app():
    set_up()
    oldresults = None
    results = write()
    refresh()
    while (True):
        results = write()

        refresh()
        while (results == oldresults):
            time.sleep(.1)
            oldresults = results
            refresh()
            time.sleep(.1)

    remove()

threading.Thread(target=app).start()


tk.mainloop()