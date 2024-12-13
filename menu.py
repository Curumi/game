from tkinter import *
from pickle import load, dump

# Menu functions
def resume_game():
    menu_window.withdraw()
    window.deiconify()

def new_game():
    global game_over, pause, x1, y1, x2, y2
    game_over = False
    pause = False
    x1, y1 = 50, 50
    x2, y2 = x1, y1 + player_size + 100
    canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
    canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
    canvas.itemconfig(text_id, text="Вперед!")
    resume_game()

def save_game():
    with open("save.pkl", "wb") as f:
        dump((x1, y1, x2, y2, game_over, pause), f)
    menu_window.withdraw()
    window.deiconify()

def load_game():
    global x1, y1, x2, y2, game_over, pause
    with open("save.pkl", "rb") as f:
        x1, y1, x2, y2, game_over, pause = load(f)
    canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
    canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
    set_status()

def exit_game():
    window.destroy()
    menu_window.destroy()

# Game functions
def set_status():
    global game_over, pause
    if game_over:
        status_text = "Игра окончена!"
    elif pause:
        status_text = "Пауза"
    else:
        status_text = "Игра идет"
    canvas.itemconfig(text_id, text=status_text)

def pause_toggle():
    global pause
    pause = not pause
    set_status()

def key_handler(event):
    global x1, y1, x2, y2, game_over
    if event.keycode == KEY_ESC:
        window.withdraw()
        menu_window.deiconify()
    elif event.keycode == KEY_PAUSE:
        pause_toggle()
    elif not pause and not game_over:
        if event.keycode == KEY_PLAYER1:  # Для игрока 1
            canvas.move(player1, SPEED, 0)
            x1 += SPEED
        elif event.keycode == KEY_PLAYER2:  # Для игрока 2
            canvas.move(player2, SPEED, 0)
            x2 += SPEED

        check_finish()

def check_finish():
    global game_over, x1, x2
    x1_end = canvas.coords(player1)[2]  # Правая граница первого игрока
    x2_end = canvas.coords(player2)[2]  # Правая граница второго игрока

    if x1_end >= x_finish:
        canvas.itemconfig(text_id, text="Игрок 1 победил!")
        game_over = True
        set_status()
    elif x2_end >= x_finish:
        canvas.itemconfig(text_id, text="Игрок 2 победил!")
        game_over = True
        set_status()

# Global variables
game_width = 800
game_height = 800

KEY_UP = 87
KEY_DOWN = 83
KEY_ESC = 27
KEY_ENTER = 13

player_size = 100
x1, y1 = 50, 50
x2, y2 = x1, y1 + player_size + 100
player1_color = 'red'
player2_color = 'blue'

x_finish = game_width - 50

KEY_PLAYER1 = 39 #Правая стрелка
KEY_PLAYER2 = 68 #D
KEY_PAUSE = 19 #Pause/Break

SPEED = 12

game_over = False
pause = False

# Create game window
window = Tk()
window.title('Игра')
window.withdraw()

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()

player1 = canvas.create_rectangle(x1,
                                  y1,
                                  x1 + player_size,
                                  y1 + player_size,
                                  fill=player1_color)
player2 = canvas.create_rectangle(x2,
                                  y2,
                                  x2 + player_size,
                                  y2 + player_size,
                                  fill=player2_color)
finish_id = canvas.create_rectangle(x_finish,
                                    0,
                                    x_finish + 10,
                                    game_height,
                                    fill='black')

text_id = canvas.create_text(x1,
                             game_height - 50,
                             anchor=SW,
                             font=('Arial', '25'),
                             text='Вперед!')

window.bind('<KeyRelease>', key_handler)

# Create menu window
menu_window = Tk()
menu_window.title('Меню игры')
menu_window.geometry('800x800')

menu_canvas = Canvas(menu_window, width=800, height=800, bg='white')
menu_canvas.pack()

menu_text = menu_canvas.create_text(400, 100, font=('Arial', '25'), text='Меню игры')

options = ['Возврат в игру', 'Новая игра', 'Сохранить', 'Загрузить', 'Выход']
option_ids = []
for i, option in enumerate(options):
    option_id = menu_canvas.create_text(400, 150 + i * 50, font=('Arial', '25'), text=option)
    option_ids.append(option_id)

selected_option = 0
menu_canvas.itemconfig(option_ids[selected_option], fill='blue')

def menu_key_handler(event):
    global selected_option
    if event.keycode == KEY_UP:
        selected_option = (selected_option - 1) % len(options)
    elif event.keycode == KEY_DOWN:
        selected_option = (selected_option + 1) % len(options)
    elif event.keycode == KEY_ENTER:
        if options[selected_option] == 'Возврат в игру':
            resume_game()
        elif options[selected_option] == 'Новая игра':
            new_game()
        elif options[selected_option] == 'Сохранить':
            save_game()
        elif options[selected_option] == 'Загрузить':
            load_game()
        elif options[selected_option] == 'Выход':
            exit_game()
    for i, option_id in enumerate(option_ids):
        if i == selected_option:
            menu_canvas.itemconfig(option_id, fill='blue')
        else:
            menu_canvas.itemconfig(option_id, fill='black')


menu_window.bind('<KeyRelease>', menu_key_handler)
menu_window.mainloop()