# tools/docs_guard/check_api_docs_vs_routes.py
import sys
import yaml
from pathlib import Path

mapping = yaml.safe_load(
    Path("tools/mappings/api_to_code.yml").read_text()
)

errors = []

for service, apis in mapping.items():
    for name, spec in apis.items():
        if not Path(spec["doc"]).exists():
            errors.append(f"[API] Missing doc: {spec['doc']}")

        for route in spec["routes"]:
            if not Path(route).exists():
                errors.append(f"[API] Missing route: {route}")

        for test in spec["tests"]:
            if not Path(test).exists():
                errors.append(f"[API] Missing test: {test}")

if errors:
    print("❌ API contract violations:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("✅ API ↔ Code checks passed")
