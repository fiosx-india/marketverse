import os
import py_compile

errors = []

for root, dirs, files in os.walk("."):
    # Skip unnecessary folders
    dirs[:] = [
        d for d in dirs
        if d not in ("venv", ".venv", "__pycache__", ".git")
    ]

    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)

            try:
                py_compile.compile(path, doraise=True)
                print(f"✓ {path}")

            except Exception as e:
                print(f"✗ {path}")
                print(e)
                errors.append(path)

print("\n==============================")

if errors:
    print("FAILED FILES:")
    for f in errors:
        print("-", f)
else:
    print("ALL PYTHON FILES ARE SYNTAX CLEAN.")
