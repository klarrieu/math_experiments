import tkinter as tk
import tkinter.ttk as ttk
import fractal_cuda as fcuda
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FractalViewer(object):
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Fractal Viewer')

        self.cmaps = list(plt.cm.datad.keys())

        # setup canvas
        self.fig = Figure()
        self.fig1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()
        # select fractal type
        self.l_frac_type = tk.Label(self.control_frame, text='Fractal type:')
        self.l_frac_type.grid(sticky=tk.W, row=1, column=0)
        self.c_frac_type = ttk.Combobox(self.control_frame, values=['Mandelbrot'], state='readonly')
        self.c_frac_type.current(0)
        self.c_frac_type.grid(sticky=tk.W, row=1, column=1)

        # select colormap
        self.l_cmap = tk.Label(self.control_frame, text='color map:')
        self.l_frac_type.grid(sticky=tk.W, row=2, column=0)
        self.c_cmap = ttk.Combobox(self.control_frame, values=self.cmaps, state='readonly')
        self.c_cmap.current(self.cmaps.index('seismic_r'))
        self.c_cmap.grid(sticky=tk.W, row=2, column=1)
        self.c_cmap.bind('<<ComboboxSelected>>', self.update_cmap)

        # select orbit trap
        self.l_otrap = tk.Label(self.control_frame, text='orbit trap:')
        self.l_otrap.grid(sticky=tk.W, row=3, column=0)
        self.c_otrap = ttk.Combobox(self.control_frame, values=['magnitude'], state='readonly')
        self.c_otrap.current(0)
        self.c_otrap.grid(sticky=tk.W, row=3, column=1)

        # zoom level
        self.l_zoom = tk.Label(self.control_frame, text='zoom:')
        self.l_zoom.grid(sticky=tk.W, row=4, column=0)
        self.s_zoom = tk.Spinbox(self.control_frame, from_=1, to=1e9, command=self.update_zoom)
        self.s_zoom.grid(sticky=tk.W, row=4, column=1)

        # navigation buttons
        self.b_up = tk.Button(self.control_frame, text='↑', command=self.update_up)
        self.b_up.grid(row=5, column=5)
        self.b_down = tk.Button(self.control_frame, text='↓', command=self.update_down)
        self.b_down.grid(row=7, column=5)
        self.b_left = tk.Button(self.control_frame, text='←', command=self.update_left)
        self.b_left.grid(row=6, column=4)
        self.b_right = tk.Button(self.control_frame, text='→', command=self.update_right)
        self.b_right.grid(row=6, column=6)

        # initialize image
        self.cmap = self.c_cmap.get()
        self.zoom = 1
        self.centerX = -0.5
        self.centerY = 0
        self.update_image()

        # launch GUI
        self.root.mainloop()

    def update_fractal_type(self):
        print('under construction')

    def update_orbit_trap(self):
        print('under construction')

    def update_image(self):
        # updates image when navigation changes
        self.gimage = fcuda.generate_img(centerX=self.centerX, centerY=self.centerY, zoom=self.zoom, iters=20*self.zoom)
        self.fig1.cla()
        self.fig1.imshow(self.gimage, cmap=self.cmap)
        self.canvas.draw()

    def update_cmap(self, event):
        # update colormap without recomputing image
        self.cmap = self.c_cmap.get()
        self.fig1.cla()
        self.fig1.imshow(self.gimage, cmap=self.cmap)
        self.canvas.draw()

    def update_zoom(self):
        # update zoom level
        self.zoom = float(self.s_zoom.get())
        self.update_image()

    def update_left(self):
        # update when left button pressed
        self.centerX -= 0.1 / (self.zoom ** 2)
        self.update_image()

    def update_right(self):
        self.centerX += 0.1 / (self.zoom ** 2)
        self.update_image()

    def update_up(self):
        self.centerY -= 0.1 / (self.zoom ** 2)
        self.update_image()

    def update_down(self):
        self.centerY += 0.1 / (self.zoom ** 2)
        self.update_image()

if __name__ == '__main__':
    FractalViewer()
