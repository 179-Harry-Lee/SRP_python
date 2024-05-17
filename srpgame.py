
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint  
 

# Kết nối với sqlite
conn = sqlite3.connect('game_users.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')
conn.commit()

c.execute('''
CREATE TABLE IF NOT EXISTS scores (
    player_id INTEGER,
    score INTEGER,
    FOREIGN KEY(player_id) REFERENCES users(id)
)
''')
conn.commit()


window = Tk()
window.title("Game Keo Bua Bao")
window.configure(background="black")

global player_id
player_id = None
def login(username, password, login_window):
    c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    if user:
        global player_id
        player_id, player_name = user
        player_indicator.config(text=player_name)
        login_window.destroy()
    else:
        Label(login_window, text="Tài khoản hoặc mật khẩu sai nha !!!").grid(row=3, column=1)
        

def register(username, password, register_window):
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        # Lấy Id người chơi mới
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = c.fetchone()[0]
        # Thêm id người chơi vào db score để tính điểm
        c.execute('INSERT INTO scores (player_id, score) VALUES (?, 0)', (user_id,))
        conn.commit()
        register_window.destroy()
        show_login_form() 
    except sqlite3.IntegrityError:
        Label(register_window, text="Username already exists!").grid(row=3, column=1)

def show_login_form():
    login_window = Toplevel(window)
    login_window.title("Login")

    login_window.grab_set()
    login_window.attributes('-topmost', True)  # This line makes the login_window appear on top of all other windows

    Label(login_window, text="Tài khoản:").grid(row=0, column=0)
    username_entry = Entry(login_window)
    username_entry.grid(row=0, column=1)

    Label(login_window, text="Mật khẩu:").grid(row=1, column=0)
    password_entry = Entry(login_window, show='*')
    password_entry.grid(row=1, column=1)

    Button(login_window, text="Đăng nhập", command=lambda: login(username_entry.get(), password_entry.get(), login_window)).grid(row=2, column=1)
    Button(login_window, text="Đăng ký", command=lambda: [login_window.destroy(), show_register_form()]).grid(row=2, column=0)

    
def show_register_form():
    register_window = Toplevel(window)
    register_window.title("Register")
    
    Label(register_window, text="Tài khoản:").grid(row=0, column=0)
    username_entry = Entry(register_window)
    username_entry.grid(row=0, column=1)
    
    Label(register_window, text="Mật khẩu:").grid(row=1, column=0)
    password_entry = Entry(register_window, show='*')
    password_entry.grid(row=1, column=1)
    
    Button(register_window, text="Đăng ký", command=lambda: register(username_entry.get(), password_entry.get(), register_window)).grid(row=2, column=1)


# Đăng xuất
def logout():
    player_indicator.config(text="")
    computer_score.config(text="0")
    player_score.config(text="0")
    show_login_form()



# Chỉnh kích cở các hình ảnh quy về một kích cở chung
desired_size = (250, 100)

#Load Hình ảnh
#Hình Player
image_rock1 = ImageTk.PhotoImage(Image.open("bua.png").resize(desired_size))

image_paper1 = ImageTk.PhotoImage(Image.open("bao.png").resize(desired_size))

image_scissors1 = ImageTk.PhotoImage(Image.open("keo.png").resize(desired_size))


#Hình Computer
image_rock2 = ImageTk.PhotoImage(Image.open("bua.png").resize(desired_size))

image_paper2 = ImageTk.PhotoImage(Image.open("bao.png").resize(desired_size))

image_scissors2 = ImageTk.PhotoImage(Image.open("keo.png").resize(desired_size))




#Tạo khung hình  hiện thị kéo,búa,bao
label_player = Label(window, image=image_scissors1)
label_computer = Label(window, image=image_scissors2)
label_computer.grid(row=1,column=1)
label_player.grid(row=1,column= 5)


#Tạo khung hình hiện thị bàn thắng
computer_score = Label(window,text=0,font=('arial',60,"bold"),fg ="red")
player_score = Label(window,text=0,font=('arial',60,"bold"),fg="red")
computer_score.grid(row=1,column=2)
player_score.grid(row=1,column=4)

#Hiện thị Tên "Player" trên đầu tỉ số
player_name = show_login_form()  # Hiện tên theo tên của player
player_indicator = Label(window, font=("arial", 40, "bold"), text=player_name, bg="orange", fg="blue")
player_indicator.grid(row=0, column=4)


#Hiện thị Tên "Computer" trên đầu tỉ số
computer_indicator = Label(window,font=("arial",40,"bold"),text="Computer",bg ="orange",fg="blue")

computer_indicator.grid(row=0,column=2)


#Hiện thị thông báo
def updateMessage(a):
    final_message['text'] = a   


#Thêm Tỉ số vào cho computer
def Computer_Update():
    final = int(computer_score['text'])
    final += 1
    computer_score['text'] = str(final)

#Thêm tỉ số vào cho player
def Player_Update():
    final = int(player_score['text'])
    final += 1
    player_score['text'] = str(final)
    c.execute('UPDATE scores SET score = ? WHERE player_id = ?', (final, player_id))
    conn.commit()



# Xử lý trò chơi
def winner_check(p,c):
    if p == c:
        updateMessage("Huề")
    elif p =="Búa":
        if c == "Bao":
            updateMessage("Máy Thắng!!!")
            Computer_Update()

        else:
            updateMessage("Người chơi thắng!!!")
            Player_Update()

    elif p =="Bao":
        if c == "Kéo":
            updateMessage("Máy Thắng!!!")
            Computer_Update()
        else:
            updateMessage("Người chơi thắng!!!")
            Player_Update()
    elif p == "Kéo":
        if c=="Búa":
            updateMessage("Máy Thắng!!!")
            Computer_Update()
        else:
            updateMessage("Người chơi thắng!!!")
            Player_Update()
    else: 
        pass


to_select = ["Kéo", "Búa","Bao"]


# Xử lý nút bấm
def choice_update(a):

    choice_computer = to_select[randint(0,2)]
    if choice_computer == "Búa":
        label_computer.configure(image = image_rock2)
    
    elif choice_computer == "Bao":
        label_computer.configure(image = image_paper2)
    
    else:
        label_computer.configure(image = image_scissors2)



    if a == "Búa":
        label_player.configure(image = image_rock1)

    elif a == "Bao":
        label_player.configure(image = image_paper1)

    else:
        label_player.configure(image = image_scissors1)

    winner_check(a,choice_computer)



final_message = Label(window,font=("arial",20,"bold"),bg="red",fg="white")
final_message.grid(row=5,column=3)





# Tạo nút bấm
button_rock = Button(window, width = 16, height=3,text="Búa",font=("arial",20,"bold"),bg = "Green",fg="red",command=lambda:choice_update("Búa")).grid(row=4,column=2)

button_paper = Button(window, width = 16, height=3,text="Bao",font=("arial",20,"bold"),bg = "pink",fg="black",command=lambda:choice_update("Bao")).grid(row=4,column=3)

button_scissors = Button(window, width = 16, height=3,text="Kéo",font=("arial",20,"bold"),bg = "blue",fg="white",command=lambda:choice_update("Kéo")).grid(row=4,column=4)

#show tỉ số
def show_scores():
    c.execute('SELECT username, score FROM users JOIN scores ON users.id = scores.player_id')
    scores = c.fetchall()
    score_message = "\n".join([f"{username}: {score}" for username, score in scores])
    messagebox.showinfo("Scores", score_message)

# Tạo memu
menu_bar = Menu(window)
window.config(menu=menu_bar)

# tạo các option trong menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tùy chọn", menu=file_menu)
file_menu.add_command(label="Đăng xuất", command=logout)
file_menu.add_command(label="Xem tỉ số", command=show_scores)

window.mainloop()