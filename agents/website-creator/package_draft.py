from pathlib import Path
import csv, hashlib, json, shutil, zipfile

root=Path(__file__).parent
shared=Path(r'C:\Users\colt3\OpenBot\Shared\Meghan-Design-Studio-Draft-2026-11-05')
shared.mkdir(parents=True,exist_ok=True)
catalog=json.loads((root/'catalog.json').read_text(encoding='utf-8'))
manifest=[]
for board in catalog.get('boards', []):
    path=root/'sources'/f"{board['id']}.pdf"
    if path.exists():
        manifest.append({'title':board['title'],'originalFilename':board['filename'],'file':f"sources/{board['id']}.pdf",'driveUrl':board['url'],'pages':board['pages'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(root/'source-manifest.json').write_text(json.dumps({'sources':manifest},indent=2),encoding='utf-8')
