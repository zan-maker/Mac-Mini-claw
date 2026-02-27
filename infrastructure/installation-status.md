# Installation Status - 2026-02-16

## ✅ Successfully Installed

### n8n (Workflow Engine)
- **Version:** 2.7.5
- **Location:** `/usr/local/bin/n8n`
- **Start:** `n8n start --port=5678`
- **Access:** http://localhost:5678

### Ollama (Local LLM)
- **Version:** 0.15.6
- **Location:** `/usr/local/bin/ollama`
- **Start:** `brew services start ollama`
- **Pull model:** `ollama pull llama3`
- **API:** http://localhost:11434

## ⚠️ Pending Fix

### WeasyPrint (PDF Generation)
- **Issue:** Missing `libgobject-2.0-0` library on macOS
- **Fix needed:**
  ```bash
  brew install pango gdk-pixbuf libffi gobject-introspection
  export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig"
  pip3 install weasyprint --user --break-system-packages
  ```

### Alternative PDF Options
- **md2pdf:** Markdown to PDF
- **pdfkit:** wkhtmltopdf wrapper
- **ReportLab:** Pure Python PDF (no system deps)

---

## Starting n8n

```bash
# Start n8n server
n8n start

# Access at http://localhost:5678
# Create first workflow for lead capture
```

## Starting Ollama

```bash
# Start Ollama service
brew services start ollama

# Pull a model
ollama pull llama3

# Test
ollama run llama3 "Hello, how are you?"
```

---

*Updated: 2026-02-16*
