import json
import base64
import pathlib
import tempfile

COMPRESSED_PIC = pathlib.Path(r"C:\Users\Public\Documents\ESTsoft\CreatorTemp\soolbamghn9l_8a6t")
imgs = sorted(COMPRESSED_PIC.glob("*.jpg"))
batches = [imgs[i : i + 4] for i in range(0, len(imgs), 4)]
out = pathlib.Path(tempfile.gettempdir()) / "soolbam_push_batches"
out.mkdir(exist_ok=True)
for bi, batch in enumerate(batches):
    files = []
    for p in batch:
        files.append(
            {
                "path": f"pic/{p.name}",
                "content": base64.standard_b64encode(p.read_bytes()).decode(),
            }
        )
    (out / f"batch{bi}.json").write_text(json.dumps(files), encoding="utf-8")
    print("batch", bi, [f["path"] for f in files], "total_b64_chars", sum(len(f["content"]) for f in files))
print("dir", out)
