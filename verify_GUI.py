from tkinter import *
import random

# click function
def click():
    entered_text = textentry.get()

    output.delete(0.0, END)

    print(solution)

    if int(entered_text) == solution:
        output.insert(END, "Correct")
    else:
        output.insert(END, "Wrong")


# main
window = Tk()
window.title("Check Answer")

# generate a random number
solution = random.randint(0, 9)

# tell person to guess number
Label(window, text = "Guess a number").grid(row=0, column=0)

# create entry box
textentry = Entry(window)
textentry.grid(row=0, column=1)

# create submit button
Button(window, text = "SUBMIT", width = 6, command = click).grid(row=0, column=2)

# create output box
output = Text(window, width = 75, height = 6, wrap = WORD)
output.grid(row=1, column=0, columnspan=3)

# run the window
window.mainloop()