"""로컬에서 GitHub MCP push_files용 JSON 한 줄 페이로드 생성 (실행 후 수동 호출 또는 파이프)."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def main() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    md = (ROOT / "웹사이트기획안.markdown").read_text(encoding="utf-8")
    workflow = """# GitHub Pages: 정적 파일을 Actions로 배포
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""

    payload = {
        "owner": "soolbam5498",
        "repo": "soolbam-landing",
        "branch": "main",
        "message": "Add Sulbam landing page, workflow, and planning doc",
        "files": [
            {"path": "index.html", "content": html},
            {"path": "웹사이트기획안.markdown", "content": md},
            {"path": ".nojekyll", "content": ""},
            {"path": ".github/workflows/deploy-pages.yml", "content": workflow},
        ],
    }

    out = ROOT / "_github_push_main.json"
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(out)
    print("bytes", out.stat().st_size)


if __name__ == "__main__":
    main()
    sys.exit(0)
