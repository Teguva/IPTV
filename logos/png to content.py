import os
from PIL import Image

def crop_pngs_in_folder(input_folder='png'):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    input_path = os.path.join(script_dir, input_folder)  # Full path to the input folder
    
    for filename in os.listdir(input_path):
        if filename.endswith('.png'):
            png_path = os.path.join(input_path, filename)
            
            # Open the PNG image
            with Image.open(png_path) as img:
                img = img.convert("RGBA")  # Ensure the image is in RGBA mode
                
                # Get the bounding box of the non-transparent content
                bbox = img.getbbox()
                
                # If there is content (bbox is not None), crop it
                if bbox:
                    cropped_img = img.crop(bbox)
                    cropped_img.save(png_path, format='PNG')  # Save the cropped image
                    print(f"Cropped {filename} to content")
                else:
                    print(f"No content found in {filename}")
    
    print("Cropping of PNGs completed!")

# Run the cropping function
crop_pngs_in_folder()
