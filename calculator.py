import tkinter as tk

# Functions of buttons
def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

def equalpress():
    global expression
    try:
        total = str(eval(expression))
        equation.set(total)
        expression = total
    except:
        equation.set("Error")
        expression = ""

def clear():
    global expression
    expression = ""
    equation.set("")

def backspace():
    global expression
    expression = expression[:-1]
    equation.set(expression)

# For Buttons 
def animate_button(btn, action):
    original_bg = btn.cget("bg")
    original_font = btn.cget("font")

    btn.config(bg="#cccccc", font=("Arial", 16, "bold"))
    window.after(100, lambda: reset_button(btn, original_bg, original_font, action))

def reset_button(btn, original_bg, original_font, action):
    btn.config(bg=original_bg, font=original_font)
    action()

# GUI
window = tk.Tk()
window.title("Calculator")
window.geometry("320x500")
window.config(bg="#1e1e1e")
window.resizable(False, False)

expression = ""
equation = tk.StringVar()

entry = tk.Entry(
    window, textvariable=equation, font=('Arial', 28, 'bold'),
    bd=0, relief='flat', fg="white", bg="#1e1e1e", justify="right"
)
entry.pack(fill='both', ipadx=8, ipady=20, pady=(10, 0))

btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(expand=True, fill='both')

btns = [
    ("C", "#f6e58d", "#ffffff"),
    ("⌫", "#f6e58d", "#ffffff"),
    ("%", "#ff9f43", "#ffffff"),
    ("^", "#ff9f43", "#ffffff"),

    ("7", "#2e2e2e", "#ffffff"),
    ("8", "#2e2e2e", "#ffffff"),
    ("9", "#2e2e2e", "#ffffff"),
    ("/", "#ff9f43", "#ffffff"),

    ("4", "#2e2e2e", "#ffffff"),
    ("5", "#2e2e2e", "#ffffff"),
    ("6", "#2e2e2e", "#ffffff"),
    ("*", "#ff9f43", "#ffffff"),

    ("1", "#2e2e2e", "#ffffff"),
    ("2", "#2e2e2e", "#ffffff"),
    ("3", "#2e2e2e", "#ffffff"),
    ("-", "#ff9f43", "#ffffff"),

    ("0", "#2e2e2e", "#ffffff"),
    (".", "#2e2e2e", "#ffffff"),
    ("=", "#eccc68", "#ffffff"),
    ("+", "#ff9f43", "#ffffff"),
]
# Create buttons
row = 0
col = 0
for (text, bg, fg) in btns:
    if text == "C":
        action = clear
    elif text == "=":
        action = equalpress
    elif text == "⌫":
        action = backspace
    elif text == "^":  
        action = lambda t="**": press(t)
    else:
        action = lambda t=text: press(t)

    btn = tk.Button(
        btn_frame, text=text, font=("Arial", 18, "bold"),
        bg=bg, fg=fg, relief='flat', activebackground="#505050"
    )
    btn.config(command=lambda b=btn, a=action: animate_button(b, a))
    btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=15)

    col += 1
    if col > 3:
        col = 0
        row += 1

for i in range(6):
    btn_frame.grid_rowconfigure(i, weight=1)
    btn_frame.grid_columnconfigure(i, weight=1)

window.mainloop()