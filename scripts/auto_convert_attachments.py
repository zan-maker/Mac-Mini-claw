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

# Try to import MarkItDown
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    logger.error("❌ MarkItDown not installed. Run: pip install 'markitdown[all]'")
    MARKITDOWN_AVAILABLE = False

class AttachmentConverter:
    """Monitor and convert file attachments automatically"""
    
    def __init__(self, watch_dir=None, output_dir=None):
        """
        Initialize attachment converter
        
        Args:
            watch_dir: Directory to watch for new files
            output_dir: Directory to save converted files
        """
        if not MARKITDOWN_AVAILABLE:
            raise ImportError("MarkItDown not installed. Please install with: pip install 'markitdown[all]'")
        
        self.watch_dir = watch_dir or "/Users/cubiczan/.openclaw/workspace/uploads"
        self.output_dir = output_dir or "/Users/cubiczan/.openclaw/workspace/converted"
        self.converter = MarkItDown()
        
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
    
    def convert_file(self, filepath, output_path):
        """Convert a file using MarkItDown"""
        try:
            result = self.converter.convert(filepath)
            
            # Save to file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            return {
                'success': True,
                'text_content': result.text_content,
                'title': result.title,
                'file_size': os.path.getsize(filepath),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text_content': None,
                'metadata': None
            }
    
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
        result = self.convert_file(filepath, output_path)
        
        if result['success']:
            # Mark as processed
            self.processed.add(file_id)
            self.save_processed()
            
            logger.info(f"✅ Converted: {filename} → {output_filename}")
            logger.info(f"   Size: {result['file_size']:,} bytes")
            if result['title']:
                logger.info(f"   Title: {result['title']}")
            
            # Create summary file
            summary_path = output_path.replace('.md', '_summary.json')
            with open(summary_path, 'w') as f:
                json.dump({
                    'original_file': filename,
                    'converted_file': output_filename,
                    'title': result['title'],
                    'file_size': result['file_size'],
                    'file_type': Path(filepath).suffix.lower(),
                    'timestamp': timestamp,
                    'preview': result['text_content'][:500] if result['text_content'] else ''
                }, f, indent=2)
            
            return {
                'original': filename,
                'converted': output_filename,
                'path': output_path,
                'summary': summary_path,
                'preview': result['text_content'][:1000] if result['text_content'] else ''
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
    
    if not MARKITDOWN_AVAILABLE:
        print("❌ MarkItDown not installed. Please install with:")
        print("   pip install 'markitdown[all]'")
        sys.exit(1)
    
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