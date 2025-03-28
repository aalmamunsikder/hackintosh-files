import os
from PIL import Image, ImageDraw, ImageFont
import shutil

# Create resources directory
resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
os.makedirs(resources_dir, exist_ok=True)

# Generate app icon
def generate_app_icon():
    # Create a 128x128 image with a blue to purple gradient background
    img = Image.new('RGB', (128, 128), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a gradient background
    for y in range(128):
        r = int(25 + (y / 128) * 30)
        g = int(100 + (y / 128) * 50)
        b = int(200 - (y / 128) * 50)
        for x in range(128):
            draw.point((x, y), fill=(r, g, b))
    
    # Draw a computer icon
    draw.rectangle([30, 40, 98, 75], outline=(255, 255, 255), width=2)
    draw.rectangle([50, 75, 78, 85], outline=(255, 255, 255), width=2)
    draw.rectangle([40, 85, 88, 88], fill=(255, 255, 255))
    
    # Draw an apple logo
    draw.ellipse([54, 50, 74, 70], outline=(255, 255, 255), width=2)
    draw.rectangle([63, 45, 65, 50], fill=(255, 255, 255))
    
    # Save the image
    img.save(os.path.join(resources_dir, "app_icon.png"))
    print(f"Generated app icon at {os.path.join(resources_dir, 'app_icon.png')}")

# Generate a screenshot placeholder
def generate_screenshot():
    # Create a 800x600 image with a dark background
    img = Image.new('RGB', (800, 600), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Draw a window frame
    draw.rectangle([50, 50, 750, 550], outline=(100, 100, 120), width=2)
    draw.rectangle([50, 50, 750, 80], fill=(60, 60, 80))
    
    # Draw window title
    draw.text((400, 65), "Hackintosh EFI Builder", fill=(220, 220, 240), anchor="mm")
    
    # Draw some UI elements
    # Left panel
    draw.rectangle([70, 100, 370, 530], outline=(80, 80, 100), width=1)
    draw.text((220, 115), "Hardware Configuration", fill=(200, 200, 220), anchor="mm")
    
    # Draw some form elements
    y_pos = 150
    for label in ["CPU Type:", "CPU Model:", "Graphics:", "Audio:", "Ethernet:", "WiFi:"]:
        draw.text((100, y_pos), label, fill=(180, 180, 200))
        draw.rectangle([200, y_pos-5, 350, y_pos+15], outline=(100, 100, 120), width=1)
        y_pos += 50
    
    # Right panel
    draw.rectangle([390, 100, 730, 530], outline=(80, 80, 100), width=1)
    draw.text((560, 115), "Build Configuration", fill=(200, 200, 220), anchor="mm")
    
    # Draw some checkboxes
    y_pos = 150
    for label in ["Lilu", "VirtualSMC", "WhateverGreen", "AppleALC"]:
        draw.rectangle([410, y_pos, 425, y_pos+15], outline=(100, 100, 120), width=1)
        draw.text((440, y_pos+7), label, fill=(180, 180, 200), anchor="lm")
        y_pos += 30
    
    # Draw a progress bar
    draw.rectangle([410, 300, 710, 320], outline=(100, 100, 120), width=1)
    draw.rectangle([410, 300, 500, 320], fill=(80, 120, 200))
    
    # Draw a button
    draw.rectangle([500, 450, 620, 480], fill=(80, 120, 200), outline=(100, 140, 220), width=2)
    draw.text((560, 465), "Build EFI", fill=(240, 240, 255), anchor="mm")
    
    # Save the image
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot.png"))
    print(f"Generated screenshot at {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshot.png')}")

if __name__ == "__main__":
    generate_app_icon()
    generate_screenshot()
    print("Resource generation complete!")