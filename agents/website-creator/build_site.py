from pathlib import Path
import json
ROOT=Path(__file__).parent
template=(ROOT/'studio.template.html').read_text(encoding='utf-8')
catalog=(ROOT/'catalog.json').read_text(encoding='utf-8').replace('</','<\\/')
library=(ROOT/'vendor/pptxgen.bundle.js').read_text(encoding='utf-8').replace('</script','<\\/script')
app=(ROOT/'app.js').read_text(encoding='utf-8')
out=template.replace('__CATALOG__',catalog).replace('__PPTX_LIB__',library).replace('__APP_JS__',app)
(ROOT/'index.html').write_text(out,encoding='utf-8')
print(f'Built self-contained index.html: {len(out.encode("utf-8")):,} bytes')
