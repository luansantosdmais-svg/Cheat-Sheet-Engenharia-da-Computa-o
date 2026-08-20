# -*- coding: utf-8 -*-
"""Build: gera e executa os notebooks .ipynb do repositorio.

Uso:
  python build_repo.py [caminho_do_repositorio] [cards.json]

Saidas (dentro do repositorio):
  notebooks/<categoria>/<Materia>.ipynb  -> executados, com saidas embutidas
  outputs/<Materia>.pdf                  -> cheat sheets gerados
  src/<Materia>.py                       -> geradores adaptados (cross-platform)
"""
import json
import re
import shutil
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import nbformat as nbf
from nbclient import NotebookClient

sys.path.insert(0, str(Path(__file__).parent))
from subjects_part1 import SUBJECTS_1
from subjects_part2a import SUBJECTS_2A
from subjects_part2b import SUBJECTS_2B
from subjects_part2c import SUBJECTS_2C
from subjects_part3 import SUBJECTS_3

SUBJECTS = SUBJECTS_1 + SUBJECTS_2A + SUBJECTS_2B + SUBJECTS_2C + SUBJECTS_3

# ---------------------------------------------------------------------------
# localiza a raiz do repositorio
# ---------------------------------------------------------------------------
ROOT = None
if len(sys.argv) > 1:
    p = Path(sys.argv[1])
    if p.exists() and p.is_dir():
        ROOT = p
if ROOT is None:
    desc = Path.home() / "Desktop"
    cands = [x for x in desc.rglob("Cheat Sheet*") if x.is_dir()]
    if cands:
        ROOT = cands[0]
if ROOT is None:
    print("Pasta do repositorio nao encontrada"); sys.exit(1)
ROOT = ROOT.resolve()
print("ROOT =", ROOT)

NB_DIR = ROOT / "notebooks"
OUT_DIR = ROOT / "outputs"
SRC_DIR = ROOT / "src"
for d in (NB_DIR, OUT_DIR, SRC_DIR):
    d.mkdir(exist_ok=True)

cards_path = Path(sys.argv[2]) if len(sys.argv) > 2 and Path(sys.argv[2]).exists() else \
    Path(__file__).parent / "cards.json"
CARDS = json.loads(cards_path.read_text(encoding="utf-8"))

# ---------------------------------------------------------------------------
# helper: fonte DejaVu cross-platform (usa a embarcada no matplotlib)
# ---------------------------------------------------------------------------
HELPER = '''from pathlib import Path
import matplotlib as _mpl

def _dejavu_dir():
    _base = Path(_mpl.__file__).parent / "mpl-data" / "fonts" / "ttf"
    if (_base / "DejaVuSans.ttf").exists():
        return str(_base)
    for _p in [Path("/usr/share/fonts/truetype/dejavu"),
               Path("/System/Library/Fonts"),
               Path("/Library/Fonts"),
               Path("C:/Windows/Fonts")]:
        if (_p / "DejaVuSans.ttf").exists():
            return str(_p)
    raise RuntimeError("Fonte DejaVuSans nao encontrada; instale matplotlib ou a fonte DejaVu.")
'''


def transform_source(source: str, out_name: str) -> str:
    s = re.sub(r"OUT\s*=\s*Path\('[^']+'\)", "OUT = Path('" + out_name + "')", source, count=1)
    s = re.sub(
        r"FONT_DIR\s*=\s*Path\('/usr/share/fonts/truetype/dejavu'\)",
        "FONT_DIR = Path(_dejavu_dir())",
        s,
        count=1,
    )
    s = s.replace("DejaVuSansCondensed.ttf", "DejaVuSans.ttf")
    s = s.replace("DejaVuSansCondensed-Bold.ttf", "DejaVuSans-Bold.ttf")
    s = s.replace("DejaVuSansCondensed-Oblique.ttf", "DejaVuSans-Oblique.ttf")
    return s


def clean_html(text: str) -> str:
    t = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
         .replace("&nbsp;", " ").replace("&apos;", "'"))
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<super>(.*?)</super>", r"^\1", t)
    t = re.sub(r"<sub>(.*?)</sub>", r"_\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.strip()


def markdown_card(card) -> str:
    title = clean_html(card["title"])
    idea = clean_html(card["idea"])
    lines = [f"### 🟢 {title}", "", f"**Ideia:** {idea}", ""]
    for f in card.get("formulas", []):
        lines.append(f"- {clean_html(f)}")
    lines.append("")
    lines.append(f"> 💡 **Dica:** {clean_html(card['tip'])}")
    lines.append("")
    return "\n".join(lines)


def build_notebook(subj: dict) -> nbf.NotebookNode:
    stem = subj["stem"]
    name = subj["name"]
    cat = subj["cat"]
    emoji = subj["emoji"]
    tagline = subj["tagline"]
    about = subj["about"]
    pdf_name = stem + ".pdf"
    src_name = subj.get("src", stem)

    original = (SRC_DIR / (src_name + ".py")).read_text(encoding="utf-8")
    transformed = transform_source(original, pdf_name)

    cards = CARDS.get(subj.get("cards_key", stem), [])
    conteudo_md = "\n".join(markdown_card(c) for c in cards) if isinstance(cards, list) else "_sem cards_"

    cells = []

    # 1) titulo
    cells.append(nbf.v4.new_markdown_cell(
        f"# {emoji} {name}\n\n"
        f"`{cat}` · **Engenharia da Computação** · `Python 3`\n\n"
        f"> **{tagline}**\n\n"
        f"{about}\n"
    ))

    # 2) conteudo teorico (cards)
    cells.append(nbf.v4.new_markdown_cell(
        "## 📚 Conteúdo da matéria\n\n"
        "Resumo teórico organizado em cards (o mesmo que é renderizado no PDF gerado abaixo).\n\n"
        + conteudo_md
    ))

    # 3) codigo: gerador
    cells.append(nbf.v4.new_markdown_cell(
        "## ⚙️ Gerador do Cheat Sheet (PDF)\n\n"
        "O script original gera um **PDF estilo OneNote** com `reportlab`. "
        "Para rodar em qualquer sistema operacional, as fontes são resolvidas automaticamente "
        "(usa a **DejaVu embarcada no matplotlib** com fallback para os caminhos clássicos "
        "de Windows/Linux/macOS) e o arquivo de saída é gerado na pasta atual.\n"
    ))
    cells.append(nbf.v4.new_code_cell(HELPER + "\n\n# ===== código original adaptado =====\n" + transformed))

    # 4) exibicao do PDF gerado
    cells.append(nbf.v4.new_markdown_cell(
        "## 🖼️ Resultado visual\n\n"
        "As páginas do PDF gerado são renderizadas abaixo (código de pré-visualização). "
        "Este é o **cheat sheet** da matéria.\n"
    ))
    cells.append(nbf.v4.new_code_cell(
        "import pymupdf as fitz\n"
        "from IPython.display import display, Image\n\n"
        f"doc = fitz.open(Path('{pdf_name}'))\n"
        "print(f'Páginas: {len(doc)}')\n"
        "for i, page in enumerate(doc, 1):\n"
        "    pix = page.get_pixmap(dpi=130)\n"
        "    display(Image(data=pix.tobytes('png')))\n"
    ))

    # 5) exemplos praticos
    cells.append(nbf.v4.new_markdown_cell(
        "## 🎯 Exemplos práticos\n\n"
        "Código executável que demonstra os conceitos da matéria com **saídas reais** "
        "(cálculos, simulações e gráficos).\n"
    ))
    cells.append(nbf.v4.new_code_cell(subj["examples"]))

    # 6) como executar
    cells.append(nbf.v4.new_markdown_cell(
        "## 🚀 Como executar\n\n"
        "1. Instale as dependências: `pip install -r requirements.txt`\n"
        "2. Abra este notebook no Jupyter (`jupyter notebook`) ou VS Code.\n"
        "3. Execute as células em ordem (`Run All`).\n\n"
        "> 💡 O notebook foi **pré-executado**: as saídas já estão embutidas, mas você pode "
        "rodar novamente para reproduzir.\n"
    ))

    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python", "version": "3"}
    nb.cells = cells
    return nb


def execute_notebook(nb, cwd: Path, timeout: int = 240) -> None:
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3",
                            resources={"metadata": {"path": str(cwd)}})
    client.execute()


def main():
    only = sys.argv[3] if len(sys.argv) > 3 else None
    t0 = time.time()
    ok, falhas = [], []
    for subj in SUBJECTS:
        stem = subj["stem"]
        if only and stem not in only:
            continue
        folder = NB_DIR / subj["folder"]
        folder.mkdir(exist_ok=True)
        pdf_name = stem + ".pdf"
        src_name = subj.get("src", stem)
        print(f"\n>>> [{stem}]")
        try:
            nb = build_notebook(subj)
            # executa na pasta da categoria (o PDF e gerado ali)
            execute_notebook(nb, cwd=folder)
            nb_path = folder / (stem + ".ipynb")
            nbf.write(nb, nb_path, version=4)
            # copia o PDF gerado para outputs/
            gen = folder / pdf_name
            if gen.exists():
                shutil.copy(gen, OUT_DIR / pdf_name)
                print(f"    PDF -> outputs/{pdf_name}")
            else:
                print(f"    AVISO: PDF nao encontrado em {gen}")
            # gerador adaptado em src/
            ok.append(stem)
            print(f"    OK -> notebooks/{subj['folder']}/{stem}.ipynb")
        except Exception as e:
            falhas.append((stem, str(e)))
            print(f"    FALHA: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print(f"Concluidos: {len(ok)}/{len([s for s in SUBJECTS if not only or s['stem'] in only])}")
    if falhas:
        print("Falhas:")
        for s, e in falhas:
            print(f"  - {s}: {e}")
    print(f"Tempo total: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()