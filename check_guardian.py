import traceback

print("=== Guardian Check ===")

try:
    from guardian import *
    print("✓ guardian package imported")
except Exception:
    print("✗ guardian package import failed")
    traceback.print_exc()

try:
    from guardian.controller import GuardianController
    print("✓ GuardianController imported")
except Exception:
    print("✗ GuardianController import failed")
    traceback.print_exc()

print("=== Guardian Check Complete ===")
