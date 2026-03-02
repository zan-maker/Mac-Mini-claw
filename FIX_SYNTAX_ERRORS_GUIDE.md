# 🔧 FIX SYNTAX ERRORS GUIDE

## 🚨 **CRITICAL ISSUES FOUND:**

### **1. `scripts/b2b-referral-agentmail.py`**
- **Line 10:** Syntax error
- **Likely cause:** Unclosed string, missing parenthesis, or invalid indentation

### **2. `scripts/expense-reduction-agentmail.py`**
- **Line 20:** Syntax error
- **Likely cause:** Unclosed string, missing parenthesis, or invalid indentation

---

## 🔍 **DIAGNOSIS STEPS:**

### **Step 1: Check Syntax**
```bash
cd /Users/cubiczan/.openclaw/workspace/scripts

# Check b2b-referral-agentmail.py
python3 -m py_compile b2b-referral-agentmail.py

# Check expense-reduction-agentmail.py
python3 -m py_compile expense-reduction-agentmail.py
```

### **Step 2: View Problematic Lines**
```bash
# View lines around the error
head -15 b2b-referral-agentmail.py | cat -n
head -25 expense-reduction-agentmail.py | cat -n
```

### **Step 3: Common Fixes**

#### **If Unclosed String:**
```python
# ❌ BAD:
message = "This is a string that never ends

# ✅ GOOD:
message = "This is a string that never ends"
```

#### **If Missing Parenthesis:**
```python
# ❌ BAD:
result = function(param1, param2

# ✅ GOOD:
result = function(param1, param2)
```

#### **If Invalid Indentation:**
```python
# ❌ BAD:
def my_function():
print("Indented wrong")

# ✅ GOOD:
def my_function():
    print("Indented correctly")
```

---

## 🛠️ **QUICK FIX SCRIPT:**

Create this script to automatically check and suggest fixes:

```python
#!/usr/bin/env python3
"""
Auto-fix syntax errors in scripts
"""

import os
import sys

def check_syntax(filepath):
    """Check Python file syntax"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Try to compile
        compile(content, filepath, 'exec')
        print(f'✅ {filepath}: Syntax OK')
        return True
        
    except SyntaxError as e:
        print(f'❌ {filepath}: Syntax error')
        print(f'   Line {e.lineno}: {e.msg}')
        print(f'   Text: {e.text}')
        return False

def main():
    """Check all problematic files"""
    scripts_dir = 'scripts'
    problematic = [
        'b2b-referral-agentmail.py',
        'expense-reduction-agentmail.py'
    ]
    
    for script in problematic:
        filepath = os.path.join(scripts_dir, script)
        if os.path.exists(filepath):
            check_syntax(filepath)
        else:
            print(f'⚠️ {filepath}: File not found')

if __name__ == '__main__':
    main()
```

---

## 🔧 **MANUAL FIX INSTRUCTIONS:**

### **For `b2b-referral-agentmail.py`:**
1. Open the file:
   ```bash
   nano scripts/b2b-referral-agentmail.py
   ```

2. Go to line 10 (or around it):
   ```bash
   sed -n '5,15p' scripts/b2b-referral-agentmail.py
   ```

3. Look for:
   - Unclosed quotes (`"` or `'`)
   - Missing parentheses (`(` or `)`)
   - Missing brackets (`[` or `]`)
   - Missing braces (`{` or `}`)
   - Invalid indentation

### **For `expense-reduction-agentmail.py`:**
1. Open the file:
   ```bash
   nano scripts/expense-reduction-agentmail.py
   ```

2. Go to line 20 (or around it):
   ```bash
   sed -n '15,25p' scripts/expense-reduction-agentmail.py
   ```

3. Look for same issues as above.

---

## 🎯 **COMMON CULPRITS:**

### **1. Docstring Issues:**
```python
# ❌ BAD:
def function():
    """This docstring never ends

# ✅ GOOD:
def function():
    """This docstring ends properly"""
```

### **2. Multi-line String Issues:**
```python
# ❌ BAD:
message = """This is a
multi-line string
that never ends

# ✅ GOOD:
message = """This is a
multi-line string
that ends properly"""
```

### **3. Dictionary/Syntax Issues:**
```python
# ❌ BAD:
data = {
    "key1": "value1",
    "key2": "value2",
    # Missing closing brace

# ✅ GOOD:
data = {
    "key1": "value1",
    "key2": "value2",
}
```

---

## 🚀 **AFTER FIXING:**

### **1. Verify Fix:**
```bash
cd /Users/cubiczan/.openclaw/workspace
python3 simple_sandbox_test.py
```

### **Expected Result:**
- ✅ No critical issues
- ⚠️ Some warnings (acceptable)
- 💡 Recommendations for improvement

### **2. Test Execution:**
```bash
# Test in sandbox mode
export SANDBOX_MODE=1
python3 scripts/b2b-referral-agentmail.py --test
python3 scripts/expense-reduction-agentmail.py --test
```

### **3. Run Full Validation:**
```bash
python3 quick_sandbox_test.py
```

---

## 📞 **IF STUCK:**

### **Option 1: Comment Out Problematic Code**
```python
# Temporarily comment out the problematic section
# TODO: Fix syntax error on line 10
# problematic_code_here = "needs fixing"
```

### **Option 2: Replace With Simpler Version**
```python
# Replace complex code with simple working version
def simple_version():
    return "Working version for now"
```

### **Option 3: Ask for Help**
```bash
# Share the error and context
echo "Syntax error in line 10 of b2b-referral-agentmail.py"
sed -n '8,12p' scripts/b2b-referral-agentmail.py
```

---

## 🎉 **SUCCESS CRITERIA:**

### **Fixed When:**
1. **`python3 -m py_compile script.py`** returns no errors
2. **Static validation** shows no critical issues
3. **Script runs** in test mode without syntax errors
4. **All tests pass** in sandbox environment

### **Then You Can:**
1. ✅ Run production code with confidence
2. ✅ Deploy updated scripts
3. ✅ Monitor for runtime errors (not syntax)
4. ✅ Scale up operations

---

## 🔗 **NEXT STEPS AFTER FIX:**

1. **Move credentials** to environment variables
2. **Add error handling** to all scripts
3. **Create .env file** for secure configuration
4. **Test in sandbox** before production
5. **Monitor first runs** closely

**Fix these 2 syntax errors FIRST, then your system will be production-ready!** 🚀