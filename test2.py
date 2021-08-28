from tkinter import *

# main
window = Tk()
window.title("Settlers of Catan Cards")

# create label
Label(window, text = "Joseph: ", font = "none 12").grid(row=0, column=0, sticky=W)

# show photo right next to previous label
photo1 = PhotoImage(file = "Icons/card_brick.png")
Label(window, image = photo1).grid(row=0, column=1, sticky=W)

photo2 = PhotoImage(file = "Icons/card_lumber.png")
Label(window, image = photo2).grid(row=0, column=2, sticky=W)

# start program
window.mainloop()