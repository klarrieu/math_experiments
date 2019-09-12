import numpy as np
from PIL import Image

def mandelbrot(z0, trap_size, iters=10, deg=2):
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
        z = z**deg + z0
        if abs(z.real) <= trap_size[0] and abs(z.imag) <= trap_size[1]:
            z_out = z
        i += 1

    return z_out


"""
def closest(arr, val):
    return min(arr, key=lambda x: abs(x - val))
"""


def apply_orbit_trap(iter_func, img_path, trap_size=(2,2)):
    print('reading image...')
    img = Image.open(img_path)
    width, height = img.size

    # left to right, top to bottom
    # real and imaginary components in complex plane of initial points (corresponding to pixel centers)
    z_reals = np.linspace(-trap_size[0], trap_size[0], width)
    z_imags = np.linspace(trap_size[1], -trap_size[1], height)

    # complex number inputs to iterate
    z_ins = [z_r + z_i*1j for z_r in z_reals for z_i in z_imags]

    # step sizes in x and y directions in complex plane between pixel centers
    x_step = z_reals[1] - z_reals[0]
    y_step = abs(z_imags[1] - z_imags[0])

    print('applying iteration...')
    z_outs = list(map(lambda x: iter_func(x, trap_size=trap_size), z_ins))

    print('matching grid cells...')
    # for each z_out, find closest location in pixel grid
    """
    z_outs = list(zip([closest(z_reals, z_out.real) for z_out in z_outs],
                      [closest(z_imags, z_out.imag) for z_out in z_outs]))
    """
    z_outs = list(zip([x_step * round((z_out.real - trap_size[0])/x_step) + trap_size[0] for z_out in z_outs],
                      [y_step * round((z_out.imag - trap_size[1]) / y_step) + trap_size[1] for z_out in z_outs]))

    print('writing output...')
    # get corresponding array index from input image ***
    i_0s = [int((z[0] + trap_size[0])/x_step) for z in z_outs]
    j_0s = [int((z[1] - trap_size[1])/y_step) for z in z_outs]

    # out_coords[i * width + j] = coordinates in orbit trap for starting coord i, j
    coord_0s = list(zip(i_0s, j_0s))
    # match to initial pixel values
    pix = img.load()
    pix_0s = [pix[coord[0], coord[1]] for coord in coord_0s]
    pix_0s = np.reshape(pix_0s, (width, height, 3))

    out_img = Image.new('RGB', (width, height), "black")  # create a new black image
    out_pix = out_img.load()  # create the pixel map

    for i in range(width):
        for j in range(height):
            out_pix[i, j] = tuple(pix_0s[i, j])

    print('saving image...')
    out_img.save("mandelbrot_test2.png")
    print('done.')


img_path = 'input.jpg'
apply_orbit_trap(lambda x: mandelbrot(x, deg=7), img_path)

