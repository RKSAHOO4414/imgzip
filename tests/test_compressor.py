"""
Unit tests for imgzip compressor
"""

import unittest
import os
import tempfile
from pathlib import Path
from PIL import Image
from imgzip.compressor import ImageCompressor


class TestImageCompressor(unittest.TestCase):
    """Test cases for ImageCompressor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.compressor = ImageCompressor(quality=85)
        
        # Create a test image
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        test_image = Image.new("RGB", (1000, 1000), color="red")
        test_image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test files"""
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)
    
    def test_quality_validation(self):
        """Test that quality parameter is validated"""
        with self.assertRaises(ValueError):
            ImageCompressor(quality=0)
        
        with self.assertRaises(ValueError):
            ImageCompressor(quality=101)
    
    def test_compress_file_exists(self):
        """Test compression of an existing file"""
        output_path = os.path.join(self.temp_dir, "compressed_test.png")
        result = self.compressor.compress(self.test_image_path, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("compression_ratio_percent", result)
        self.assertGreater(result["compression_ratio_percent"], 0)
    
    def test_compress_nonexistent_file(self):
        """Test that compression fails for nonexistent file"""
        with self.assertRaises(FileNotFoundError):
            self.compressor.compress("/nonexistent/path/image.png")
    
    def test_auto_output_path(self):
        """Test automatic output path generation"""
        original_dir = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            result = self.compressor.compress(self.test_image_path)
            
            self.assertTrue(os.path.exists(result["output_path"]))
            self.assertIn("compressed_", result["output_path"])
        finally:
            os.chdir(original_dir)
    
    def test_resize_functionality(self):
        """Test image resizing during compression"""
        compressor_with_resize = ImageCompressor(quality=85, max_width=500, max_height=500)
        output_path = os.path.join(self.temp_dir, "resized.png")
        
        compressor_with_resize.compress(self.test_image_path, output_path)
        
        # Verify resized image
        compressed_img = Image.open(output_path)
        self.assertLessEqual(compressed_img.width, 500)
        self.assertLessEqual(compressed_img.height, 500)
    
    def test_compression_ratio(self):
        """Test that compression actually reduces file size"""
        # Create a more complex image that compresses better
        import random
        test_image = Image.new("RGB", (1000, 1000))
        pixels = test_image.load()
        for i in range(1000):
            for j in range(1000):
                pixels[i, j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        complex_image_path = os.path.join(self.temp_dir, "complex_image.png")
        test_image.save(complex_image_path)
        
        output_path = os.path.join(self.temp_dir, "compressed_test.jpg")
        result = self.compressor.compress(complex_image_path, output_path, format="JPEG")
        
        self.assertLess(result["compressed_size_kb"], result["original_size_kb"])


if __name__ == "__main__":
    unittest.main()
