import sys
import yaml
import ast
from pathlib import Path
from fnmatch import fnmatch

RULES = yaml.safe_load(
    Path("tools/architecture_guard/import_rules.yml").read_text()
)["rules"]

errors = []

def matches_any(path, patterns):
    return any(fnmatch(path, p) for p in patterns)

def get_imports(py_file: Path):
    try:
        tree = ast.parse(py_file.read_text())
    except SyntaxError:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports

for rule in RULES:
    for file in Path(".").rglob("*"):
        if not file.is_file():
            continue

        if not matches_any(str(file), rule["paths"]):
            continue

        if file.suffix != ".py" and not file.suffix in [".ts", ".tsx"]:
            continue

        if file.suffix == ".py":
            imports = get_imports(file)
        else:
            imports = file.read_text().splitlines()

        for forbidden in rule["forbidden_imports"]:
            for imp in imports:
                if forbidden in imp:
                    errors.append(
                        f"[{rule['name']}] {file} imports forbidden '{forbidden}'"
                    )

if errors:
    print("❌ Architecture Import Violations:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("✅ Architecture import rules passed")
