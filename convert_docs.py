import os
import glob
import markdown
from markitdown import MarkItDown

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}assets/learning-hub-shared.css">
<script src="{root}assets/learning-hub-shared.js"></script>
<style>
:root {{
  --bg: #f4f6f8;
  --surface: #ffffff;
  --text: #151922;
  --muted: #586173;
  --border: #dce3ec;
  --accent: #2459d6;
  --shadow: 0 14px 36px rgba(31, 42, 63, .1);
}}
html.dark {{
  --bg: #101319;
  --surface: #181d27;
  --text: #edf1f7;
  --muted: #a2acbc;
  --border: #303849;
  --accent: #7ca2ff;
}}
body {{
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, sans-serif;
  padding: 40px 20px;
  line-height: 1.6;
}}
.wrap {{
  max-width: 1000px;
  margin: 0 auto;
  background: var(--surface);
  padding: 40px;
  border-radius: 12px;
  box-shadow: var(--shadow);
}}
.header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}}
.btn-back {{
  padding: 10px 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: var(--text);
  font-weight: bold;
}}
h1, h2, h3, h4, h5, h6 {{ margin-top: 1.5em; }}
pre {{
  background: #1e1e1e;
  color: #fff;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}}
code {{ font-family: monospace; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}}
th, td {{
  border: 1px solid var(--border);
  padding: 10px;
  text-align: left;
}}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <a href="{root}library.html" class="btn-back">Back to Library</a>
  </div>
  <div class="content">
    {content}
  </div>
</div>
</body>
</html>"""

def convert_pdfs():
    md = MarkItDown()
    resources_dir = os.path.join(os.path.dirname(__file__), 'Resources')
    output_dir = os.path.join(os.path.dirname(__file__), 'ConvertedDocs')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = glob.glob(os.path.join(resources_dir, '**', '*.pdf'), recursive=True)
    
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        try:
            result = md.convert(pdf_path)
            md_text = result.text_content
            
            # Convert MD to HTML
            html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
            
            # Form final HTML
            rel_path = os.path.relpath(pdf_path, resources_dir)
            title = os.path.basename(pdf_path).replace('.pdf', '')
            depth = len(os.path.relpath(out_file, output_dir).replace("\\", "/").split("/")) - 1
            root = "../" * (depth + 1)
            final_html = HTML_TEMPLATE.format(title=title, content=html_content, root=root)
            
            out_file = os.path.join(output_dir, rel_path.replace('.pdf', '.html'))
            
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(final_html)
                
            print(f"Successfully converted to {out_file}")
        except Exception as e:
            print(f"Failed to convert {pdf_path}: {e}")

if __name__ == "__main__":
    convert_pdfs()
