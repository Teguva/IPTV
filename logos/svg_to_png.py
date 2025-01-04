import os
from PIL import Image
import cairosvg

def convert_svgs_to_pngs(input_folder='svg', output_folder='png', size=(512, 512)):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    input_path = os.path.join(script_dir, input_folder)  # Full path to the input folder
    output_path = os.path.join(script_dir, output_folder)  # Full path to the output folder
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for filename in os.listdir(input_path):
        if filename.endswith('.svg'):
            svg_path = os.path.join(input_path, filename)
            png_path = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.png")
            
            # Convert SVG to PNG using cairosvg
            with open(svg_path, "rb") as svg_file:
                cairosvg.svg2png(file_obj=svg_file, write_to=png_path)

            # Adjust PNG to fit content while maintaining aspect ratio
            with Image.open(png_path) as img:
                img = img.convert("RGBA")
                img_width, img_height = img.size

                # Calculate scale factor to fit the largest dimension to 512px
                if img_width > img_height:
                    scale_factor = size[0] / img_width
                else:
                    scale_factor = size[1] / img_height

                # Resize the image while maintaining aspect ratio
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Create a new image with a transparent background
                new_img = Image.new("RGBA", size, (0, 0, 0, 0))
                new_img.paste(img, ((size[0] - new_width) // 2, (size[1] - new_height) // 2))

                # Save the resized image
                new_img.save(png_path, format='PNG')

            print(f"Converted {filename} to {png_path}")

# Run the conversion
convert_svgs_to_pngs()

print("SVG to PNG conversion completed!")
