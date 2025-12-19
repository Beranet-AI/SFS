import sys
import yaml
from pathlib import Path

mapping = yaml.safe_load(
    Path("tools/mappings/sequence_to_tests.yml").read_text()
)

errors = []

for name, spec in mapping.items():
    doc = Path(spec["doc"])
    if not doc.exists():
        errors.append(f"[SEQ] Missing doc: {doc}")

    for test in spec["tests"]:
        if not Path(test).exists():
            errors.append(f"[SEQ] Missing test for {name}: {test}")

if errors:
    print("❌ Sequence ↔ Test violations:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("✅ Sequence ↔ Test checks passed")
