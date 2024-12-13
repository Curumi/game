from tkinter import *
from pickle import load, dump



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
        window.destroy()
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

# область функций

# область глобальных переменных
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







game_width = 800
game_height = 800
window = Tk()
window.title('Меню игры')

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()
#menu_create(canvas)
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
window.mainloop()