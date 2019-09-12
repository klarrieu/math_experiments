import numpy as np
from PIL import Image

def mandelbrot(z0, trap_size, iters=10):
    """
    Iterates Mandelbrot set recursive function
    :param z0: initial complex number
    :param iters: number of iterations
    :param trap_size: 1/2 side lengths of rectangle in complex plane centered at origin for orbit trap

    :return: final complex number within trap
    """
    # iteration number
    i = 1
    # initial z
    z = z0
    # initialize output z
    z_out = z0

    while i < iters:
        z = z**2 + z0
        if abs(z.real) <= trap_size[0] and abs(z.imag) <= trap_size[1]:
            z_out = z
        i += 1

    return z_out

def closest(arr, val):
    return min(arr, key=lambda x: abs(x - val))

# apply orbit trap coloring
def apply_orbit_trap(iter_func, img_path, trap_size=(2,2)):
    print('reading image...')
    img = Image.open(img_path)
    width, height = img.size

    z_reals = np.linspace(-trap_size[0], trap_size[0], width)
    z_imags = np.linspace(-trap_size[1], trap_size[1], height)

    z_ins = [z_r + z_i*1j for z_r in z_reals for z_i in z_imags]

    print('applying iteration...')
    z_outs = list(map(lambda x: iter_func(x, trap_size=trap_size), z_ins))

    print('matching grid cells...')
    # for each z_out, find closest location in pixel grid
    z_outs = list(zip([closest(z_reals, z_out.real) for z_out in z_outs],
                      [closest(z_imags, z_out.imag) for z_out in z_outs]))

    # get corresponding image pixel value ***

    print('mapping pixels...')
    pix = img.load()  # load input pixel map
    out_pix = np.asarray(img)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            out_pix[i, j] = 

    print('saving image...')



img_path = 'C:\\Users\\klarrieu\\Desktop\\math_experiments\\ripleysqw.png'
apply_orbit_trap(mandelbrot, img_path)

