#!/usr/bin/env python3
"""
PWA Icon Generator for Garage Management System
Generates all required icon sizes for PWA deployment
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Icon sizes required for PWA
SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Colors
BG_COLOR = '#FF6600'
TEXT_COLOR = 'white'

def create_icon(size):
    """Create a single icon of specified size"""
    # Create image with gradient-like background
    img = Image.new('RGB', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle background
    draw.rounded_rectangle([(0, 0), (size, size)], radius=size//8, fill=BG_COLOR)
    
    # Add emoji/text
    try:
        # Try to use a nice font
        font_size = size // 2
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw wrench emoji or text
    text = "🔧"
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=TEXT_COLOR, font=font)
    
    # Add "GMS" text for larger icons
    if size >= 192:
        try:
            small_font = ImageFont.truetype("arial.ttf", size // 8)
        except:
            small_font = ImageFont.load_default()
        
        gms_text = "GMS"
        bbox = draw.textbbox((0, 0), gms_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (size - text_width) // 2
        y = int(size * 0.75)
        
        draw.text((x, y), gms_text, fill=TEXT_COLOR, font=small_font)
    
    return img

def generate_all_icons():
    """Generate all required icon sizes"""
    # Create icons directory if it doesn't exist
    icons_dir = 'icons'
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"✅ Created {icons_dir} directory")
    
    print("🎨 Generating PWA icons...")
    
    for size in SIZES:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(icons_dir, filename)
        
        # Create and save icon
        icon = create_icon(size)
        icon.save(filepath, 'PNG')
        
        print(f"✅ Generated {filename}")
    
    print("\n🎉 All icons generated successfully!")
    print(f"📁 Icons saved to: {os.path.abspath(icons_dir)}")
    print("\n📋 Next steps:")
    print("1. Check the icons in the /icons folder")
    print("2. Deploy your app to a web server with HTTPS")
    print("3. Use PWABuilder.com to create Android package")
    print("4. Upload to Google Play Store")

if __name__ == "__main__":
    try:
        generate_all_icons()
    except ImportError:
        print("❌ PIL (Pillow) not installed!")
        print("\n📦 Install it with:")
        print("   pip install Pillow")
        print("\nOr use the HTML icon generator:")
        print("   Open http://localhost:3000/generate-icons.html")
