import tkinter as tk

root = tk.Tk()

root.title('Fractal Viewer')

canvas = tk.Canvas(root, width=1000, height=500)
canvas.grid(sticky=tk.NW, row=0, column=0)



root.mainloop()
