"""Fix stray path strings inside generator expressions in build-pages.py."""
import re

with open("scripts/build-pages.py", "r", encoding="utf-8") as f:
    c = f.read()

original = c

# Fix 1: proj_items - stray /why-choose-us.html
# Pattern: '    if i != 6...,\n    "/why-choose-us.html"\n)'
c = re.sub(
    r'(    if i != 6 and i != 11 and i != 12[^\n]*),\n    "[^"]+"\n\)',
    r'\1\n)',
    c
)

# Fix 2: faq_html - stray /projects.html
# Pattern: '    for q, a in faqs,\n    "/projects.html"\n)'
c = re.sub(
    r'(    for q, a in faqs),\n    "[^"]+"\n\)',
    r'\1\n)',
    c
)

# Also check for any other generator with trailing stray path
c = re.sub(
    r'(    for \w[\w, ]+ in \w+),\n    "[^"]+"\n\)',
    r'\1\n)',
    c
)

changed = c != original
print(f"Changes made: {changed}")

with open("scripts/build-pages.py", "w", encoding="utf-8") as f:
    f.write(c)

# Verify no syntax error
import ast
try:
    ast.parse(c)
    print("Syntax OK")
except SyntaxError as e:
    print(f"Syntax error at line {e.lineno}: {e.msg}")
    # Show context
    lines = c.splitlines()
    start = max(0, e.lineno - 3)
    end   = min(len(lines), e.lineno + 2)
    for i, line in enumerate(lines[start:end], start=start+1):
        marker = ">>>" if i == e.lineno else "   "
        print(f"  {marker} {i}: {line}")
