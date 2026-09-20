import re
import json

def main():
    content_file = r"C:\Users\mamid\.gemini\antigravity\brain\6710f161-0039-41fa-ba5c-6c6a87c812ac\.system_generated\steps\26\content.md"
    
    with open(content_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Find all chunks: self.__next_f.push([1,"..."])
    # The string inside is a JSON string literal.
    pattern = r'self\.__next_f\.push\(\[1,(".*?(?<!\\)")\]\)'
    matches = re.findall(pattern, html_content)
    
    full_str = ""
    for m in matches:
        try:
            # m is a valid JSON string literal like '"foo\\nbar"'
            decoded = json.loads(m)
            full_str += decoded
        except Exception as e:
            # If it fails, just skip or handle
            pass

    # Now full_str contains the un-chunked data.
    # It still contains things like \"sections\":[{...
    # So we need to find \"sections\":[{"category_id"
    start_idx = full_str.find('"sections":[{')
    if start_idx == -1:
        start_idx = full_str.find('\\"sections\\":[{')
        if start_idx != -1:
            # It's double escaped. Let's unescape it fully.
            # actually we can just parse it as JSON if we find the outer JSON.
            pass
    
    # Let's just use regex to extract problems from full_str.
    # The structure is known.
    
    # We can just look for "category_name":"...", "subcategories":[...]
    # Wait, if we replace \\" with " we can parse it as JSON.
    clean_str = full_str.replace('\\"', '"').replace('\\\\', '\\')
    
    start_idx = clean_str.find('"sections":[{')
    if start_idx == -1:
        print("Failed to find 'sections' in cleaned string.")
        return
        
    start_idx += 11 # points to '['
    
    bracket_count = 0
    end_idx = -1
    for i in range(start_idx, len(clean_str)):
        if clean_str[i] == '[':
            bracket_count += 1
        elif clean_str[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end_idx = i + 1
                break
                
    if end_idx != -1:
        json_str = clean_str[start_idx:end_idx]
        try:
            sections = json.loads(json_str)
            with open("striver_parsed.json", "w", encoding="utf-8") as out:
                json.dump(sections, out, indent=2)
            print(f"Successfully extracted {len(sections)} sections.")
            return
        except Exception as e:
            print(f"Loads failed: {e}")
            with open("striver_raw.txt", "w", encoding="utf-8") as out:
                out.write(json_str)
    else:
        print("Failed to match brackets.")

if __name__ == "__main__":
    main()
