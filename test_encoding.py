with open('context/ACTIVE_THOUGHTS.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("First few characters:")
for c in text[:20]:
    print(repr(c), hex(ord(c)))
