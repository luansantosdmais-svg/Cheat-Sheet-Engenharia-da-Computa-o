import ast
import json
import sys
from pathlib import Path

if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
    SRC_DIR = Path(sys.argv[1])
else:
    desc = Path.home() / "Desktop"
    cands = [p for p in desc.rglob("Cheat Sheet*") if p.is_dir()]
    if not cands:
        cands = [p for p in (desc / "UNIVERSITY").rglob("Cheat Sheet*") if p.is_dir()] if (desc / "UNIVERSITY").exists() else []
    SRC_DIR = cands[0] if cands else None
if SRC_DIR is None:
    print("Folder not found"); sys.exit(1)
SRC_DIR = SRC_DIR / "src" if (SRC_DIR / "src").is_dir() else SRC_DIR
print("SRC_DIR =", SRC_DIR)


def safe_eval(node):
    if isinstance(node, ast.Dict):
        return {safe_eval(k): safe_eval(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.List) or isinstance(node, ast.Tuple):
        return [safe_eval(x) for x in node.elts]
    if isinstance(node, ast.Str) or isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.left, ast.Str):
        return node.left.value + safe_eval(node.right)
    if isinstance(node, ast.Constant):
        return node.value
    raise ValueError(f"Unsupported node: {ast.dump(node)}")


out = {}
for src in sorted(SRC_DIR.glob("*.py")):
    text = src.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(text)
    cards = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "CARDS":
                    try:
                        cards = safe_eval(node.value)
                    except Exception as e:
                        cards = {"__error__": str(e)}
    if cards is None:
        cards = {"__error__": "CARDS not found"}
    out[src.stem] = cards

outpath = Path(sys.argv[2])
outpath.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Wrote {len(out)} subjects to {outpath}")
for stem, cards in out.items():
    if isinstance(cards, list):
        titles = [c.get("title", "?").replace("<br/>", " / ") for c in cards]
        print(stem, "->", len(cards), "cards:", titles)
    else:
        print(stem, "->", cards)