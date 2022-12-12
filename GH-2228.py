#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import os
import pathlib

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    # 写輪眼
    # 開眼すると瞳が赤く発光し、瞳孔の周囲に黒い巴模様が複数浮かぶようになる。
    # 開眼時は瞳の巴は1～2つであり、優れた動体視力とチャクラを可視化する能力を得る。
    # 開眼者が成長すると巴が増え、最終的に両目の巴が3つずつになると通常の写輪眼としては完成形となる。
    # 薄暗い中でも写輪眼は発光しているので、敵からしたら赤い発光体が2つキョロキョロ動くので何処にいるのかが丸分かりである。
    # 瞳力は開眼者の精神と深い関係にあり、憎しみの感情が増大すると瞳力も飛躍的に高まっていく。
    dimensions = [768, 1024]
    sizes = set()
    for size in itertools.combinations_with_replacement(dimensions, 2):
        # drop some aspect ratio
        w, h = size
        need_drop = 4
        if w / h > need_drop or h / w > need_drop:
            continue
        sizes.update([size, size[::-1]])
    aspect2sizes = {'Landscape': [], 'Portrait': [], 'Square': []}
    for size in sizes:
        w, h = size
        if w == h:
            aspect2sizes['Square'].append(size)
        elif w < h:
            aspect2sizes['Portrait'].append(size)
        elif h < w:
            aspect2sizes['Landscape'].append(size)
        else:
            raise Exception(size)
    # -flop for horizontal mirroring, and -flip for vertical
    orientation2transformation = {
        0: {'rotation': 0, 'flip': False, 'flop': False},
        # ・ Orientation = 1 is created when 0th row of the coded image data stored in the Exif image file
        # and the visual top of the display screen, and 0th column and visual left, will each be matched
        # for display
        1: {'rotation': 0, 'flip': False, 'flop': False},
        # ・ Orientation = 2 is equivalent to an arrangement that is reversed Orientation = 1 horizontally
        2: {'rotation': 0, 'flip': False, 'flop': True},
        # ・ Orientation = 3 is equivalent to an arrangement that is turned Orientation = 6 90 degrees
        # clockwise
        3: {'rotation': 90 + 90, 'flip': False, 'flop': False},
        # ・ Orientation = 4 is equivalent to an arrangement that is reversed Orientation = 3 horizontally
        4: {'rotation': 90 + 90, 'flip': False, 'flop': True},
        # ・ Orientation = 5 is equivalent to an arrangement that is reversed Orientation = 6 horizontally
        5: {'rotation': 90, 'flip': False, 'flop': True},
        # ・ Orientation = 6 is equivalent to an arrangement that is turned Orientation = 1 90 degrees
        # clockwise
        6: {'rotation': 90, 'flip': False, 'flop': False},
        # ・ Orientation = 7 is equivalent to an arrangement that is reversed Orientation = 8 horizontally
        7: {'rotation': 90 + 90 + 90, 'flip': False, 'flop': True},
        # ・ Orientation = 8 is equivalent to an arrangement that is turned Orientation = 3 90 degrees
        # clockwise
        8: {'rotation': 90 + 90 + 90, 'flip': False, 'flop': False}
    }
    # @formatter:on
    path = pathlib.Path().cwd() / 'PainNotes'
    cur_path = path
    s = '''
        Content-Type: text/x-zim-wiki
        Wiki-Format: zim 0.6
        Creation-Date: 2022-11-28T21:43:31+00:00

        ====== {page_name} ======
        --------------------
        '''
    s = s.replace('\n', '', 1)
    s = '\n'.join([x.strip() for x in s.split('\n')])
    if not s.endswith('\n'):
        s += '\n'
    (path / 'TestExifOrientation').mkdir(parents=True, exist_ok=True)
    with open(path / 'TestExifOrientation.txt', mode='w', encoding='utf-8') as f:
        f.write(s.format(page_name='TestExifOrientation'))
    cur_path /= 'TestExifOrientation'
    for aspect in aspect2sizes.keys():
        for size in aspect2sizes[aspect]:
            print(size)
            w, h = size
            cell_size = (48, 48)
            background_color = (0xff, 0x00, 0x00, 0xff)
            foreground_color = (0x00, 0x00, 0xff, 0xff)
            image1 = Image.new('RGBA', (w, h), background_color)
            image3 = Image.new('RGBA', (w, h), (0xff, 0xff, 0xff, 0xff))
            draw3 = ImageDraw.Draw(image3)
            for i in range(w):
                x = int(255 / 100 * i * 100 / w * 0.75)
                draw3.line((i, 0, i, h - 1), fill=(0xff - x, 0x00 + x, 0xff, x), width=1)
            image4 = Image.new('RGBA', (w, h), (0xff, 0xff, 0xff, 0xff))
            draw4 = ImageDraw.Draw(image4)
            for i in range(w):
                x = int(255 / 100 * i * 100 / w * 0.75)
                draw4.line((w - i, 0, w - i, h - 1), fill=(0xff, 0x00 + x, 0xff - x, x), width=1)
            draw1 = ImageDraw.Draw(image1)
            chess_pattern = []
            for y in range(0, h // cell_size[1] + 1):
                row = []
                for x in range(0, w // cell_size[0] + 1):
                    row.append((x + y) % 2)
                chess_pattern.append(row)
            for y, row in enumerate(chess_pattern):
                for x, c in enumerate(row):
                    bbox = ((x * cell_size[0], y * cell_size[0]),
                            (x * cell_size[0] + cell_size[1], y * cell_size[1] + cell_size[1]))
                    draw1.rectangle(bbox, fill=foreground_color if c else background_color)

            factor1 = (((w // cell_size[0]) + (h // cell_size[1])) // 2) * 4
            font1 = ImageFont.truetype('ubuntu-font-family-0.83/UbuntuMono-B.ttf', factor1)
            image1 = Image.alpha_composite(image1, image3)
            image1 = Image.alpha_composite(image1, image4)
            image1.putalpha(image4.convert('L'))
            pixels = image1.load()
            for j in range(image1.size[1]):
                for i in range(image1.size[0]):
                    # noinspection PyUnresolvedReferences
                    r, b, g, a = pixels[i, j]
                    x = 255 - int(255 / 100 * j * 100 / (image1.size[1] + 1) * 1)
                    # noinspection PyUnresolvedReferences
                    pixels[i, j] = (r, b, g, x)

            draw1 = ImageDraw.Draw(image1)
            draw1.text((w // 2, 0), 'Top', fill='white', anchor='ma', font=font1)
            draw1.text((w, h // 2), 'Right', fill='white', anchor='rm', font=font1)
            draw1.text((w // 2, h), 'Bottom', fill='white', anchor='md', font=font1)
            draw1.text((0, h // 2), 'Left', fill='white', anchor='lm', font=font1)

            for orientation, transformation in orientation2transformation.items():
                image2 = image1.copy()
                draw2 = ImageDraw.Draw(image2)
                factor2 = factor1 * 4
                font2 = ImageFont.truetype('ubuntu-font-family-0.83/UbuntuMono-B.ttf', factor2)
                draw2.text((w // 2, h // 2), f'{orientation}', fill='black', anchor='mm', font=font2)
                if transformation['flip']:
                    image2 = image2.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                if transformation['flop']:
                    image2 = image2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if transformation['rotation'] != 0:
                    image2 = image2.rotate(transformation['rotation'], expand=True)
                for format_image in ('jpeg', 'png', 'webp'):
                    n = f'Format[{format_image}]'
                    (cur_path / n).mkdir(parents=True, exist_ok=True)
                    with open(cur_path / f'{n}.txt', mode='w', encoding='utf-8') as f:
                        f.write(s.format(page_name=f'{n}'))
                    case = f'Case[{size[0]}x{size[1]}]'
                    p = cur_path / n / aspect / case
                    p.mkdir(parents=True, exist_ok=True)
                    with open(cur_path / n / aspect / f'{case}.txt', mode='w', encoding='utf-8') as f:
                        f.write(s.format(page_name=f'{case}'))
                    name = f'{aspect}_{w}x{h}_{orientation}.{format_image}'
                    filename = p / name
                    print(format_image, image2.mode)
                    if format_image == 'jpeg':
                        tmp = image2.convert('RGB')
                        tmp.save(filename, 'JPEG')
                    elif format_image == 'png':
                        image2.save(filename, 'PNG')
                    elif format_image == 'webp':
                        image2.save(filename, 'WebP')
                    else:
                        raise Exception(format_image)

                    if orientation != 0:
                        os.system(f'exiftool -overwrite_original -Orientation={orientation} -n "{filename}"')
                    for scale in ['Up', 'Down']:
                        scale_s = f'Scale{scale}'
                        p2 = cur_path / n / aspect / case / scale_s
                        p2.mkdir(parents=True, exist_ok=True)
                        with open(cur_path / n / aspect / case / f'{scale_s}.txt', mode='w', encoding='utf-8') as f:
                            f.write(s.format(page_name=f'{scale_s}'))
                        for by in ['None', 'Height', 'Width', 'Height&Width']:
                            by_s = f'By{by}'
                            p3 = cur_path / n / aspect / case / scale_s / by_s
                            p3.mkdir(parents=True, exist_ok=True)
                            fn1 = cur_path / n / aspect / case / scale_s / f'{by_s}.txt'
                            if fn1.exists():
                                if fn1.is_file():
                                    if fn1.stat().st_size != 0:
                                        with open(file=fn1, mode='r', encoding='utf-8') as fh_in:
                                            data = fh_in.read()
                                    else:
                                        data = ''
                                else:
                                    raise
                            else:
                                data = ''
                            data = data.replace(s.format(page_name=f'{by_s}'), '', 1)
                            rename_me_1 = data.split('\n')
                            rename_me_0 = len(rename_me_1)

                            print(f'data len={rename_me_0}, {rename_me_1=}')
                            if rename_me_0 >= 10:
                                pass
                            else:
                                #  data = data[::-1].replace('--------------------\n'[::-1], '', 1)[::-1]
                                with open(fn1, mode='w', encoding='utf-8') as f:
                                    f.write(s.format(page_name=f'{by_s}'))
                                    f.write(data)
                                    t = ''
                                    if by == 'None':
                                        pass
                                    elif by == 'Height':
                                        t = 'height'
                                        if scale == 'Up':
                                            t += f'={int(image2.height * 1.5)}'
                                        elif scale == 'Down':
                                            t += f'=240'
                                        else:
                                            raise
                                    elif by == 'Width':
                                        t = 'width'
                                        if scale == 'Up':
                                            t += f'={int(image2.width * 1.5)}'
                                        elif scale == 'Down':
                                            t += f'=240'
                                        else:
                                            raise
                                    elif by == 'Height&Width':
                                        t = 'height'
                                        if scale == 'Up':
                                            t += f'={int(image2.height * 1.5)}'
                                        elif scale == 'Down':
                                            t += f'=240'
                                        else:
                                            raise
                                        t += '&'
                                        t += 'width'
                                        if scale == 'Up':
                                            t += f'={int(image2.width * 1.5)}'
                                        elif scale == 'Down':
                                            t += f'=240'
                                        else:
                                            raise
                                    else:
                                        raise
                                    if t != '':
                                        t = f'?{t}'
                                    print(t)
                                    x = f'{{{{../../{filename.name}{t}}}}}'
                                    f.write(f'{x}')
                                    f.write('\n')
                            pass


if __name__ == '__main__':
    main()
