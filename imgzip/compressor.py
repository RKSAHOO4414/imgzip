"""
Core image compression module
"""

import os
from PIL import Image
from pathlib import Path


class ImageCompressor:
    """
    A simple and efficient image compressor for common image formats.
    
    Supported formats: JPG, PNG, BMP, GIF
    """
    
    def __init__(self, quality=85, max_width=None, max_height=None):
        """
        Initialize the ImageCompressor.
        
        Args:
            quality (int): JPEG quality level (1-100). Default is 85.
                          Higher = better quality, larger file size.
            max_width (int): Maximum width in pixels. Maintains aspect ratio if set.
            max_height (int): Maximum height in pixels. Maintains aspect ratio if set.
        """
        if not 1 <= quality <= 100:
            raise ValueError("Quality must be between 1 and 100")
        
        self.quality = quality
        self.max_width = max_width
        self.max_height = max_height
    
    def compress(self, input_path, output_path=None, format=None):
        """
        Compress a single image file.
        
        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the compressed image. 
                              If None, saves as 'compressed_<original_name>'.
            format (str): Image format for output (JPG, PNG). If None, uses input format.
        
        Returns:
            dict: Dictionary with compression details (original size, compressed size, ratio).
        
        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If file format is not supported.
        """
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Open image
        try:
            img = Image.open(input_path)
        except Exception as e:
            raise ValueError(f"Cannot open image file: {e}")
        
        # Get original file size
        original_size = os.path.getsize(input_path)
        
        # Determine output path
        if output_path is None:
            input_name = Path(input_path).stem
            input_ext = Path(input_path).suffix
            output_path = f"compressed_{input_name}{input_ext}"
        
        # Determine output format
        if format is None:
            format = img.format or "JPEG"
        format = format.upper()
        
        # Resize if max dimensions are set
        if self.max_width or self.max_height:
            img.thumbnail((self.max_width or img.width, self.max_height or img.height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if saving as JPEG
        if format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = rgb_img
        
        # Save compressed image
        img.save(output_path, format=format, quality=self.quality, optimize=True)
        
        # Get compressed file size
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - (compressed_size / original_size)) * 100
        
        return {
            "input_path": input_path,
            "output_path": output_path,
            "original_size_kb": round(original_size / 1024, 2),
            "compressed_size_kb": round(compressed_size / 1024, 2),
            "compression_ratio_percent": round(compression_ratio, 2),
        }
    
    def compress_batch(self, input_folder, output_folder=None):
        """
        Compress all images in a folder.
        
        Args:
            input_folder (str): Path to folder containing images.
            output_folder (str): Path to save compressed images. 
                                If None, creates 'compressed' folder in input folder.
        
        Returns:
            list: List of dictionaries with compression details for each image.
        """
        if not os.path.isdir(input_folder):
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        if output_folder is None:
            output_folder = os.path.join(input_folder, "compressed")
        
        os.makedirs(output_folder, exist_ok=True)
        
        results = []
        supported_formats = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
        
        for filename in os.listdir(input_folder):
            if Path(filename).suffix.lower() in supported_formats:
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f"compressed_{filename}")
                
                try:
                    result = self.compress(input_path, output_path)
                    results.append(result)
                except Exception as e:
                    results.append({
                        "input_path": input_path,
                        "error": str(e)
                    })
        
        return results
