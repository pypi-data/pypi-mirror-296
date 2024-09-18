import argparse
import os
from tqdm import tqdm
from PIL import Image


def center_crop_images(folder: str = None, resolution: tuple[int] = None):
    '''
    In-place center cropping of images present in a folder

    @Args:
        1. folder: path of the folder containing images.
        2. resolution: resolution of the images to be cropped to.
    '''
    paths = os.listdir(folder)
    for path in tqdm(paths):
        f = Image.open(f'{folder}/{path}')
        width, height = f.size
        new_width, new_height = resolution

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        f = f.crop((left, top, right, bottom))
        f.save(f'{folder}/{path}')

def main():
    parser = argparse.ArgumentParser(prog='Name', description='Description of the program')
    parser.add_argument('--f', required=True, help='Path of the folder')
    parser.add_argument('--r', required=True, type=int, nargs='+', help='Resolution of the images')
    args = parser.parse_args()

    center_crop_images(folder=args.f, resolution=tuple(args.r))

if __name__ == '__main__':
    main()