"""
Create a simple custom icon for the GUI
This creates a basic rocket icon to replace the default tkinter feather
"""

try:
    from PIL import Image, ImageDraw
    
    # Create a 32x32 icon with transparent background
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple rocket shape
    # Body (rectangle)
    draw.rectangle([12, 8, 20, 24], fill='#3498db', outline='#2980b9', width=1)
    
    # Nose cone (triangle)
    draw.polygon([16, 4, 12, 8, 20, 8], fill='#e74c3c', outline='#c0392b')
    
    # Window (circle)
    draw.ellipse([14, 12, 18, 16], fill='#ecf0f1', outline='#bdc3c7')
    
    # Fins (triangles)
    draw.polygon([12, 20, 8, 24, 12, 24], fill='#2ecc71', outline='#27ae60')
    draw.polygon([20, 20, 24, 24, 20, 24], fill='#2ecc71', outline='#27ae60')
    
    # Flame (triangles)
    draw.polygon([14, 24, 12, 28, 16, 28], fill='#f39c12', outline='#e67e22')
    draw.polygon([18, 24, 16, 28, 20, 28], fill='#f39c12', outline='#e67e22')
    
    # Save as ICO
    img.save('ReusableTools/app_icon.ico', format='ICO')
    print("✅ Icon created successfully: ReusableTools/app_icon.ico")
    
except ImportError:
    print("⚠️  PIL/Pillow not installed. Run: pip install Pillow")
    print("   Icon creation skipped - GUI will work without custom icon")

except Exception as e:
    print(f"⚠️  Could not create icon: {e}")
    print("   GUI will work without custom icon")
