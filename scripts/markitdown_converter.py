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
    
    def __init__(self, docintel_endpoint=None, llm_client=None, llm_model=None):
        """
        Initialize MarkItDown converter
        
        Args:
            docintel_endpoint: Azure Document Intelligence endpoint (optional)
            llm_client: LLM client for image descriptions (optional)
            llm_model: LLM model name for image descriptions (optional)
        """
        self.md = MarkItDown(
            docintel_endpoint=docintel_endpoint,
            llm_client=llm_client,
            llm_model=llm_model
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
                'title': result.title,
                'error': None
            }
            
            # Save to file if output path provided
            if output_path:
                # Create directory if it doesn't exist
                dirname = os.path.dirname(output_path)
                if dirname:  # Only create directory if path has a directory component
                    os.makedirs(dirname, exist_ok=True)
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
                'title': None
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
    parser.add_argument('--docintel-endpoint', help='Azure Document Intelligence endpoint')
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
    converter = OpenClawMarkItDown(docintel_endpoint=args.docintel_endpoint)
    
    # Check if input is file or directory
    if os.path.isfile(args.input):
        # Single file conversion
        result = converter.convert_file(args.input, args.output)
        
        if result['success']:
            print(f"✅ Successfully converted: {args.input}")
            print(f"📄 Output: {result.get('output_file', 'Not saved to file')}")
            print(f"📏 File size: {result['file_size']:,} bytes")
            if result['title']:
                print(f"📌 Title: {result['title']}")
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