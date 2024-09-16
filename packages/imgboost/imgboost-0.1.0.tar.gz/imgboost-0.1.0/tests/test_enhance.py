import unittest
import os
from PIL import Image
from imgboost.enhance import enhance_image

class TestEnhanceImage(unittest.TestCase):

    def setUp(self):
        self.input_image = 'test_input.jpg'
        self.output_image = 'test_output.jpg'
        
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.input_image)

    def test_enhance_image(self):
        enhance_image(self.input_image, self.output_image, brightness=1.5, contrast=1.4, sharpness=1.8)
        
        self.assertTrue(os.path.exists(self.output_image))
        
        with Image.open(self.output_image) as img:
            self.assertGreater(img.size[0], 0)
            self.assertGreater(img.size[1], 0)

    def tearDown(self):
        if os.path.exists(self.input_image):
            os.remove(self.input_image)
        if os.path.exists(self.output_image):
            os.remove(self.output_image)

if __name__ == '__main__':
    unittest.main()