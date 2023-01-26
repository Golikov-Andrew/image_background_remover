import math
import os
import traceback

from PIL import Image, ImageFilter, ImageEnhance

from gav_utils.icutil import init_dir


def new_bg_palette():
    return set()


def new_bg_palette_2() -> dict:
    return {'R': [None, None], 'G': [None, None], 'B': [None, None]}


class DIRECTION:
    RIGHT = 'RIGHT'
    UP = 'UP'
    LEFT = 'LEFT'
    DOWN = 'DOWN'


class ImageBGRemover:

    def __init__(self, images_dir_path: str):
        self._images_dir_path = images_dir_path
        self._dest_dir_path = init_dir('dest_images')
        self._cur_image_path = ''
        self._image_data = None
        self._image_filename = None
        self._bg_palette = new_bg_palette_2()

    def _misc(self):
        # out = self._image_data.filter(ImageFilter.DETAIL)
        # split the image into individual bands
        # source = self._image_data.split()
        # R, G, B = 0, 1, 2
        # # select regions where red is less than 100
        # mask = source[R].point(lambda i: i < 100 and 255)
        # # process the green band
        # out = source[G].point(lambda i: i * 0.7)
        # self.show_result()
        # # paste the processed band back, but only where red was < 100
        # source[G].paste(out, None, mask)
        # # build a new multiband image
        # self._image_data = Image.merge(self._image_data.mode, source)
        # out = self._image_data.point(lambda i: i * 1.2)

        # enh = ImageEnhance.Contrast(self._image_data)
        # enh.enhance(1.3).show("30% more contrast")

        # bands = self._image_data.getbands()
        pass

    def remove_bg(self, image_name: str):

        self._image_filename = image_name
        self._cur_image_path = os.path.join(self._images_dir_path, image_name)
        self._image_data = self._load_image()
        print(self._image_data.format, self._image_data.size, self._image_data.mode)
        self._bg_palette = new_bg_palette_2()

        width, height = self._image_data.size

        width_pixel_treshold = math.floor(0.3 * width)
        width_pixel_treshold_back = width - width_pixel_treshold
        height_pixel_treshold = math.floor(0.3 * height)
        height_pixel_treshold_back = height - height_pixel_treshold
        bg_contrast = 1

        pixel_data = self._image_data.getpixel((0, 0))
        self._init_bg_palette(bg_contrast, pixel_data)

        w_r_lim = width
        w_l_lim = 0
        h_b_lim = height
        h_t_lim = 0
        direction = DIRECTION.RIGHT
        col, row = 0, 0

        while True:
            # for row in range(height):
            #     for col in range(width):
            coords = (col, row)
            try:
                pixel_data = self._image_data.getpixel(coords)
            except:
                traceback.print_exc()

            if (col < width_pixel_treshold or col >= width_pixel_treshold_back or
                    row < height_pixel_treshold or row >= height_pixel_treshold_back):
                if self.is_need_to_add_to_bg_palette(pixel_data, bg_contrast):
                    self._add_to_bg_palette(pixel_data)
                    self._image_data.putpixel(coords, (255, 255, 255))
            else:
                if self._is_bg_pixel(pixel_data):
                    # self._add_to_bg_palette(pixel_data)
                    self._image_data.putpixel(coords, (255, 255, 255))

            if direction == DIRECTION.RIGHT:
                if col < w_r_lim - 1:
                    col += 1
                else:
                    direction = DIRECTION.DOWN
                    row += 1
                    w_r_lim -= 1


            elif direction == DIRECTION.DOWN:
                if row < h_b_lim - 1:
                    row += 1
                else:
                    direction = DIRECTION.LEFT
                    col -= 1
                    h_b_lim -= 1

            elif direction == DIRECTION.LEFT:
                if col > w_l_lim:
                    col -= 1
                else:
                    direction = DIRECTION.UP
                    row -= 1
                    w_l_lim += 1

            elif direction == DIRECTION.UP:
                if row > h_t_lim:
                    row -= 1
                else:
                    direction = DIRECTION.RIGHT
                    col += 1
                    h_t_lim += 1

            if h_t_lim >= h_b_lim or w_l_lim >= w_r_lim:
                break

    def show_result(self):
        self._image_data.show()

    def save_result(self):
        self._image_data.save(os.path.join(self._dest_dir_path, self._image_filename))

    def _load_image(self):
        # return Image.open(io.BytesIO(buffer))
        return Image.open(self._cur_image_path)

    def _add_to_bg_palette(self, pixel_data):
        r = pixel_data[0]
        g = pixel_data[1]
        b = pixel_data[2]

        if self._bg_palette['R'][0] > r:
            self._bg_palette['R'][0] = r
        elif self._bg_palette['R'][1] < r:
            self._bg_palette['R'][1] = r

        if self._bg_palette['G'][0] > g:
            self._bg_palette['G'][0] = g
        elif self._bg_palette['G'][1] < g:
            self._bg_palette['G'][1] = g

        if self._bg_palette['B'][0] > b:
            self._bg_palette['B'][0] = b
        elif self._bg_palette['B'][1] < b:
            self._bg_palette['B'][1] = b

        # self._bg_palette.add(pixel_data)

    def _is_bg_pixel(self, pixel_data: tuple) -> bool:
        if pixel_data in self._bg_palette:
            return True
        return False

    def is_need_to_add_to_bg_palette(self, pixel_data: tuple, bg_contrast: int) -> bool:
        if self._bg_palette['R'][0] - bg_contrast < pixel_data[0] < self._bg_palette['R'][1] + bg_contrast:
            if self._bg_palette['G'][0] - bg_contrast < pixel_data[1] < self._bg_palette['G'][1] + bg_contrast:
                if self._bg_palette['B'][0] - bg_contrast < pixel_data[2] < self._bg_palette['B'][1] + bg_contrast:
                    return True
        return False

    def _init_bg_palette(self, bg_contrast, pixel_data):
        r = pixel_data[0]
        if self._bg_palette['R'][0] is None:
            self._bg_palette['R'][0] = self._prepare_val(r - bg_contrast)
        if self._bg_palette['R'][1] is None:
            self._bg_palette['R'][1] = self._prepare_val(r + bg_contrast)
        g = pixel_data[1]
        if self._bg_palette['G'][0] is None:
            self._bg_palette['G'][0] = self._prepare_val(g - bg_contrast)
        if self._bg_palette['G'][1] is None:
            self._bg_palette['G'][1] = self._prepare_val(g + bg_contrast)
        b = pixel_data[2]
        if self._bg_palette['B'][0] is None:
            self._bg_palette['B'][0] = self._prepare_val(b - bg_contrast)
        if self._bg_palette['B'][1] is None:
            self._bg_palette['B'][1] = self._prepare_val(b + bg_contrast)

    def _prepare_val(self, val: int) -> int:
        if val < 0:
            return 0
        elif val >= 255:
            return 255
        else:
            return val


if __name__ == '__main__':
    image_bg_remover = ImageBGRemover('src_images')
    image_bg_remover.remove_bg('0.jpg')
    image_bg_remover.show_result()
    print()
    # image_bg_remover.save_result()
