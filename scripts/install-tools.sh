#!/bin/bash
# Install and start open-source tools for ChatGPT clone
# Run each tool in a separate terminal

echo "=================================================="
echo "Open-Source ChatGPT Clone - Tool Installer"
echo "=================================================="

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js not installed. Install with: brew install node"
fi

# Check npm
if command -v npm &> /dev/null; then
    echo "✅ npm: $(npm --version)"
else
    echo "❌ npm not installed"
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama: installed"
else
    echo "⚠️ Ollama not installed. Install from: https://ollama.ai"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version)"
else
    echo "⚠️ Docker not installed. Tools will run via npm."
fi

echo ""
echo "=================================================="
echo "Installation Commands"
echo "=================================================="

echo ""
echo "# 1. Install n8n (workflow engine)"
echo "npm install -g n8n"
echo "n8n start --port=5678"
echo ""

echo "# 2. Install Typebot CLI"
echo "npm install -g @typebot.io/cli"
echo ""

echo "# 3. Install Ollama (local LLM)"
echo "brew install ollama"
echo "ollama pull llama3"
echo "ollama serve"
echo ""

echo "# 4. Install WeasyPrint (PDF generation)"
echo "pip3 install weasyprint"
echo ""

echo "=================================================="
echo "Supabase Setup"
echo "=================================================="
echo ""
echo "1. Go to https://supabase.com"
echo "2. Create free account"
echo "3. Create new project"
echo "4. Get API URL and anon key"
echo "5. Add to .env file"
echo ""

echo "=================================================="
