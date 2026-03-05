"""
PDF Study Reader - Comprehensive document analysis

Purpose: Deep study of entire PDF documents in manageable chunks
Use when: You need to understand the complete structure and content of a document
"""

import PyPDF2
import os
import time
import re
from typing import List, Dict, Optional, Generator

class PDFStudyReader:
    """Comprehensive PDF study reader with chunked processing"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.total_pages = self._get_page_count()
        self.chunk_size = 10  # Process 10 pages at a time
    
    def _get_page_count(self) -> int:
        """Get total page count"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception:
            return 0
    
    def get_document_overview(self) -> Dict:
        """Get high-level document overview"""
        if self.total_pages == 0:
            return {'error': 'PDF not accessible'}
        
        # Read first few pages for overview
        overview = {
            'filename': os.path.basename(self.pdf_path),
            'total_pages': self.total_pages,
            'estimated_chunks': (self.total_pages + self.chunk_size - 1) // self.chunk_size,
            'title': '',
            'table_of_contents': [],
            'document_type': 'Unknown'
        }
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract title and basic info from first 3 pages
                title_text = ""
                toc_text = ""
                
                for page_num in range(min(3, self.total_pages)):
                    page_text = pdf_reader.pages[page_num].extract_text()
                    
                    if page_num == 0:
                        # Extract title from first page
                        lines = page_text.split('\n')[:10]
                        for line in lines:
                            line = line.strip()
                            if len(line) > 10 and not line.startswith('Copyright'):
                                title_text = line
                                break
                    
                    # Look for table of contents
                    if 'contents' in page_text.lower() or 'chapter' in page_text.lower():
                        toc_text += page_text + "\n"
                
                overview['title'] = title_text
                overview['table_of_contents'] = self._extract_toc(toc_text)
                overview['document_type'] = self._determine_document_type(title_text + toc_text)
        
        except Exception as e:
            overview['error'] = f"Failed to read overview: {e}"
        
        return overview
    
    def _extract_toc(self, text: str) -> List[str]:
        """Extract table of contents items with improved detection"""
        toc_items = []
        lines = text.split('\n')
        
        # Look for TOC section first
        toc_section_found = False
        toc_start_idx = -1
        
        for i, line in enumerate(lines):
            line_clean = line.strip().lower()
            
            # Detect TOC section start with multiple patterns
            toc_markers = [
                'contents', 'table of contents', 'table des matières',
                'índice', 'inhalt', 'sommaire'
            ]
            
            if any(marker in line_clean for marker in toc_markers):
                toc_section_found = True
                toc_start_idx = i
                break
        
        if toc_section_found and toc_start_idx >= 0:
            # Process lines after TOC marker
            for j in range(toc_start_idx + 1, min(toc_start_idx + 100, len(lines))):
                toc_line = lines[j].strip()
                
                # Skip empty lines and very short lines
                if len(toc_line) < 3:
                    continue
                
                # Enhanced TOC item detection patterns
                is_toc_item = False
                
                # Pattern 1: Chapter/Section keywords
                if any(keyword in toc_line.lower() for keyword in [
                    'chapter', 'section', 'appendix', 'part', 'unit',
                    'lesson', 'module', 'topic', 'overview', 'introduction',
                    'getting started', 'configuration', 'setup', 'installation'
                ]):
                    is_toc_item = True
                
                # Pattern 2: Numbered items (1., 2., 1.1, etc.)
                elif re.match(r'^\d+\.?\d*\.?\s+[A-Z]', toc_line):
                    is_toc_item = True
                
                # Pattern 3: Items with page numbers at end
                elif re.search(r'\.\.\.\s*\d+$', toc_line) or re.search(r'\s+\d+$', toc_line):
                    is_toc_item = True
                
                # Pattern 4: Items with dots leading to page numbers
                elif re.search(r'\.{3,}\s*\d+', toc_line):
                    is_toc_item = True
                
                # Pattern 5: Capitalized items (likely headings)
                elif (toc_line[0].isupper() and 
                      len(toc_line) > 10 and len(toc_line) < 120 and
                      not toc_line.endswith('.') and
                      toc_line.count(' ') < 15):
                    is_toc_item = True
                
                # Pattern 6: Items starting with letters (A., B., etc.)
                elif re.match(r'^[A-Z]\.?\s+[A-Z]', toc_line):
                    is_toc_item = True
                
                if is_toc_item and len(toc_line) < 150:
                    # Clean up the TOC item
                    clean_item = re.sub(r'\.\.\.\s*\d+$', '', toc_line).strip()
                    clean_item = re.sub(r'\s+\d+$', '', clean_item).strip()
                    clean_item = re.sub(r'\.{3,}\s*\d+', '', clean_item).strip()
                    
                    if len(clean_item) > 5:
                        toc_items.append(clean_item)
        
        # If no formal TOC found, look for chapter headings in document
        if not toc_items:
            for i, line in enumerate(lines[:300]):  # First portion of document
                line_clean = line.strip()
                
                # Look for chapter/section headings
                if re.match(r'^(Chapter|Section|Part)\s+\d+', line_clean, re.IGNORECASE):
                    if len(line_clean) < 100:
                        toc_items.append(line_clean)
                
                # Look for numbered headings that appear to be major sections
                elif re.match(r'^\d+\.\s+[A-Z][a-z]', line_clean):
                    if len(line_clean) < 80 and len(line_clean) > 10:
                        # Check if next few lines are content (not another heading)
                        is_heading = True
                        for check_idx in range(i+1, min(i+3, len(lines))):
                            if lines[check_idx].strip() and len(lines[check_idx].strip()) > 20:
                                is_heading = True
                                break
                        
                        if is_heading:
                            toc_items.append(line_clean)
        
        return toc_items[:25]  # Limit to 25 items for better performance
    
    def _determine_document_type(self, text: str) -> str:
        """Determine document type from content"""
        text_lower = text.lower()
        
        if 'user guide' in text_lower or 'user manual' in text_lower:
            return 'User Guide'
        elif 'reference' in text_lower and 'guide' in text_lower:
            return 'Reference Guide'
        elif 'installation' in text_lower:
            return 'Installation Guide'
        elif 'configuration' in text_lower:
            return 'Configuration Guide'
        elif 'developer' in text_lower or 'development' in text_lower:
            return 'Developer Guide'
        elif 'admin' in text_lower or 'administration' in text_lower:
            return 'Administration Guide'
        else:
            return 'Technical Documentation'
    
    def study_document_by_chunks(self) -> Generator[Dict, None, None]:
        """Study document in chunks to manage memory and context limits"""
        if self.total_pages == 0:
            yield {'error': 'PDF not accessible'}
            return
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for chunk_start in range(0, self.total_pages, self.chunk_size):
                    chunk_end = min(chunk_start + self.chunk_size, self.total_pages)
                    
                    chunk_data = {
                        'chunk_number': (chunk_start // self.chunk_size) + 1,
                        'pages': f"{chunk_start + 1}-{chunk_end}",
                        'content_summary': '',
                        'key_topics': [],
                        'sections_found': [],
                        'page_count': chunk_end - chunk_start
                    }
                    
                    # Process pages in this chunk
                    chunk_text = ""
                    for page_num in range(chunk_start, chunk_end):
                        try:
                            page_text = pdf_reader.pages[page_num].extract_text()
                            chunk_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                        except Exception:
                            continue
                    
                    # Analyze chunk content
                    if chunk_text.strip():
                        chunk_data['content_summary'] = self._summarize_chunk(chunk_text)
                        chunk_data['key_topics'] = self._extract_key_topics(chunk_text)
                        chunk_data['sections_found'] = self._find_sections(chunk_text)
                    
                    yield chunk_data
                    
                    # Small delay to prevent overwhelming
                    time.sleep(0.1)
        
        except Exception as e:
            yield {'error': f'Failed to study document: {e}'}
    
    def _summarize_chunk(self, text: str) -> str:
        """Create a summary of chunk content"""
        # Get first few meaningful lines
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 20]
        
        # Find the most substantial lines (likely headings or key content)
        substantial_lines = [line for line in lines[:20] if len(line) > 30 and len(line) < 200]
        
        if substantial_lines:
            return ' | '.join(substantial_lines[:3])
        else:
            return text[:300] + "..." if len(text) > 300 else text
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from chunk"""
        # Look for common technical terms and headings
        topics = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for headings (short lines, often capitalized)
            if 5 < len(line) < 80 and not line.endswith('.'):
                # Check if it looks like a heading
                if line.isupper() or (line[0].isupper() and line.count(' ') < 8):
                    topics.append(line)
        
        return topics[:10]  # Limit to 10 topics
    
    def get_toc_guided_analysis(self) -> Dict:
        """Get TOC-guided analysis for intelligent document navigation"""
        overview = self.get_document_overview()
        
        if 'error' in overview:
            return overview
        
        toc_analysis = {
            'document_info': {
                'title': overview['title'],
                'pages': overview['total_pages'],
                'type': overview['document_type']
            },
            'table_of_contents': overview['table_of_contents'],
            'toc_based_sections': [],
            'recommended_reading_order': []
        }
        
        # Analyze TOC for section importance
        if overview['table_of_contents']:
            for item in overview['table_of_contents']:
                section_info = self._analyze_toc_item(item)
                toc_analysis['toc_based_sections'].append(section_info)
            
            # Create recommended reading order
            toc_analysis['recommended_reading_order'] = self._create_reading_order(
                toc_analysis['toc_based_sections']
            )
        
        return toc_analysis
    
    def _analyze_toc_item(self, toc_item: str) -> Dict:
        """Analyze a TOC item to determine its importance and content type"""
        item_lower = toc_item.lower()
        
        # Determine section type and importance
        section_type = 'general'
        importance = 'medium'
        
        if any(keyword in item_lower for keyword in ['getting started', 'introduction', 'overview']):
            section_type = 'introduction'
            importance = 'high'
        elif any(keyword in item_lower for keyword in ['configuration', 'setup', 'installation']):
            section_type = 'configuration'
            importance = 'high'
        elif any(keyword in item_lower for keyword in ['reference', 'api', 'commands']):
            section_type = 'reference'
            importance = 'medium'
        elif any(keyword in item_lower for keyword in ['troubleshooting', 'error', 'problem']):
            section_type = 'troubleshooting'
            importance = 'high'
        elif any(keyword in item_lower for keyword in ['appendix', 'index', 'glossary']):
            section_type = 'appendix'
            importance = 'low'
        
        return {
            'title': toc_item,
            'type': section_type,
            'importance': importance,
            'keywords': self._extract_keywords_from_title(toc_item)
        }
    
    def _extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract keywords from a section title"""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        words = re.findall(r'\b[A-Za-z]{3,}\b', title.lower())
        return [word for word in words if word not in common_words][:5]
    
    def _create_reading_order(self, sections: List[Dict]) -> List[str]:
        """Create recommended reading order based on section analysis"""
        # Sort by importance and type
        priority_order = ['introduction', 'configuration', 'general', 'reference', 'troubleshooting', 'appendix']
        importance_order = ['high', 'medium', 'low']
        
        sorted_sections = sorted(sections, key=lambda x: (
            priority_order.index(x['type']) if x['type'] in priority_order else 99,
            importance_order.index(x['importance']) if x['importance'] in importance_order else 99
        ))
        
        return [section['title'] for section in sorted_sections]
    
    def _find_sections(self, text: str) -> List[str]:
        """Find major sections in chunk"""
        sections = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for section markers
            if any(marker in line.lower() for marker in ['chapter', 'section', 'overview', 'introduction', 'configuration', 'setup']):
                if 5 < len(line) < 100:
                    sections.append(line)
        
        return sections[:5]  # Limit to 5 sections

def study_pdf_with_toc_guidance(pdf_path: str) -> Dict:
    """Study a PDF with TOC guidance for intelligent analysis"""
    reader = PDFStudyReader(pdf_path)
    
    # Get TOC-guided analysis
    toc_analysis = reader.get_toc_guided_analysis()
    
    if 'error' in toc_analysis:
        return toc_analysis
    
    # Get targeted chunks based on TOC
    important_chunks = []
    chunk_count = 0
    
    for chunk in reader.study_document_by_chunks():
        chunk_count += 1
        important_chunks.append(chunk)
        
        # Limit chunks but prioritize based on TOC
        if chunk_count >= 3:  # Limit for context management
            break
    
    return {
        'toc_analysis': toc_analysis,
        'chunks_analyzed': len(important_chunks),
        'chunks': important_chunks,
        'toc_guided': True
    }

def study_pdf_comprehensively(pdf_path: str) -> Dict:
    """Legacy function - comprehensive PDF study (maintained for compatibility)"""
    reader = PDFStudyReader(pdf_path)
    
    # Get document overview
    overview = reader.get_document_overview()
    
    if 'error' in overview:
        return {'overview': overview, 'chunks_analyzed': 0, 'chunks': []}
    
    # Get all chunks
    chunks = []
    for chunk in reader.study_document_by_chunks():
        chunks.append(chunk)
        if len(chunks) >= 5:  # Limit for memory management
            break
    
    return {
        'overview': overview,
        'chunks_analyzed': len(chunks),
        'chunks': chunks
    }

# Test function
def test_study_reader():
    """Test the study reader"""
    pdf_path = r"D:\Kiro\ANA-050_to_Solution_ReferenceDocuments\Web_UI_UserGuide.pdf"
    
    print("=== PDF Study Reader Test ===")
    
    result = study_pdf_comprehensively(pdf_path)
    
    if 'error' not in result['overview']:
        print(f"Document: {result['overview']['title']}")
        print(f"Type: {result['overview']['document_type']}")
        print(f"Total pages: {result['overview']['total_pages']}")
        print(f"Chunks analyzed: {result['chunks_analyzed']}")
        
        print("\nTable of Contents:")
        for item in result['overview']['table_of_contents'][:5]:
            print(f"  - {item}")
        
        print(f"\nFirst chunk summary:")
        if result['chunks']:
            chunk = result['chunks'][0]
            print(f"  Pages: {chunk['pages']}")
            print(f"  Summary: {chunk['content_summary'][:200]}...")
            print(f"  Key topics: {', '.join(chunk['key_topics'][:3])}")
    else:
        print(f"Error: {result['overview']['error']}")

if __name__ == "__main__":
    test_study_reader()