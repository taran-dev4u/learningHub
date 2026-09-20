import json
import re

def normalize_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def main():
    with open('striver_parsed.json', 'r', encoding='utf-8') as f:
        striver_data = json.load(f)
        
    with open('DSA_Ultimate_Index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    existing_problems = {}
    for m in re.finditer(r'<li [^>]*data-lc="([^"]+)"[^>]*data-name="([^"]+)"[^>]*>', html):
        lc = m.group(1)
        name = m.group(2)
        norm_name = normalize_name(name)
        existing_problems[norm_name] = lc

    new_striver_html = []
    striver_pattern_count = 100 
    
    for category in striver_data:
        cat_name = category['category_name']
        pattern_id = f"striver_{striver_pattern_count}"
        striver_pattern_count += 1
        
        cat_html = []
        cat_html.append(f'<div class="pattern" id="pattern-{pattern_id}" data-pattern-lcs="">')
        cat_html.append(f'  <div class="head">')
        cat_html.append(f'    <h2>Striver: {cat_name}</h2>')
        cat_html.append(f'    <div class="progress-bar-container"><div class="progress-bar" data-pp-fill="{pattern_id}"></div></div>')
        cat_html.append(f'    <span class="count" data-pp-count="{pattern_id}">0/0</span>')
        cat_html.append(f'  </div>')
        
        cat_lcs = []
        
        for subcat in category['subcategories']:
            subcat_name = subcat['subcategory_name']
            cat_html.append(f'  <h3 style="margin: 10px 0 5px 20px; color: var(--accent); font-size: 14px;">{subcat_name}</h3>')
            cat_html.append(f'  <ol class="problems">')
            
            for prob in subcat['problems']:
                prob_name = prob['problem_name']
                norm_name = normalize_name(prob_name)
                diff = prob['difficulty'].upper()[0] if prob.get('difficulty') else 'M'
                if diff not in ['E', 'M', 'H']: diff = 'M'
                
                if norm_name in existing_problems:
                    pass
                else:
                    lc = "s" + prob['problem_id']
                    cat_html.append(f'    <li data-diff="{diff}" data-lc="{lc}" data-striver="1" data-name="{prob_name}" data-companies="">')
                    cat_html.append(f'      <div class="solve-check" data-lc="{lc}" title="Mark as solved"></div>')
                    cat_html.append(f'      <div class="bookmark-star" data-lc="{lc}" title="Bookmark to revisit">☆</div>')
                    
                    link = prob.get('leetcode')
                    article = prob.get('article')
                    yt = prob.get('youtube')
                    
                    if link and link != "$undefined":
                        cat_html.append(f'      <a href="{link}" target="_blank" class="problem-name">{prob_name}</a>')
                    else:
                        cat_html.append(f'      <a href="{article if article != "$undefined" else "#"}" target="_blank" class="problem-name">{prob_name}</a>')
                    
                    cat_html.append(f'      <div class="badges">')
                    if yt and yt != "$undefined":
                        cat_html.append(f'        <a href="{yt}" target="_blank" class="badge badge-yt" title="Video Solution">YT</a>')
                    if article and article != "$undefined":
                        cat_html.append(f'        <a href="{article}" target="_blank" class="badge badge-article" title="Article">Article</a>')
                    cat_html.append(f'      </div>')
                    cat_html.append(f'      <div class="note-btn" data-lc="{lc}" title="Add a note for this problem">📝</div>')
                    cat_html.append(f'    </li>')
                    cat_lcs.append(lc)
                    
            cat_html.append(f'  </ol>')
        
        cat_html[0] = f'<div class="pattern" id="pattern-{pattern_id}" data-pattern-lcs="{",".join(cat_lcs)}">'
        cat_html.append(f'</div>')
        new_striver_html.append("\n".join(cat_html))
        
    striver_html_block = "\n".join(new_striver_html)
    
    if 'Striver: Learn the basics' not in html:
        # Instead of </main>, insert before <script> tag
        idx = html.find('<script>')
        if idx != -1:
            html = html[:idx] + striver_html_block + '\n' + html[idx:]
        else:
            print("Failed to find <script> tag.")

    with open('DSA_Ultimate_Index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Successfully appended Striver HTML blocks")

if __name__ == "__main__":
    main()
