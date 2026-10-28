"""Refresh the manually matched Dinesh Varyani catalogue using YouTube oEmbed.

No media is downloaded. A failed title/channel check prevents any output write.
The problem mappings are deliberately explicit; similar titles are not enough
to make a different problem variant an exact solution.
"""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'tools/dinesh_varyani_videos.json'
PLAYLIST = 'https://www.youtube.com/playlist?list=PL6Zs6LgrJj3tDXv8a_elC6eT_4R5gfX4d'
CHANNEL = 'https://www.youtube.com/@itsdineshvaryani'

# Exact problem walkthroughs. Parts with "Two Sum II" in their titles are
# parts of LeetCode #1, not LeetCode #167; their published titles are preserved.
EXACT = {
    'two-sum': ['_0sLV_H9gIY', 'mS8SgO_Ux4s', 'j5j6_45nxP0'],
    'add-two-numbers': ['qE9KOe3Fu7Q'],
    'longest-substring-without-repeating-characters': ['zKrEIlwbF5A'],
    '3sum': ['bZrgAfkrs9M'],
    'valid-parentheses': ['9TVrlVAtpv8'],
    'merge-two-sorted-lists': ['IMWiPqoneT4', 'IdBENG4jRWY'],
    'remove-duplicates-from-sorted-array': ['ss0j3BuPNTk'],
    'remove-element': ['yAt_P1x6LuU'],
    'search-insert-position': ['O282KYvGkyc'],
    'maximum-subarray': ['y3zb6paCCy8', 'ZD12jyrrUGI', 'f35VqXSsP6Y'],
    'spiral-matrix': ['dm25MsWHYuk'],
    'merge-intervals': ['uO1Pe5MCGAc'],
    'insert-interval': ['nALxbxZnzks'],
    'sort-colors': ['19p9d9PCDkA', 'srRqxjRA9dQ'],
    'remove-duplicates-from-sorted-list': ['0Hn18rUkZKY'],
    'binary-tree-inorder-traversal': ['vpXcceCmSbg', 'uMTrIjP_0Gw'],
    'validate-binary-search-tree': ['ACoLBU0nPAw'],
    'symmetric-tree': ['lStz4y5Cq4c'],
    'binary-tree-level-order-traversal': ['hXAqTO7VqUQ'],
    'linked-list-cycle': ['rOpnLs0lXy0', '5czD98BU28o'],
    'linked-list-cycle-ii': ['yKNOZ8bPdRQ', 'e4JbuvkhrpI'],
    'binary-tree-preorder-traversal': ['R4V4n-waxn4', 'VaIaJMeNWtU'],
    'binary-tree-postorder-traversal': ['xDMFBKjxZNc', 'uigaktgcQWU', 'm4Wb3kXk_iA'],
    'number-of-islands': ['iz0T9z3V84g'],
    'reverse-linked-list': ['jY-EUKXYT20'],
    'product-of-array-except-self': ['w-qeVOijccg'],
    'sliding-window-maximum': ['HihXfX24GO4'],
    'search-a-2d-matrix-ii': ['4lATqBxapmc', 'og-ab_WgWBc'],
    'move-zeroes': ['wvz5Jz_PW_8', 'FjU-6e881Uk'],
    'fibonacci-number': ['8Upn_Z_VjQw', 'I6AJxmyQ9dA', '-WgPTuBYSCE', 'gX36VvycDnY'],
    'search-in-a-binary-search-tree': ['n1fnwWfgcvY', 'wL1oxXrEgr4'],
    'insert-into-a-binary-search-tree': ['B2g1shI0pbk', 'ZHLAiHiYgeI'],
    'binary-search': ['KPQTOH_adT0'],
    'squares-of-a-sorted-array': ['npKnie2kjiM', 'vr0jRG5wuMQ'],
}

# Related explanations with a different interface/constraint are labelled as
# topic support in the panel, never as an exact LeetCode solution.
SUPPORT = {
    'reverse-integer': ('Integer reversal technique', ['aInhXAUOJoY']),
    'remove-nth-node-from-end-of-list': ('Finding the nth node from the end', ['adS-s2Stg_A']),
    'merge-sorted-array': ('Merging sorted arrays; separate output array', ['QK6I45kC2VQ', 'tSrUFzSn-P0', '7ynKGC1_cVk']),
    'valid-palindrome': ('Basic palindrome check; review problem-specific normalization', ['Q485CWk_QWk', 'HLui6CzK-bI']),
    'missing-number': ('Missing-number technique; review the input range', ['PaQA-9mHMRY', 'Zh8RcXFOKVo']),
    'is-subsequence': ('Subsequence technique using arrays', ['bgWX-auJpI0', '9eAMIKZ3edI']),
    'next-greater-element-i': ('Next-greater-element stack technique', ['JUDNrDg-LhQ']),
    'middle-of-the-linked-list': ('Middle-node technique; check the even-length convention', ['DYpEpZzNmiA']),
    'implement-trie-prefix-tree': ('Trie representation and insertion', ['TnKfIlImSKI', 'c1lX6ntrj64', 'I6i4AyDsMQA', 'oFf4oTE7GgY', 'ucJfhsLCBw0']),
}

TOPICS = {
    's2869': ('Array fundamentals', ['CysMrYVgyGU', 'lTyEeOhB0Fs']),
    's342': ('Reversing an array', ['PkrEpxfhSao', 'YrTJFPa9CpM']),
    's1203': ('Hashing and hash tables', ['44A_jk4_Rx8', 'dj7MYmhrebE', 'hEPciOcibZs']),
    's947': ('Selection sort', ['u8moN7j6P8w', 'ezwtvaqiZH8', 'vQ5S6rESu8w']),
    's943': ('Bubble sort', ['eFreSZFj1bI', 'pYyl9QAtRdk', 'fF1aJL-4Yzk']),
    's944': ('Insertion sort', ['W3TklBfIK9U', 'TKIAVBsCLqk', 'GDNUL4lv8Nc']),
    's945': ('Merge sort', ['MZM63AvAs7s']),
    's946': ('Quick sort', ['Ic4K6pz0rRo']),
    's43': ('Second maximum in an array', ['UULE-HyfERc']),
    's41': ('Linear search', ['xSbScg7ONw8', 'aWFrL3qBRF4']),
    's44': ('Missing number in an array', ['PaQA-9mHMRY', 'Zh8RcXFOKVo']),
    's1237': ('Singly linked list fundamentals', ['WI1qQavJIRo', 'k9r80o_DeK4', 'Fg4VIjTdHx4', 'ZovnBKd6O7g']),
    's356': ('Insert at the head of a linked list', ['Xxk_j0fBXws', 'LRUdf9VpO0w']),
    's470': ('Linked list length', ['q99_b1z715M', 'MGs4rxFQmfE']),
    's905': ('Searching a linked list', ['feLNtgVg1xI']),
    's1234': ('Doubly linked lists', ['YgfaeRol4e0']),
    's361': ('Insert at the head of a doubly linked list', ['jircscEJnWI']),
    's348': ('Delete the head of a doubly linked list', ['WtoyZk6fgJ0']),
    's390': ('Stack using an array', ['XcJ16QUeJr0']),
    's391': ('Stack using a linked list', ['Us4N22SEbM0']),
    's388': ('Queue implementation', ['sn8BPJGRA8U']),
    's1223': ('Priority queues and binary heaps', ['dOynDPicyiI']),
    's2865': ('Binary tree fundamentals', ['mQk6Y5B_0Mk', 'wL7JOLxbMI4']),
    's2864': ('Binary tree representation in Java', ['mQk6Y5B_0Mk', 'wL7JOLxbMI4']),
    's1153': ('Binary search tree fundamentals', ['B1Mau6NCHx0', '_JcH9H9TVcY']),
    's1222': ('Graph fundamentals', ['T2HMp69s8jw']),
    's2871': ('Graph representation in Java', ['9qFLiiNPDEI', 'zqXDwFhfPtI', 'X1LdtRW88c0', 'Kd__dmFHoZo', 'nt8uN6pQrnw', '6rDKLqFLfh0']),
    's528': ('Connected components', ['NWl-LtrWU-o']),
    's529': ('Graph traversal', ['-X6ji6sjxD4', 'grewOnmAd0k', 'WxM-EENBY-w', 'Wzk6BBEBlYE', 'MmIeokeCdjY']),
    's2831': ('Depth-first search', ['WxM-EENBY-w', 'Wzk6BBEBlYE', 'MmIeokeCdjY']),
    's1195': ('Dynamic programming foundations', ['qWFKDj41eVw', 'MWV5I3W-0JU', 'm8ERwzH7JOI', 'dxNTArjcas8', 'jT3dwqvPA8g']),
    's1027': ('Trie representation and insertion', ['TnKfIlImSKI', 'c1lX6ntrj64', 'I6i4AyDsMQA', 'oFf4oTE7GgY', 'ucJfhsLCBw0']),
}


def main():
    matches = [{'slug': slug, 'kind': 'exact', 'videoIds': ids} for slug, ids in EXACT.items()]
    matches += [{'slug': slug, 'kind': 'topic', 'focus': focus, 'videoIds': ids} for slug, (focus, ids) in SUPPORT.items()]
    matches += [{'rowId': row, 'kind': 'topic', 'focus': focus, 'videoIds': ids} for row, (focus, ids) in TOPICS.items()]
    video_ids = sorted({v for match in matches for v in match['videoIds']})
    summary = json.loads((ROOT / 'tools/problems_summary.json').read_text(encoding='utf-8'))
    for match in matches:
        assert any(p.get('slug') == match.get('slug') if 'slug' in match else p['lcId'] == match['rowId'] for p in summary), match

    durations = {}
    cache = ROOT / 'tools/.dsa-cache/dinesh-playlist.tmp.json'
    if cache.exists():
        raw = cache.read_bytes()
        encoding = 'utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig'
        playlist = json.loads(raw.decode(encoding))
        assert playlist['channel_id'] == 'UCd0L83mMeQ4Ioy4IjaSYhvA'
        durations = {v['id']: v.get('duration') for v in playlist['entries']}
        assert all(v in durations for v in video_ids), 'Video not in the official playlist'
    elif OUTPUT.exists():
        durations = {k: v.get('durationSeconds') for k, v in json.loads(OUTPUT.read_text(encoding='utf-8'))['videos'].items()}

    checked = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    def verify(video_id):
        url = 'https://www.youtube.com/oembed?' + urllib.parse.urlencode({'url': 'https://www.youtube.com/watch?v=' + video_id, 'format': 'json'})
        with urllib.request.urlopen(url, timeout=25) as response:
            data = json.load(response)
        if data.get('author_name') != 'Dinesh Varyani' or data.get('author_url', '').rstrip('/') != CHANNEL:
            raise ValueError(f'{video_id}: unexpected author {data.get("author_name")} {data.get("author_url")}')
        return video_id, {'title': data['title'], 'author': data['author_name'], 'authorUrl': data['author_url'], 'durationSeconds': durations.get(video_id), 'verifiedAt': checked, 'verificationUrl': url}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        videos = dict(pool.map(verify, video_ids))
    # Published LeetCode numbers must agree even where titles say "Part II".
    for match in matches:
        if match['kind'] != 'exact':
            continue
        numbers = {int(p['lcNum']) for p in summary if p.get('slug') == match['slug'] and p.get('lcNum')}
        for video_id in match['videoIds']:
            stated = re.findall(r'LeetCode\s*#?\s*(\d+)', videos[video_id]['title'], re.I)
            assert not stated or all(int(n) in numbers for n in stated), (match, videos[video_id]['title'])
    output = {'source': {'playlistUrl': PLAYLIST, 'repositoryUrl': 'https://github.com/dinesh-varyani/ds-algos', 'channelUrl': CHANNEL, 'channelId': 'UCd0L83mMeQ4Ioy4IjaSYhvA'}, 'videos': videos, 'matches': matches}
    fd, temp = tempfile.mkstemp(prefix='.dinesh-videos-', suffix='.tmp', dir=OUTPUT.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            json.dump(output, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        for attempt in range(5):
            try:
                os.replace(temp, OUTPUT)
                break
            except OSError:
                if attempt == 4:
                    raise
                time.sleep(.2 * (attempt + 1))
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    print(f'Verified {len(videos)} Dinesh Varyani videos across {len(matches)} explicit matches.')


if __name__ == '__main__':
    main()
