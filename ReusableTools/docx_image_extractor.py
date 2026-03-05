"""
Reusable utility to extract images from .docx files with contextual information.

Usage:
    python docx_image_extractor.py <path_to_docx> [output_dir]
    
Example:
    python docx_image_extractor.py "../TES-070/SoNH_TES-070_INT_FIN_013.docx"
"""

from docx import Document
import os
import sys
from pathlib import Path

def extract_all_images_with_context(docx_path, output_dir=None):
    """Extract all images and create detailed context report."""
    
    # Default output directory based on input file
    if output_dir is None:
        docx_name = Path(docx_path).stem
        output_dir = f"{docx_name}_images"
    
    doc = Document(docx_path)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Get all relationships that are images
    image_rels = [rel for rel in doc.part.rels.values() if "image" in rel.target_ref]
    
    print(f"Found {len(image_rels)} image relationships")
    
    # Extract each image
    for idx, rel in enumerate(image_rels, 1):
        try:
            image_data = rel.target_part.blob
            ext = rel.target_ref.split('.')[-1]
            filename = f"image_{idx:03d}.{ext}"
            filepath = output_path / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Extracted: {filename}")
        except Exception as e:
            print(f"❌ Error extracting image {idx}: {e}")
    
    # Now create context report by walking through document
    report_lines = [
        f"# TES-070 Image Analysis Report",
        f"**Source:** {docx_path}",
        f"**Total Images:** {len(image_rels)}",
        "",
        "---",
        ""
    ]
    
    current_section = ""
    image_counter = 0
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        # Track sections
        if text and para.style.name.startswith('Heading'):
            current_section = text
            report_lines.append(f"\n## {text}")
            report_lines.append("")
        
        # Check if paragraph contains image
        if any('graphic' in run.element.xml for run in para.runs):
            image_counter += 1
            report_lines.append(f"### Image {image_counter}")
            report_lines.append(f"**Section:** {current_section}")
            report_lines.append(f"**Context:** {text if text else '(Image with no caption)'}")
            report_lines.append(f"![image_{image_counter:03d}](image_{image_counter:03d}.png)")
            report_lines.append("")
        elif text:
            # Regular text paragraph
            report_lines.append(text)
            report_lines.append("")
    
    # Save report
    report_path = output_path / "context_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n📄 Context report saved to {report_path}")
    return len(image_rels)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python docx_image_extractor.py <path_to_docx> [output_dir]")
        print("\nExample:")
        print('  python docx_image_extractor.py "../TES-070/document.docx"')
        print('  python docx_image_extractor.py "document.docx" "my_images"')
        sys.exit(1)
    
    docx_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if os.path.exists(docx_file):
        count = extract_all_images_with_context(docx_file, output_dir)
        print(f"\n✅ Successfully extracted {count} images")
    else:
        print(f"❌ File not found: {docx_file}")
