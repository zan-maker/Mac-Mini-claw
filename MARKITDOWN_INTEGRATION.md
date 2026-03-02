# 🚀 **Microsoft MarkItDown Integration for OpenClaw**

## 📋 **Overview**

**MarkItDown** is a Microsoft Python utility that converts various file formats to Markdown for LLM consumption. This integration enables your OpenClaw system to automatically convert any attached file (Word, Excel, PDF, PowerPoint, images, etc.) to clean Markdown text that can be processed by your agents.

## 🎯 **Supported File Formats**

| Format | Extension | Status |
|--------|-----------|--------|
| **Microsoft Word** | .docx, .doc | ✅ Full support |
| **Microsoft Excel** | .xlsx, .xls | ✅ Full support |
| **Microsoft PowerPoint** | .pptx, .ppt | ✅ Full support |
| **PDF Documents** | .pdf | ✅ Full support |
| **Images** | .jpg, .png, .gif, .bmp | ✅ OCR + metadata |
| **Audio Files** | .mp3, .wav | ✅ Transcription |
| **HTML Pages** | .html | ✅ Full support |
| **Text Formats** | .csv, .json, .xml, .txt | ✅ Full support |
| **ZIP Archives** | .zip | ✅ Extracts & converts contents |
| **YouTube URLs** | URLs | ✅ Transcription |
| **EPub Books** | .epub | ✅ Full support |

## 🔧 **Installation**

### **1. Install MarkItDown with all dependencies:**
```bash
cd /Users/cubiczan/.openclaw/workspace
pip install 'markitdown[all]'
```

### **2. Verify installation:**
```bash
markitdown --version
python3 -c "from markitdown import MarkItDown; print('✅ MarkItDown installed successfully')"
```

### **3. Optional: Install specific dependencies only:**
```bash
# Minimal installation for your needs
pip install 'markitdown[docx, xlsx, pdf, pptx]'
```

## 🚀 **Integration Components**

### **1. Core Conversion Script:**
**File:** `scripts/markitdown_converter.py`
```python
#!/usr/bin/env python3
"""
MarkItDown File Converter for OpenClaw
Converts any attached file to Markdown for LLM processing
"""

import os
import sys
import argparse
from pathlib import Path
from markitdown import MarkItDown

class OpenClawMarkItDown:
    """MarkItDown integration for OpenClaw file conversion"""
    
    def __init__(self, enable_plugins=False, docintel_endpoint=None):
        """
        Initialize MarkItDown converter
        
        Args:
            enable_plugins: Enable third-party plugins
            docintel_endpoint: Azure Document Intelligence endpoint (optional)
        """
        self.md = MarkItDown(
            enable_plugins=enable_plugins,
            docintel_endpoint=docintel_endpoint
        )
        
    def convert_file(self, input_path, output_path=None):
        """
        Convert a file to Markdown
        
        Args:
            input_path: Path to input file
            output_path: Path to output Markdown file (optional)
            
        Returns:
            dict: Conversion results including text content and metadata
        """
        try:
            # Check if file exists
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Convert file
            result = self.md.convert(input_path)
            
            # Prepare output
            output = {
                'success': True,
                'input_file': input_path,
                'file_size': os.path.getsize(input_path),
                'file_type': Path(input_path).suffix.lower(),
                'text_content': result.text_content,
                'metadata': result.metadata,
                'conversion_time': result.conversion_time,
                'error': None
            }
            
            # Save to file if output path provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                output['output_file'] = output_path
            
            return output
            
        except Exception as e:
            return {
                'success': False,
                'input_file': input_path,
                'error': str(e),
                'text_content': None,
                'metadata': None
            }
    
    def convert_directory(self, input_dir, output_dir=None, extensions=None):
        """
        Convert all files in a directory
        
        Args:
            input_dir: Directory containing files to convert
            output_dir: Directory to save converted files (optional)
            extensions: List of file extensions to convert (optional)
            
        Returns:
            list: Results for each converted file
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        results = []
        input_path = Path(input_dir)
        
        # Default extensions to convert
        if extensions is None:
            extensions = ['.docx', '.xlsx', '.pptx', '.pdf', '.jpg', '.png', '.html']
        
        # Find all matching files
        for ext in extensions:
            for file_path in input_path.rglob(f"*{ext}"):
                # Determine output path
                if output_dir:
                    rel_path = file_path.relative_to(input_dir)
                    output_path = Path(output_dir) / rel_path.with_suffix('.md')
                else:
                    output_path = None
                
                # Convert file
                result = self.convert_file(str(file_path), str(output_path) if output_path else None)
                results.append(result)
        
        return results
    
    def batch_convert(self, file_list, output_dir=None):
        """
        Convert a list of files
        
        Args:
            file_list: List of file paths to convert
            output_dir: Directory to save converted files (optional)
            
        Returns:
            list: Results for each converted file
        """
        results = []
        
        for file_path in file_list:
            # Determine output path
            if output_dir:
                filename = Path(file_path).stem
                output_path = os.path.join(output_dir, f"{filename}.md")
            else:
                output_path = None
            
            # Convert file
            result = self.convert_file(file_path, output_path)
            results.append(result)
        
        return results

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='Convert files to Markdown using MarkItDown')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('--enable-plugins', action='store_true', help='Enable third-party plugins')
    parser.add_argument('--list-formats', action='store_true', help='List supported file formats')
    
    args = parser.parse_args()
    
    # List supported formats
    if args.list_formats:
        print("📋 Supported File Formats:")
        print("="*50)
        formats = [
            ("Word Documents", ".docx, .doc"),
            ("Excel Spreadsheets", ".xlsx, .xls"),
            ("PowerPoint Presentations", ".pptx, .ppt"),
            ("PDF Documents", ".pdf"),
            ("Images", ".jpg, .png, .gif, .bmp, .tiff"),
            ("Audio Files", ".mp3, .wav, .m4a"),
            ("HTML Pages", ".html, .htm"),
            ("Text Formats", ".txt, .csv, .json, .xml"),
            ("ZIP Archives", ".zip"),
            ("EPub Books", ".epub"),
        ]
        for name, exts in formats:
            print(f"  • {name}: {exts}")
        return
    
    # Initialize converter
    converter = OpenClawMarkItDown(enable_plugins=args.enable_plugins)
    
    # Check if input is file or directory
    if os.path.isfile(args.input):
        # Single file conversion
        result = converter.convert_file(args.input, args.output)
        
        if result['success']:
            print(f"✅ Successfully converted: {args.input}")
            print(f"📄 Output: {result.get('output_file', 'Not saved to file')}")
            print(f"📏 File size: {result['file_size']:,} bytes")
            print(f"⏱️ Conversion time: {result['conversion_time']:.2f}s")
            print(f"📝 Preview (first 500 chars):")
            print("-"*50)
            print(result['text_content'][:500] + "..." if len(result['text_content']) > 500 else result['text_content'])
            print("-"*50)
        else:
            print(f"❌ Conversion failed: {result['error']}")
            sys.exit(1)
            
    elif os.path.isdir(args.input):
        # Directory conversion
        if not args.output:
            print("❌ Output directory required for batch conversion")
            sys.exit(1)
        
        print(f"📁 Converting all files in: {args.input}")
        print(f"📁 Saving to: {args.output}")
        
        results = converter.convert_directory(args.input, args.output)
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        failed = sum(1 for r in results if not r['success'])
        
        print(f"\n📊 Conversion Summary:")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📄 Total: {len(results)}")
        
        # Show failed files
        if failed > 0:
            print(f"\n❌ Failed conversions:")
            for result in results:
                if not result['success']:
                    print(f"  • {result['input_file']}: {result['error']}")
                    
    else:
        print(f"❌ Input not found: {args.input}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### **2. Discord/Telegram Integration Script:**
**File:** `scripts/auto_convert_attachments.py`
```python
#!/usr/bin/env python3
"""
Automatic Attachment Converter for OpenClaw
Monitors message channels for file attachments and converts them to Markdown
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from markitdown_converter import OpenClawMarkItDown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/markitdown.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AttachmentConverter:
    """Monitor and convert file attachments automatically"""
    
    def __init__(self, watch_dir=None, output_dir=None):
        """
        Initialize attachment converter
        
        Args:
            watch_dir: Directory to watch for new files
            output_dir: Directory to save converted files
        """
        self.watch_dir = watch_dir or "/Users/cubiczan/.openclaw/workspace/uploads"
        self.output_dir = output_dir or "/Users/cubiczan/.openclaw/workspace/converted"
        self.converter = OpenClawMarkItDown()
        
        # Create directories if they don't exist
        os.makedirs(self.watch_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Track processed files
        self.processed_file = os.path.join(self.output_dir, "processed_files.json")
        self.processed = self.load_processed()
        
        logger.info(f"📁 Watching directory: {self.watch_dir}")
        logger.info(f"📁 Output directory: {self.output_dir}")
    
    def load_processed(self):
        """Load list of processed files"""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_processed(self):
        """Save list of processed files"""
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed), f)
    
    def is_supported_file(self, filepath):
        """Check if file format is supported"""
        supported_extensions = {
            '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
            '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.html', '.htm', '.csv', '.json', '.xml', '.txt',
            '.zip', '.epub', '.mp3', '.wav'
        }
        return Path(filepath).suffix.lower() in supported_extensions
    
    def process_file(self, filepath):
        """Process a single file"""
        filename = Path(filepath).name
        file_id = f"{filename}_{os.path.getsize(filepath)}"
        
        # Skip if already processed
        if file_id in self.processed:
            logger.info(f"⏭️ Already processed: {filename}")
            return None
        
        # Check if supported
        if not self.is_supported_file(filepath):
            logger.warning(f"❌ Unsupported format: {filename}")
            return None
        
        # Generate output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{Path(filepath).stem}_{timestamp}.md"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Convert file
        logger.info(f"🔄 Converting: {filename}")
        result = self.converter.convert_file(filepath, output_path)
        
        if result['success']:
            # Mark as processed
            self.processed.add(file_id)
            self.save_processed()
            
            logger.info(f"✅ Converted: {filename} → {output_filename}")
            logger.info(f"   Size: {result['file_size']:,} bytes")
            logger.info(f"   Time: {result['conversion_time']:.2f}s")
            
            # Create summary file
            summary_path = output_path.replace('.md', '_summary.json')
            with open(summary_path, 'w') as f:
                json.dump({
                    'original_file': filename,
                    'converted_file': output_filename,
                    'conversion_time': result['conversion_time'],
                    'file_size': result['file_size'],
                    'file_type': result['file_type'],
                    'timestamp': timestamp
                }, f, indent=2)
            
            return {
                'original': filename,
                'converted': output_filename,
                'path': output_path,
                'summary': summary_path,
                'preview': result['text_content'][:1000]  # First 1000 chars
            }
        else:
            logger.error(f"❌ Failed to convert {filename}: {result['error']}")
            return None
    
    def watch_and_process(self, interval=5):
        """Watch directory for new files and process them"""
        logger.info(f"👀 Starting to watch directory (interval: {interval}s)")
        
        try:
            while True:
                # Scan directory for new files
                for filename in os.listdir(self.watch_dir):
                    filepath = os.path.join(self.watch_dir, filename)
                    
                    # Skip directories
                    if not os.path.isfile(filepath):
                        continue
                    
                    # Process file
                    result = self.process_file(filepath)
                    
                    # If successful, optionally move original file
                    if result:
                        archive_dir = os.path.join(self.watch_dir, "archive")
                        os.makedirs(archive_dir, exist_ok=True)
                        archive_path = os.path.join(archive_dir, filename)
                        os.rename(filepath, archive_path)
                        logger.info(f"📦 Archived original: {archive_path}")
                
                # Wait before next scan
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Stopping directory watch")
        except Exception as e:
            logger.error(f"💥 Error in watch loop: {e}")

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automatically convert file attachments')
    parser.add_argument('--watch', action='store_true', help='Watch directory for new files')
    parser.add_argument('--convert', help='Convert specific file or directory')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--interval', type=int, default=5, help='Watch interval in seconds')
    
    args = parser.parse_args()
    
    converter = AttachmentConverter(output_dir=args.output)
    
    if args.convert:
        # Convert specific file or directory
        if os.path.isfile(args.convert):
            result = converter.process_file(args.convert)
            if result:
                print(f"✅ Converted: {result['original']}")
                print(f"📄 Output: {result['converted']}")
                print(f"📝 Preview: {result['preview'][:500]}...")
            else:
                print(f"❌ Failed to convert: {args.convert}")
        elif os.path.isdir(args.convert):
            print(f"📁 Converting directory: {args.convert}")
            # Implementation for directory conversion
        else:
            print(f"❌ Not found: {args.convert}")
    
    elif args.watch:
        # Start watching directory
        converter.watch_and_process(interval=args.interval)
    
    else:
        print("Please specify --watch to monitor directory or --convert to convert specific file")

if __name__ == "__main__":
    main()
```

### **3. OpenClaw Skill Integration:**
**File:** `/Users/cubiczan/mac-bot/skills/markitdown-converter/SKILL.md`
```markdown
# MarkItDown File Converter Skill

## Description
Convert any file attachment (Word, Excel, PDF, PowerPoint, images, etc.) to Markdown for LLM processing. This skill enables OpenClaw agents to read and analyze content from various file formats.

## Usage

### Basic Commands:
```bash
# Convert a single file
markitdown path/to/document.docx -o output.md

# Convert all files