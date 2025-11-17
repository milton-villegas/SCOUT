# Message Standardization Analysis

## Industry Best Practices

### 1. Material Design (Google)
```
ERROR:
❌ Title: Clear, specific noun phrase
   Body: What happened + Why + How to fix
   Example: "Upload Failed"
           "The file size exceeds the 10MB limit.
            Please compress or choose a smaller file."

SUCCESS:
✅ Title: Action completed
   Body: What was done + Result
   Example: "File Uploaded"
           "profile.jpg was saved to your library."

WARNING:
⚠️  Title: Potential issue
   Body: What might happen + Suggested action
   Example: "Low Storage"
           "You have less than 10% storage remaining.
            Delete files or upgrade storage."
```

### 2. Apple Human Interface Guidelines
```
- Use title case for dialog titles
- Use sentence case for message body
- Be specific and clear
- Avoid technical jargon
- Provide actionable next steps
- Use "OK" and "Cancel" (not "Yes/No" for actions)

ERROR: "The document couldn't be opened"
       "The file may be damaged or use a format that Preview doesn't recognize."
       [Show in Finder] [Cancel]

SUCCESS: "Export Complete"
         "The document was exported as PDF."
         [Open] [Done]
```

### 3. Microsoft Fluent Design
```
- Main instruction: Bold, brief (one sentence)
- Supplemental instruction: Explain details
- Commitment buttons: Specific actions (not just OK)

ERROR: Main: "Can't connect to database"
       Detail: "Check your network connection and try again."
       [Retry] [Cancel]

INFO:  Main: "Do you want to save changes?"
       Detail: "Your changes will be lost if you don't save them."
       [Save] [Don't Save] [Cancel]
```

---

## Current State in Your Code

### ✅ GOOD Patterns (Keep These!)

#### 1. Detailed Error with Context + Solutions
```python
# EXCELLENT! Follows best practices
messagebox.showerror("Invalid Concentrations",
    f"The following concentration(s) EXCEED the stock concentration:\n\n"
    f"Stock: {stock_base} {unit}\n"
    f"Invalid levels: {', '.join(invalid_levels)}\n\n"
    f"⚠️ You cannot make a solution more concentrated than your stock!\n\n"
    f"Either:\n"
    f"• Increase stock concentration, OR\n"
    f"• Reduce the level values")
```
**Why it's good:**
- ✅ Clear title
- ✅ Shows what's wrong (with values)
- ✅ Explains why it's wrong
- ✅ Provides specific solutions
- ✅ Uses visual indicators (⚠️, •)

#### 2. Structured Success Messages
```python
# EXCELLENT! Clean and organized
messagebox.showinfo("Export Complete",
    f"Files saved:\n\n"
    f"    {xlsx_filename}\n"
    f"    {csv_filename}\n\n"
    f"Location:\n"
    f"    {directory}")
```
**Why it's good:**
- ✅ Clear title
- ✅ Lists what was done
- ✅ Shows file paths clearly
- ✅ Consistent formatting

#### 3. Console Messages with Visual Indicators
```python
# EXCELLENT! Easy to scan
print(f"✓ Successfully exported:")
print(f"  Excel: {excel_path}")
print(f"  CSV: {csv_path}")
print(f"  Rows added: {len(new_excel_rows)}")

print(f"⚠ Could not extract feature importances, falling back to range-based selection")
```
**Why it's good:**
- ✅ Visual indicators (✓, ⚠, ℹ️)
- ✅ Indentation for hierarchy
- ✅ Consistent format

---

### ❌ INCONSISTENT Patterns (Need Fixing)

#### 1. Generic Error Titles
```python
# INCONSISTENT - Too generic
messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
messagebox.showerror("Error", f"Analysis failed:\n{str(e)}")
messagebox.showerror("Error", str(e))

# BETTER:
messagebox.showerror("File Load Failed",
    f"Could not open the selected file.\n\n"
    f"Details: {str(e)}\n\n"
    f"Make sure the file is not open in another program.")

messagebox.showerror("Analysis Error",
    f"Statistical analysis could not be completed.\n\n"
    f"Error: {str(e)}\n\n"
    f"Check that your data includes all required columns.")
```

#### 2. Inconsistent Title Case
```python
# MIXED - Some title case, some sentence case
"Invalid Value"        # ✓ Title case
"Invalid Input"        # ✓ Title case
"No Levels"           # ✓ Title case
"No Selection"        # ✓ Title case

"Already Added"       # ✗ Doesn't match pattern
"Export Failed"       # ✓ Good
"Missing Library"     # ✓ Good

# Should be consistent - Use Title Case for All
```

#### 3. Inconsistent Punctuation
```python
# MIXED - Some have periods, some don't
"Step must be positive."           # Has period
"Please enter a factor name."      # Has period
"Factor name cannot be empty"      # No period
"At least one level is required"   # No period

# Should be consistent - periods for full sentences only
```

#### 4. Yes/No vs Specific Actions
```python
# CURRENT:
messagebox.askyesno("Confirm Delete",
    f"Are you sure you want to delete '{factor_name}'?")

# BETTER (more specific):
response = messagebox.askquestion("Delete Factor",
    f"Delete '{factor_name}'?\n\n"
    f"This action cannot be undone.",
    icon='warning')
# Returns 'yes' or 'no'

# OR use custom dialog with specific buttons:
# [Delete] [Cancel]
```

#### 5. Console Print Inconsistency
```python
# MIXED STYLES:
print("Warning: Ax not available. Install with: pip install ax-platform")  # Plain
print(f"⚠ Could not extract feature importances...")                       # With emoji
print(f"✓ Using feature importances for factor selection")                 # With emoji

# Should use consistent emoji indicators
```

---

## Proposed Standardization

### Message Style Guide

#### 1. Dialog Titles (Always Title Case)
```
✅ Good:
- "Invalid Concentration"
- "Export Complete"
- "Delete Factor"
- "Analysis Error"

❌ Bad:
- "Error" (too generic)
- "invalid value" (not title case)
- "Export failed" (not title case)
```

#### 2. Error Messages (Problem + Reason + Solution)
```python
# TEMPLATE:
messagebox.showerror("Specific Error Title",
    f"[What happened]\n\n"
    f"[Why it happened]\n\n"
    f"[How to fix it]")

# EXAMPLES:
messagebox.showerror("File Not Found",
    f"Could not open '{filename}'.\n\n"
    f"The file may have been moved or deleted.\n\n"
    f"Please check the file path and try again.")

messagebox.showerror("Invalid pH Range",
    f"pH value {value} is out of range.\n\n"
    f"pH must be between 1.0 and 14.0.\n\n"
    f"Enter a value within the valid range.")
```

#### 3. Warning Messages (Issue + Impact + Action)
```python
# TEMPLATE:
messagebox.showwarning("Warning Title",
    f"[What's the issue]\n\n"
    f"[What might happen]\n\n"
    f"[Suggested action]")

# EXAMPLE:
messagebox.showwarning("Large Design",
    f"This design will create 256 combinations.\n\n"
    f"This may take several minutes to generate.\n\n"
    f"Consider using a smaller design or Latin Hypercube Sampling.")
```

#### 4. Success Messages (Action + Result)
```python
# TEMPLATE:
messagebox.showinfo("Action Complete",
    f"[What was done]\n\n"
    f"[Results/details]")

# EXAMPLE:
messagebox.showinfo("Export Complete",
    f"Design exported successfully.\n\n"
    f"Files saved:\n"
    f"  • {xlsx_filename}\n"
    f"  • {csv_filename}\n\n"
    f"Location: {directory}")
```

#### 5. Info/Help Messages (Topic + Details)
```python
# TEMPLATE:
messagebox.showinfo("Topic Title",
    f"[Main explanation]\n\n"
    f"[Additional details]")

# EXAMPLE:
messagebox.showinfo("About Latin Hypercube Sampling",
    f"LHS creates a space-filling design that efficiently explores "
    f"the parameter space with fewer experimental runs.\n\n"
    f"Recommended for:\n"
    f"  • Large factor spaces (5+ factors)\n"
    f"  • Limited experimental budget\n"
    f"  • Initial screening experiments")
```

#### 6. Console Messages (Always with Indicators)
```python
# STANDARD INDICATORS:
ℹ️  = Info/Notice
✓ = Success/Completed
⚠ = Warning/Caution
❌ = Error/Failed
🔧 = Action needed

# EXAMPLES:
print(f"ℹ️  Loading data from {filename}...")
print(f"✓ Analysis complete: R² = {r2:.3f}")
print(f"⚠ Low R² value ({r2:.3f}) - model may not fit well")
print(f"❌ Export failed: {error}")
print(f"🔧 Install required package: pip install ax-platform")
```

#### 7. Confirmation Dialogs (Specific Actions)
```python
# TEMPLATE:
messagebox.askyesno("Action Confirmation",
    f"[What will happen]\n\n"
    f"[Warning if irreversible]")

# EXAMPLE:
messagebox.askyesno("Delete Factor",
    f"Delete '{factor_name}' from the design?\n\n"
    f"This action cannot be undone.")
```

#### 8. Validation Messages (Inline)
```python
# TEMPLATE (return tuple):
(is_valid, error_message)

# EXAMPLES:
(True, "")
(False, "pH must be between 1.0 and 14.0")
(False, "Stock concentration cannot be less than final concentration")
```

---

## Centralized Message Constants

### Create: `core/messages.py`

```python
"""
Centralized user-facing messages for consistency.
"""

class MessageTemplates:
    """Standard message templates."""

    # Error messages
    ERRORS = {
        'file_not_found': (
            "File Not Found",
            "Could not open '{filename}'.\n\n"
            "The file may have been moved or deleted.\n\n"
            "Please check the file path and try again."
        ),
        'invalid_ph': (
            "Invalid pH Value",
            "pH value {value} is out of range.\n\n"
            "pH must be between {min} and {max}.\n\n"
            "Enter a value within the valid range."
        ),
        'stock_exceeded': (
            "Stock Concentration Exceeded",
            "Final concentration ({final} {unit}) exceeds stock ({stock} {unit}).\n\n"
            "You cannot make a solution more concentrated than the stock.\n\n"
            "Either increase the stock concentration or reduce the final concentration."
        ),
        # ... more
    }

    # Success messages
    SUCCESS = {
        'export_complete': (
            "Export Complete",
            "Files saved:\n\n"
            "  • {xlsx_file}\n"
            "  • {csv_file}\n\n"
            "Location: {directory}"
        ),
        'analysis_complete': (
            "Analysis Complete",
            "Statistical analysis finished successfully.\n\n"
            "Model: {model}\n"
            "R²: {r2:.4f}\n"
            "Observations: {n}"
        ),
        # ... more
    }

    # Console indicators
    CONSOLE = {
        'info': 'ℹ️ ',
        'success': '✓ ',
        'warning': '⚠ ',
        'error': '❌ ',
        'action': '🔧 ',
    }

    @staticmethod
    def format_error(key, **kwargs):
        """Format an error message."""
        title, template = MessageTemplates.ERRORS[key]
        message = template.format(**kwargs)
        return title, message

    @staticmethod
    def format_success(key, **kwargs):
        """Format a success message."""
        title, template = MessageTemplates.SUCCESS[key]
        message = template.format(**kwargs)
        return title, message

# Usage:
from core.messages import MessageTemplates

title, message = MessageTemplates.format_error('invalid_ph',
    value=15.0, min=1.0, max=14.0)
messagebox.showerror(title, message)
```

---

## Comparison Table

| Aspect | Industry Standard | Current Code | Recommendation |
|--------|------------------|--------------|----------------|
| **Title Case** | Always Title Case | Mixed | ✅ Standardize to Title Case |
| **Error Structure** | Problem + Reason + Solution | Mixed (some good, some generic) | ✅ Use 3-part template |
| **Console Indicators** | Consistent symbols | Mixed (some have ℹ️✓⚠, some plain) | ✅ Always use indicators |
| **Punctuation** | Periods for complete sentences | Mixed | ✅ Consistent rules |
| **Generic Titles** | Specific (e.g., "File Not Found") | Often just "Error" | ✅ Always be specific |
| **Confirmation Dialogs** | Specific actions | Uses Yes/No | ✅ Consider specific buttons |
| **Message Organization** | Visual hierarchy (bullets, spacing) | Good! (already using) | ✅ Keep current approach |
| **Context in Errors** | Always provide | Sometimes missing | ✅ Always include context |

---

## Priority Fixes

### High Priority (User-Facing Dialogs)
1. ✅ Replace all generic "Error" titles with specific ones
2. ✅ Standardize to Title Case for all dialog titles
3. ✅ Add context and solutions to simple error messages
4. ✅ Create centralized message templates

### Medium Priority (Console Output)
5. ✅ Add emoji indicators to all console messages
6. ✅ Consistent indentation for hierarchical info

### Low Priority (Nice to Have)
7. ⭕ Consider custom dialogs with specific action buttons
8. ⭕ Add message categories (severity levels)

---

## Implementation Plan

1. **Create `core/messages.py`** with centralized templates
2. **Update GUI files** to use message templates
3. **Update console output** to use consistent indicators
4. **Update exception messages** in core modules
5. **Test all message scenarios**

---

## Examples to Fix

### Before → After

#### Generic Error
```python
# BEFORE:
messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

# AFTER:
messagebox.showerror("File Load Failed",
    f"Could not open the selected file.\n\n"
    f"Details: {str(e)}\n\n"
    f"Make sure the file is not open in another program.")
```

#### Plain Console
```python
# BEFORE:
print("Warning: Ax not available. Install with: pip install ax-platform")

# AFTER:
print(f"⚠ Bayesian Optimization unavailable")
print(f"🔧 Install required package: pip install ax-platform")
```

#### Simple Validation
```python
# BEFORE:
messagebox.showerror("Invalid Value", error_msg)

# AFTER:
messagebox.showerror("Invalid pH Value",
    f"pH value {value} is out of range.\n\n"
    f"pH must be between 1.0 and 14.0.\n\n"
    f"Enter a value within the valid range.")
```
