import os
import sys
import importlib

errors = []

# Add project root
sys.path.insert(0, os.path.abspath("."))

# Skip these folders
SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv"
}

print("=" * 60)
print("MARKETVERSE IMPORT CHECK")
print("=" * 60)

for root, dirs, files in os.walk("."):

    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

    for file in files:

        if not file.endswith(".py"):
            continue

        if file.startswith("__"):
            continue

        path = os.path.join(root, file)

        module = (
            path[:-3]
            .replace(os.sep, ".")
            .replace("./", "")
            .lstrip(".")
        )

        try:
            importlib.import_module(module)
            print(f"✓ {module}")

        except Exception as e:
            print(f"✗ {module}")
            print(f"   {e}")
            errors.append((module, str(e)))

print("\n" + "=" * 60)

if errors:
    print("IMPORT ERRORS FOUND\n")

    for module, err in errors:
        print(f"- {module}")
        print(f"  {err}\n")

    raise SystemExit(1)

print("ALL MODULES IMPORTED SUCCESSFULLY.")
