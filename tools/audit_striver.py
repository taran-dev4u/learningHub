import re

def main():
    with open('DSA_Ultimate_Index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Count total Striver problems (data-striver="1")
    striver_problems = re.findall(r'<li[^>]*data-striver="1"[^>]*>', html)
    print(f'Total Striver problems found: {len(striver_problems)}')

    # 2. Check for duplicate problems (by data-lc)
    lc_counts = {}
    for m in re.finditer(r'<li[^>]*data-lc="([^"]+)"', html):
        lc = m.group(1)
        lc_counts[lc] = lc_counts.get(lc, 0) + 1
        
    duplicates = {lc: count for lc, count in lc_counts.items() if count > 1}
    if duplicates:
        print(f"Warning: Found {len(duplicates)} duplicate problems.")
        for lc, c in list(duplicates.items())[:5]:
            print(f"LC {lc} appears {c} times.")
    else:
        print("No duplicate problems found.")

    # 3. Check button presence
    if 'data-val="striver"' in html:
        print("Striver filter button is present.")
    else:
        print("Error: Striver filter button missing.")

    # 4. Check CSS
    if '--striver:' in html:
        print("Striver CSS is present.")
    else:
        print("Error: Striver CSS missing.")

    # 5. Check filter logic
    if 'filters.list.has(\'striver\')' in html:
        print("Filter logic for Striver is present.")
    else:
        print("Error: Filter logic missing.")

if __name__ == "__main__":
    main()
