from imgzip import ImageCompressor

# Example 1: Compress a single image
compressor = ImageCompressor(quality=85)
result = compressor.compress(r"C:\Users\ranja\Downloads\Screenshot 2026-05-25 104119.png", r"C:\Users\ranja\Downloads\Screenshot_compressed.png")

print(f"Original: {result['original_size_kb']} KB")
print(f"Compressed: {result['compressed_size_kb']} KB")
print(f"Saved: {result['compression_ratio_percent']}%")


# Example 2: Compress all images in a folder
compressor = ImageCompressor(quality=85)
results = compressor.compress_batch("path/to/input/folder", "path/to/output/folder")

for result in results:
    if "error" not in result:
        print(f"Compressed: {result['input_path']}")
    else:
        print(f"Failed: {result['error']}")