import re
with open("scripts/build-pages.py","r",encoding="utf-8") as f:
    c = f.read()
before = c.count("/why-choose-us.html")
# Remove the stray path and trailing comma from the proj_items generator
c = re.sub(
    r'(if i != 6 and i != 11 and i != 12[^\n]*),\n\s+"/why-choose-us\.html"',
    r'\1',
    c
)
after = c.count("/why-choose-us.html")
# Now also add /why-choose-us.html as the path arg to the why-choose-us page() call
# Find the why-choose-us.html page call and ensure it has the path
print(f"Occurrences before: {before}, after: {after}")
with open("scripts/build-pages.py","w",encoding="utf-8") as f:
    f.write(c)
print("Saved")
