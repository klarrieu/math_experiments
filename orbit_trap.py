import numpy as np
from PIL import Image
import pathos
from pathos.multiprocessing import ProcessingPool


def mandelbrot(z0, trap_size, iters=1000, deg=3, **kwargs):
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
        if (z.real**2 + z.imag**2) ** 0.5 > 1e3:  # safe to assume diverged at this point for most IFSs
            break

    return z_out


def julia(z0, trap_size, iters=100, deg=2, c=0.618):
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
        z = z**deg + c
        if abs(z.real) <= trap_size[0] and abs(z.imag) <= trap_size[1]:
            z_out = z
        i += 1
        if np.absolute(z) > 1e3:  # safe to assume diverged at this point for most IFSs
            break

    return z_out


def apply_orbit_trap(iter_func, img_path, trap_size=(2, 2)):
    print('reading image...')
    img = Image.open(img_path)
    res = int(1024 * 8)
    img = img.resize((res, int(res*5/4)))
    width, height = img.size

    # left to right, top to bottom
    # real and imaginary components in complex plane of initial points (corresponding to pixel centers)
    z_reals = np.linspace(-trap_size[0], trap_size[0], width)
    z_imags = np.linspace(-trap_size[1], trap_size[1], height)

    # complex number inputs to iterate
    z_ins = [z_r + z_i*1j for z_r in z_reals for z_i in z_imags]

    # step sizes in x and y directions in complex plane between pixel centers
    x_step = abs(z_reals[1] - z_reals[0])
    y_step = abs(z_imags[1] - z_imags[0])

    print('applying iteration...')
    num_cores = pathos.multiprocessing.cpu_count()
    print('using %i cores...' % num_cores)
    p = ProcessingPool(num_cores)
    z_outs = list(p.map(lambda x: iter_func(x, trap_size=trap_size), z_ins))
    # z_outs = list(map(lambda x: iter_func(x, trap_size=trap_size), z_ins))

    print('matching grid cells...')
    # for each z_out, find closest location in pixel grid
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
    out_img.save("out1.png")
    print('done.')


if __name__ == "__main__":

    img_path = 'input_4_5.jpg'
    apply_orbit_trap(mandelbrot, img_path, trap_size=(0.8, 1))

