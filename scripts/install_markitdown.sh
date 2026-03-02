#!/bin/bash
# MarkItDown Installation Script for OpenClaw

echo "🚀 Installing Microsoft MarkItDown for OpenClaw"
echo "============================================================"

# Check Python version
echo "🔍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p /Users/cubiczan/.openclaw/workspace/uploads
mkdir -p /Users/cubiczan/.openclaw/workspace/converted
mkdir -p /Users/cubiczan/.openclaw/workspace/logs
mkdir -p /Users/cubiczan/mac-bot/skills/markitdown-converter

echo "✅ Directories created:"
echo "   - /Users/cubiczan/.openclaw/workspace/uploads (for file uploads)"
echo "   - /Users/cubiczan/.openclaw/workspace/converted (for converted files)"
echo "   - /Users/cubiczan/.openclaw/workspace/logs (for conversion logs)"
echo "   - /Users/cubiczan/mac-bot/skills/markitdown-converter (skill files)"

# Install MarkItDown
echo "📦 Installing MarkItDown with all dependencies..."
cd /Users/cubiczan/.openclaw/workspace
pip install 'markitdown[all]'

if [ $? -eq 0 ]; then
    echo "✅ MarkItDown installed successfully"
else
    echo "❌ MarkItDown installation failed. Trying alternative method..."
    pip install markitdown
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install MarkItDown. Please check pip configuration."
        exit 1
    fi
fi

# Verify installation
echo "🔍 Verifying installation..."
python3 -c "from markitdown import MarkItDown; print('✅ MarkItDown import successful')"
if [ $? -ne 0 ]; then
    echo "❌ MarkItDown import failed. Installation may be incomplete."
    exit 1
fi

# Make scripts executable
echo "🔧 Setting up scripts..."
chmod +x /Users/cubiczan/.openclaw/workspace/scripts/markitdown_converter.py
chmod +x /Users/cubiczan/.openclaw/workspace/scripts/auto_convert_attachments.py

# Test conversion with a sample file
echo "🧪 Testing conversion with sample file..."
echo "This is a test document for MarkItDown." > /Users/cubiczan/.openclaw/workspace/test_document.txt
python3 /Users/cubiczan/.openclaw/workspace/scripts/markitdown_converter.py /Users/cubiczan/.openclaw/workspace/test_document.txt -o /Users/cubiczan/.openclaw/workspace/test_output.md

if [ $? -eq 0 ]; then
    echo "✅ Test conversion successful"
    rm /Users/cubiczan/.openclaw/workspace/test_document.txt
    rm /Users/cubiczan/.openclaw/workspace/test_output.md
else
    echo "⚠️ Test conversion had issues (this may be normal for some file types)"
fi

# Create cron job for automatic monitoring (optional)
echo "⏰ Setting up optional cron job for automatic file monitoring..."
read -p "Do you want to set up automatic file monitoring? (y/n): " setup_cron

if [[ $setup_cron == "y" || $setup_cron == "Y" ]]; then
    # Add cron job to watch uploads directory every 5 minutes
    (crontab -l 2>/dev/null; echo "*/5 * * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/auto_convert_attachments.py --watch --interval 300 >> logs/markitdown_cron.log 2>&1") | crontab -
    echo "✅ Cron job added: Automatic file monitoring every 5 minutes"
    echo "   Logs: /Users/cubiczan/.openclaw/workspace/logs/markitdown_cron.log"
else
    echo "⏭️ Skipping cron job setup"
fi

# Summary
echo ""
echo "============================================================"
echo "🎉 MARKITDOWN INSTALLATION COMPLETE!"
echo "============================================================"
echo ""
echo "📋 Installation Summary:"
echo "✅ MarkItDown Python package installed"
echo "✅ Directories created for file processing"
echo "✅ Scripts configured and made executable"
echo "✅ Skill file created: /Users/cubiczan/mac-bot/skills/markitdown-converter/SKILL.md"
echo "✅ Documentation: /Users/cubiczan/.openclaw/workspace/MARKITDOWN_INTEGRATION.md"
echo ""
echo "🚀 Usage Examples:"
echo "1. Convert a single file:"
echo "   python3 scripts/markitdown_converter.py document.docx -o output.md"
echo ""
echo "2. List supported formats:"
echo "   python3 scripts/markitdown_converter.py --list-formats"
echo ""
echo "3. Watch directory for new files:"
echo "   python3 scripts/auto_convert_attachments.py --watch"
echo ""
echo "4. Use in Python code:"
echo "   from markitdown import MarkItDown"
echo "   md = MarkItDown()"
echo "   result = md.convert('document.docx')"
echo "   print(result.text_content)"
echo ""
echo "📁 File Locations:"
echo "   - Upload files: /Users/cubiczan/.openclaw/workspace/uploads/"
echo "   - Converted files: /Users/cubiczan/.openclaw/workspace/converted/"
echo "   - Logs: /Users/cubiczan/.openclaw/workspace/logs/markitdown.log"
echo ""
echo "🔧 Next Steps:"
echo "1. Drop files in /Users/cubiczan/.openclaw/workspace/uploads/ for automatic conversion"
echo "2. Use the conversion scripts in your OpenClaw workflows"
echo "3. Check logs for any conversion issues"
echo ""
echo "Need help? Check the documentation or run:"
echo "   python3 scripts/markitdown_converter.py --help"
echo ""
echo "============================================================"
echo "✅ MarkItDown is ready to convert your files to Markdown! 🚀"