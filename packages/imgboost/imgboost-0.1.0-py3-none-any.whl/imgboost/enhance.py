from PIL import Image, ImageEnhance
import cv2
import numpy as np
import argparse

def enhance_image(input_image_path, output_image_path, brightness=1.2, contrast=1.3, sharpness=2.0):
    try:
        img = Image.open(input_image_path)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)
        
        img_cv = np.array(img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        
        denoised_img = cv2.fastNlMeansDenoisingColored(img_cv, None, 10, 10, 7, 21)
        
        cv2.imwrite(output_image_path, denoised_img)
        print(f'Image is save in {output_image_path}')
    except FileNotFoundError:
        print(f"File {input_image_path} not found")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Enhance an image and save the result.')
    parser.add_argument('input_image', type=str, help='Path to the input image')
    parser.add_argument('output_image', type=str, help='Path to the output image')
    parser.add_argument('--brightness', type=float, default=1.2, help='Brightness factor')
    parser.add_argument('--contrast', type=float, default=1.3, help='Contrast factor')
    parser.add_argument('--sharpness', type=float, default=2.0, help='Sharpness factor')
    
    args = parser.parse_args()
    
    enhance_image(args.input_image, args.output_image, args.brightness, args.contrast, args.sharpness)