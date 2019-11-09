import tkinter as tk
import tkinter.ttk as ttk
import fractal_cuda as fcuda


class FractalViewer(object):
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Fractal Viewer')

        self.frac_creator = fcuda.FractalCreator()

        # setup canvas
        canvas = tk.Canvas(self.root, width=1000, height=500)
        canvas.grid(sticky=tk.NW, row=0, column=0, columnspan=12)

        # select fractal type
        self.l_frac_type = tk.Label(self.root, text='Fractal type:')
        self.l_frac_type.grid(sticky=tk.W, row=1, column=0)
        self.c_frac_type = ttk.Combobox(self.root, values=['Mandelbrot'])
        self.c_frac_type.current(0)
        self.c_frac_type.grid(sticky=tk.W, row=1, column=1)

        # select colormap
        self.l_cmap = tk.Label(self.root, text='color map:')
        self.l_frac_type.grid()
        self.c_cmap = ttk.Combobox()
        self.c_cmap.current(0)
        self.c_cmap.grid()

        # select orbit trap
        self.l_otrap = tk.Label(self.root, text='orbit trap:')
        self.l_otrap.grid()
        self.c_otrap = ttk.Combobox()
        self.c_otrap.current(0)
        self.c_otrap.grid()

        # navigation buttons
        self.b_up = tk.Button(self.root)
        self.b_up.grid()
        self.b_down = tk.Button(self.root)
        self.b_down.grid()
        self.b_left = tk.Button(self.root)
        self.b_left.grid()
        self.b_right = tk.Button(self.root)
        self.b_right.grid()

        # launch GUI
        self.root.mainloop()

    def update_fractal_type(self):
        print('under construction')

    def update_orbit_trap(self):
        print('under construction')

    def update_image(self):
        # updates image when navigation changes
        print('under construction')
        self.frac_creator.generate_img()

    def update_cmap(self):
        # update colormap without recomputing image
        print('under construction')

FractalViewer()
