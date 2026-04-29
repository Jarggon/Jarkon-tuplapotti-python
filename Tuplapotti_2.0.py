import tkinter as tk
import random
import os
import pygame
import sys

#tarkistaa onko mac vai windows
if sys.platform == "darwin":
    try:
        from tkmacosx import Button
        tk.Button = Button
    except ImportError:
        print("tkmacosx not installed")

#tarkistaa onko .exe vai .py
if getattr(sys, 'frozen', False):
    base_folder = os.path.dirname(sys.executable)
else:
    base_folder = os.path.dirname(__file__)
    
#etsii tiedostot "jarkon settings" kansiosta
game_folder = os.path.join(base_folder, "jarkon settings")

if not os.path.exists(game_folder):
    os.makedirs(game_folder)

#äänet
pygame.mixer.init()

def load_sound(filename):

    path = os.path.join(game_folder, filename)

    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except FileNotFoundError:
        print(f"File not found {filename}")
        return None

sound_kela = load_sound("kela.mp3.mp3")
sound_spin = load_sound("reelspin.mp3.mp3")
sound_collect = load_sound("collect.mp3.mp3")
sound_smallwin = load_sound("smallwin.mp3.mp3")
sound_bigwin = load_sound("bigwin.mp3.mp3")
sound_doubling = load_sound("doubling.mp3.mp3")
sound_doubling_right = load_sound("doublingright.mp3.mp3")
sound_wrong = load_sound("wrong.mp3.mp3")

sound_work_list = [
            load_sound("work1.mp3"),
            load_sound("work2.mp3"),
            load_sound("work3.mp3"),
            load_sound("work4.mp3"),
            load_sound("work5.mp3"),
            load_sound("work6.mp3"),
            load_sound("work7.mp3"),
            load_sound("work8.mp3"),
            load_sound("work9.mp3"),
            load_sound("work10.mp3")]

def play_sound(sound_file, time_ms = 0, loop = False):
    if sound_file is not None:

        repetition = -1 if loop else 0

        if time_ms > 0:
            sound_file.play(loops = repetition, maxtime = time_ms)
        else:
            sound_file.play(loops = repetition)

def stop_sound(*sound_files):
    for sound in sound_files:
        if sound is not None:
            sound.stop()

#pelin asetukset ja muuttujat
symbols = ["🍒", "🍒", "🍊", "🍇", "🍏", "🍉", "💎", "🔔",]
doubling_symbols = ["👑", "🐈", "⚡"]
doubling_prosent = [48, 48, 4]
symbol_colours = {
    "🍒": "#FF0040",
    "🍊": "#FF8C00",
    "🍇": "#9370DB",
    "🍏": "#32CD32",
    "🍉": "#FF6347",
    "💎": "#00FFFF",
    "🔔": "#FFD700",
    "👑": "#FFD700",
    "🐈": "#DF630B",
    "⚡": "#008CFF" 
}
current_win = 0

def save_money():

    save_money_path = os.path.join(game_folder, "jarkonsaldo.txt")

    with open(save_money_path, "w") as file:
        file.write(str(round(money, 2)))

def load_money():

    save_money_path = os.path.join(game_folder, "jarkonsaldo.txt")

    try:
        with open(save_money_path, "r") as file:
            return round(float(file.read()), 2)
    except (FileNotFoundError, ValueError):
        return 100.00
money = load_money()

#minipelin asetukset ja muuttujat
work_clicks = 0
work_professions = [
    "DELIVER MAIL",
    "CUT THE GRASS",
    "SHELF SAUSAGES",
    "DRIVE A FORKLIFT",
    "FEED THE HORSES",
    "CLEAN THE TOILET",
    "SEND EMAILS",
    "WRITE A RAPORT",
    "SERVE BEER",
    "TORISÄÄTÖ",
    "SELL DRUGS",
    ]


def spin_button_pressed():

    global money, current_win

    spin.config(state=tk.DISABLED)
    win_amount.config(text="")
    error_output.config(text="")
    doubling_text.config(text="")
    
    if current_win > 0:
        collect_button_pressed()
        spin.config(state=tk.NORMAL)
        return

    try:
        bet_amount = float(bet_input.get())
        bet_as_cent = int(round(bet_amount * 100))

    except ValueError:
        error_output.config(text="Only numbers", fg="red")
        spin.config(state=tk.NORMAL)
        return

    if bet_amount > money:
        error_output.config(text="No balance", fg="red")
        spin.config(state=tk.NORMAL)
        return
    
    if  bet_amount < 0.20:
        error_output.config(text="Min bet 0.20$", fg="red")
        spin.config(state=tk.NORMAL)
        return
    
    if bet_as_cent % 20 != 0:
        error_output.config(text="Use 0.20$ steps", fg="red")
        spin.config(state=tk.NORMAL)
        return  

    money = round(money - bet_amount, 2)
    save_money()
    play_sound(sound_spin)
    wallet.config(text=f"BALANCE: {money:.2f}$")

    roll1 = random.choice(symbols)
    roll2 = random.choice(symbols)
    roll3 = random.choice(symbols)

    roll1_image.config(text="❓", fg="black")
    roll2_image.config(text="❓", fg="black")
    roll3_image.config(text="❓", fg="black")

    window.after(1000, lambda: roll1_image.config(text=f"{roll1}", fg=symbol_colours[roll1]))
    window.after(2000, lambda: roll2_image.config(text=f"{roll2}", fg=symbol_colours[roll2]))
    window.after(3000, lambda: roll3_image.config(text=f"{roll3}", fg=symbol_colours[roll3]))

    window.after(3000, lambda: check_win(roll1, roll2, roll3, bet_amount))

def check_win(roll1, roll2, roll3, bet_amount):
    global current_win

    if roll1 == roll2 == roll3 == "🔔":
        current_win = bet_amount * 50
    elif roll1 == roll2 == "🔔" or roll1 == roll3 == "🔔" or roll2 == roll3 == "🔔":
        current_win = bet_amount * 7
    elif roll1 == roll2 == roll3 == "💎":
        current_win = bet_amount * 25
    elif roll1 == roll2 == "💎" or roll1 == roll3 == "💎" or roll2 == roll3 == "💎":
        current_win = bet_amount * 4
    elif roll1 == roll2 == roll3 == "🍒":
        current_win = bet_amount
    elif roll1 == roll2 == "🍒" or roll1 == roll3 == "🍒" or roll2 == roll3 == "🍒":
        current_win = bet_amount * 0.2
    elif roll1 == roll2 == roll3 == "🍊":
        current_win = bet_amount * 7
    elif roll1 == roll2 == "🍊" or roll1 == roll3 == "🍊" or roll2 == roll3 == "🍊":
        current_win = bet_amount * 1.2
    elif roll1 == roll2 == roll3:
        current_win = bet_amount * 10
    elif roll1 == roll2 or roll1 == roll3 or roll2 == roll3:
        current_win = bet_amount * 1.6
    else:
        current_win = 0
        win_amount.config(text="NO WIN", fg="black")
        play_sound(sound_wrong)

    if current_win > 0:
        win_amount.config(text=f"WIN\n{current_win:.2f}$", fg="green")
        if current_win >= bet_amount * 50:
            big_win_output.config(text="🔔🔔🔔!!!JACKPOT!!!🔔🔔🔔")
        elif current_win >= bet_amount * 25:
            big_win_output.config(text="💎💎💎!!!MEGA WIN!!!💎💎💎")
        elif current_win >= bet_amount * 10:
            big_win_output.config(text="!!!BIG WIN!!!")

        if current_win >= bet_amount * 10:
            play_sound(sound_bigwin)
        else:
            play_sound(sound_smallwin)


    spin.config(state=tk.NORMAL)
    check_work_state()
    save_money()
        

def collect_button_pressed():
    
    global money, current_win

    stop_sound(sound_doubling, sound_doubling_right)
    double.config(state=tk.NORMAL)

    if current_win > 0:
        money = round(money + current_win, 2)
        wallet.config(text=f"BALANCE: {money:.2f}$")
        win_amount.config(text=f"COLLECTED\n{current_win:.2f}$", fg="blue")
        chance_text.config(text="")
        doubling_text.config(text="")
        big_win_output.config(text="💎💎💎=MEGA WIN! 🔔🔔🔔=JACKPOT!")
        heads.config(state=tk.DISABLED)
        tails.config(state=tk.DISABLED)
        current_win = 0
        check_work_state()
        save_money()
        play_sound(sound_collect)


def doubling_button_pressed():

    global money, current_win

    if current_win <= 0:
        return
    else:
        play_sound(sound_doubling, loop = True)
        double.config(state=tk.DISABLED)
        heads.config(state=tk.NORMAL)
        tails.config(state=tk.NORMAL)

        chance_text.config(text=f"CHANCE TO WIN\n{current_win*2:.2f}$", fg="green")
        doubling_text.config(text="👑 or 🐈", fg="#2927AE")
        

def tails_button_pressed():
    stop_sound(sound_doubling, sound_doubling_right)
    toss("🐈")

def heads_button_pressed():
    stop_sound(sound_doubling, sound_doubling_right)
    toss("👑")


def toss(player_choice):

    global current_win
    play_sound(sound_spin, 1500)

    if current_win <= 0:
        return
    
    heads.config(state=tk.DISABLED)
    tails.config(state=tk.DISABLED)
    
    doubling_result = random.choices(doubling_symbols, weights=doubling_prosent, k=1)[0]
    doubling_roll_image.config(text="❓", fg="black")

    window.after(1500, lambda: show_doubling_result(doubling_result, player_choice))


def show_doubling_result(doubling_result, player_choice):

    global current_win

    doubling_roll_image.config(text=doubling_result, fg=symbol_colours[doubling_result])


    if doubling_result == player_choice:
        play_sound(sound_doubling_right, loop = True)
        current_win *= 2
        win_amount.config(text=f"WIN\n{current_win:.2f}$", fg="green")
        chance_text.config(text=f"CHANCE TO WIN\n{current_win*2}$")
        heads.config(state=tk.NORMAL)
        tails.config(state=tk.NORMAL)

    else:
        current_win = 0
        win_amount.config(text="NO WIN", fg="black")
        chance_text.config(text="")
        doubling_text.config(text="")
        big_win_output.config(text="💎💎💎=MEGA WIN! 🔔🔔🔔=JACKPOT!")
        check_work_state()
        save_money()
        play_sound(sound_wrong)
        double.config(state=tk.NORMAL)

def kela_button_pressed():
    global money

    money = round(money + 10, 2)
    save_money()
    play_sound(sound_kela)
    wallet.config(text=f"BALANCE: {money:.2f}$")

    kela_button.config(state=tk.DISABLED)
    kela_timer(60)
    check_work_state()


def kela_timer(seconds):
    
    if seconds > 0:
        window.after(1000, lambda: kela_timer(seconds -1))
        kela_button.config(text=f"KELA {seconds}")
    else:
        kela_button.config(state=tk.NORMAL)
        kela_button.config(text="KELA")

def work_button_pressed():
    
    global work_clicks, work_professions

    work_start_button.config(state=tk.DISABLED)
    work_window = tk.Toplevel(window)
    work_window.title("Go to work")
    work_window.geometry("400x300")
    work_window.configure(bg="#2C3E50")
    work_window.transient(window)


    def stop_work():
        global work_clicks
        work_clicks = 0
        check_work_state()
        save_money()
        work_window.destroy()

    work_window.protocol("WM_DELETE_WINDOW", stop_work)

    #work ikkuna
    random_profession = random.choice(work_professions)
    work_title = tk.Label(work_window, text=f"{random_profession}", font=("Arial", 16, "bold"), bg="#2C3E50", fg="black")
    work_title.pack(pady=20)

    work_progress = tk.Label(work_window, text=f"{work_clicks} / 100",font=("Arial", 26, "bold"), bg="#2C3E50", fg="#F1C40F")
    work_progress.pack()

    def do_work():

        global work_clicks, money
        sound_work = random.choice(sound_work_list)
        play_sound(sound_work)

        work_clicks +=1
        work_progress.config(text=f"{work_clicks} / 100")

        if work_clicks % 2 == 0:
            work_window.configure(bg="#F1C40F")
            work_progress.config(bg="#F1C40F", fg="#2C3E50")
            work_title.config(bg="#F1C40F")
        else:
            work_window.configure(bg="#2C3E50")
            work_progress.config(bg="#2C3E50", fg="#F1C40F")
            work_title.config(bg="#2C3E50")

        if work_clicks == 100:
            money = round(money + 100, 2)
            save_money()
            wallet.config(text=f"BALANCE: {money:.2f}$")
            work_title.configure(text="You got paid 100$")
            work_button.config(text="EXIT WORK", command=stop_work)


    #työntekonappi
    work_button = tk.Button(work_window, text="WORK", font=("Arial", 20, "bold"), bg="#E74C3C", fg="white", command = do_work)
    work_button.pack(pady=30)

def check_work_state():
    if money + current_win <= 10:
        work_start_button.configure(state=tk.NORMAL)
    else:
        work_start_button.configure(state=tk.DISABLED)

#ikkuna
window = tk.Tk()
window.title("Jarkon Tuplapotti")
window.geometry("700x700")
window.minsize(600, 700)
window.configure(bg="darkred")

#otsikko
title = tk.Label(text="JARKON TUPLAPOTTI", font=("Arial", 20, "bold"), bg="red", bd=10, relief="raised")
title.pack(pady=20)

#big win
big_win_output = tk.Label(window, text="💎💎💎=MEGA WIN! 🔔🔔🔔=JACKPOT!", width=35, height=3, font=("Arial", 20, "bold"), bg="#DF8686", bd=10, relief="sunken")
big_win_output.pack()


#rullat
roll_frame = tk.Frame(window, bg="black", bd=10, relief="sunken")
roll_frame.pack(pady=(30, 10))

roll1_image = tk.Label(roll_frame, text="🔔", font=("Arial", 50), width=3, bg="white", fg=symbol_colours["🔔"], relief="ridge")
roll1_image.grid(row=0, column=0, padx=5)

roll2_image = tk.Label(roll_frame, text="🔔", font=("Arial", 50), width=3, bg="white", fg=symbol_colours["🔔"], relief="ridge")
roll2_image.grid(row=0, column=1, padx=5)

roll3_image = tk.Label(roll_frame, text="🔔", font=("Arial", 50), width=3, bg="white", fg=symbol_colours["🔔"], relief="ridge")
roll3_image.grid(row=0, column=2, padx=5)

doubling_roll_image = tk.Label(roll_frame, text="⚡", font=("Arial", 50), width=3, bg="white", fg=symbol_colours["⚡"], relief="ridge")
doubling_roll_image.grid(row=0, column=3, padx=5)

#voitto teksti
win_amount = tk.Label(roll_frame, width=14, height=2, text="WIN", font=("Arial", 10), bg="lightgray", bd=5, relief="sunken")
win_amount.grid(row=1, column=1, pady=20)

#tuplaus teksti
doubling_text = tk.Label(roll_frame, width=5, height=2, text="", font=("Arial", 10), bg="lightgray", bd=5, relief="sunken")
doubling_text.grid(row=1, column=3, padx=5)

#saatat voittaa teksti
chance_text = tk.Label(roll_frame, width=14, height=2, text="", font=("Arial", 10), bg="lightgray", bd=5, relief="sunken")
chance_text.grid(row=1, column=2, padx=5)

#lompakko teksti
wallet = tk.Label(window, text=f"BALANCE: {money:.2f}$", font=("Arial", 20), bg="lightgray", bd=5, relief="sunken")
wallet.pack(side="bottom", anchor="sw", padx=30, pady=15)

#kela nappi
kela_button = tk.Button(window, text="KELA", font=("Arial", 16, "bold"), bg="white", fg="#0033FF", bd=5, relief="sunken", state=tk.DISABLED, command=kela_button_pressed)
kela_button.place(relx=1, rely=1, x=-20, y=-15, anchor="se", width=120, height=45)

#töihin nappi
work_start_button = tk.Button(window, text="WORK", font=("Arial", 16, "bold"), bg="black", fg="white", bd=5, relief="sunken", command=work_button_pressed)
work_start_button.place(relx=1, rely=1, x=-160, y=-15, anchor="se", width=120, height=45)
check_work_state()

#slotin napit
button_frame = tk.Frame(window, bg="black", bd=10, relief="sunken")
button_frame.pack(side="bottom", pady=(10,0))

#pyöräytä
spin = tk.Button(button_frame, text="SPIN", font=("Arial", 12, "bold"), padx=16, pady=8, bg="#27AE60", fg="white", bd=5, relief="raised", command=spin_button_pressed)
spin.grid(row=0, column=3, padx=20)

#tuplaus
double = tk.Button(button_frame, text="DOUBLE", font=("Arial", 12, "bold"), padx=3, pady=8, bg="#2927AE", fg="white", bd=5, relief="raised", command=doubling_button_pressed)
double.grid(row=0, column=2, padx=20)

heads = tk.Button(button_frame, text="👑", font=("Arial", 12, "bold"), padx=26, pady=1, bg="#C2501F", fg="black", bd=5, relief="raised", command=heads_button_pressed, state=tk.DISABLED)
heads.grid(row=2, column=2)

tails = tk.Button(button_frame, text="🐈", font=("Arial", 12, "bold"), padx=26, pady=1, bg="#C2501F", fg="black", bd=5, relief="raised", command=tails_button_pressed, state=tk.DISABLED)
tails.grid(row=2, column=3)

#kerää voitot
collect = tk.Button(button_frame, text="COLLECT", font=("Arial", 12, "bold"), padx=0, pady=8, bg="#E5DB14", fg="white", bd=5, relief="raised", command=collect_button_pressed)
collect.grid(row=0, column=1, padx=20)

#panos
bet_input = tk.Entry(button_frame, width=7, bg="lightgray", bd=3, relief="sunken")
bet_input.grid(row=1, column=4)
bet_input.insert(0, "1")

bet_label = tk.Label(button_frame, text="BET $", bg="lightgray", bd=1, relief="sunken")
bet_label.grid(row=0, column=4, padx=40)

#error output
error_output = tk.Label(button_frame, width=14, text="", bg="lightgray", bd=1, relief="sunken")
error_output.grid(row=2, column=4)

kela_timer(60)
window.mainloop()