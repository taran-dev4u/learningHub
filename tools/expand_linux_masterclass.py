import os
import sys
import tempfile
import time
import re
import html as html_lib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(4):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 3: raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except OSError: pass

LINUX_SUBSECTIONS = [
    {
        "num": "4.1",
        "title": "Linux Filesystem Hierarchy, VFS & Storage Subsystems",
        "desc": "Filesystem standards, virtual filesystem abstractions, inode mechanics, partition mount tables, and Logical Volume Management (LVM).",
        "concepts": [
            ("4.1.1", "Linux Filesystem Hierarchy Standard (FHS): /etc, /var, /proc, /sys & /dev",
             "Virtual pseudo-filesystems (procfs kernel telemetry, sysfs device trees), devfs hardware node management, ephemeral /run vs persistent /var, and /opt vs /usr/local binary isolation.",
             "https://www.youtube.com/watch?v=42iQKuQodW4", "00:00", "freeCodeCamp.org", "https://man7.org/linux/man-pages/man7/hier.7.html"),
            ("4.1.2", "Inodes, Hard Links, Symbolic Links & Ext4/XFS File Storage",
             "Inode metadata allocation, file pointers, directory block structures, unlink refcounts, hard links across the same filesystem vs symlink dangling pointers.",
             "https://www.youtube.com/watch?v=tKTZf4nhfG8", "00:00", "Computerphile", "https://www.kernel.org/doc/html/latest/filesystems/ext4/index.html"),
            ("4.1.3", "Storage Device Partitioning, Mounting & /etc/fstab UUID Automation",
             "Block devices /dev/sdX & /dev/nvmeX, GPT vs MBR, fdisk/parted, mount namespaces, loop devices, /etc/fstab filesystem mounts by UUID, and noatime/discard performance options.",
             "https://www.youtube.com/watch?v=Hbdcxzcbk74", "00:00", "NetworkChuck", "https://man7.org/linux/man-pages/man5/fstab.5.html"),
            ("4.1.4", "Logical Volume Management (LVM): Physical Volumes, Volume Groups & Logical Volumes",
             "Storage abstraction layer: PVs, VGs, LVs, dynamic thin-provisioning, online volume expansion with lvextend and resize2fs, and LVM snapshot copy-on-write backups.",
             "https://www.youtube.com/watch?v=F55_dZ0Dk-g", "00:00", "Red Hat", "https://man7.org/linux/man-pages/man8/lvm.8.html")
        ]
    },
    {
        "num": "4.2",
        "title": "Linux Permissions, Access Control Lists (ACLs) & Kernel Security",
        "desc": "Discretionary access control, special permission bits, fine-grained POSIX ACLs, and mandatory access control frameworks.",
        "concepts": [
            ("4.2.1", "Standard File Permissions & Umask Computation",
             "Symbolic vs Octal chmod [4,2,1], user/group/other target bits, chown/chgrp ownership delegation, and default umask bitmask filtering [0022 vs 0027].",
             "https://www.youtube.com/watch?v=1xW7_W5vYg0", "00:00", "freeCodeCamp.org", "https://man7.org/linux/man-pages/man1/chmod.1.html"),
            ("4.2.2", "Special Permission Bits: SUID, SGID & Sticky Bit Mechanics",
             "SUID 4000 root privilege escalation on executables, SGID 2000 directory group inheritance, Sticky Bit 1000 shared deletion protection on /tmp, and security auditing with find -perm.",
             "https://www.youtube.com/watch?v=rW3k_W4x_34", "00:00", "NetworkChuck", "https://man7.org/linux/man-pages/man1/chmod.1.html"),
            ("4.2.3", "POSIX Access Control Lists (ACLs): getfacl & setfacl Fine-Grained Rules",
             "Extending standard permissions, user/group-specific granular permissions, default inherited ACLs for directories, mask recalculation, and backup/restore with getfacl -R / setfacl --restore.",
             "https://www.youtube.com/watch?v=vV7Y_9a0Q8c", "00:00", "Chris Titus Tech", "https://man7.org/linux/man-pages/man1/getfacl.1.html"),
            ("4.2.4", "Linux Security Modules: SELinux Contexts & AppArmor Profiles",
             "Mandatory Access Control (MAC) vs Discretionary Access Control (DAC), SELinux labels [user:role:type:level], getenforce, setenforce, audit2allow, and AppArmor complain/enforce profile containment.",
             "https://www.youtube.com/watch?v=_WOKlUCZFNU", "00:00", "Red Hat", "https://man7.org/linux/man-pages/man8/selinux.8.html")
        ]
    },
    {
        "num": "4.3",
        "title": "Process Lifecycle, Scheduling, Signals & Systemd Internals",
        "desc": "Process tree generation, kernel signal dispatch, CFS thread scheduling, and modern systemd service orchestration.",
        "concepts": [
            ("4.3.1", "Process Lifecycle: fork(), exec(), wait(), PID 1, Zombie & Orphan States",
             "Process table, process states (R running, S interruptible sleep, D uninterruptible disk sleep, Z zombie, T stopped), parent-child trees with pstree, reap routines, and orphan adoption by PID 1.",
             "https://www.youtube.com/watch?v=cex_4V_5X_8", "00:00", "Computerphile", "https://man7.org/linux/man-pages/man2/fork.2.html"),
            ("4.3.2", "Linux Kernel Signals: SIGTERM, SIGKILL, SIGHUP & Signal Traps",
             "Asynchronous inter-process notifications, graceful termination via SIGTERM (15), uncatchable kernel SIGKILL (9), config reloading via SIGHUP (1), and Bash trap handlers.",
             "https://www.youtube.com/watch?v=83M5-NPDeWs", "00:00", "Computerphile", "https://man7.org/linux/man-pages/man7/signal.7.html"),
            ("4.3.3", "CPU Scheduling Priorities: Nice Values, Renice & Completely Fair Scheduler (CFS)",
             "CFS red-black tree virtual runtime algorithm, static niceness scale [-20 highest to 19 lowest], renice dynamic priority adjustment, and real-time scheduling policies SCHED_FIFO / SCHED_RR.",
             "https://www.youtube.com/watch?v=F3wYv0xT4-s", "00:00", "Hussein Nasser", "https://man7.org/linux/man-pages/man1/nice.1.html"),
            ("4.3.4", "Systemd Service Architecture: Unit Files, Targets, Dependencies & journalctl",
             "Modern init system, unit types (.service, .timer, .socket, .target), After/Requires/Wants dependency graphs, restart policies, cgroups resource isolation, and structured querying with journalctl.",
             "https://www.youtube.com/watch?v=Vl0v_6N4Kk8", "00:00", "TechWorld with Nana", "https://systemd.io/")
        ]
    },
    {
        "num": "4.4",
        "title": "Memory Management, Virtual Memory, Paging & Kernel Diagnostics",
        "desc": "Virtual memory addressing, paging mechanisms, buffer/cache architectures, and system bottleneck profiling.",
        "concepts": [
            ("4.4.1", "Virtual Memory Architecture: Pages, Page Tables, MMU & Translation Lookaside Buffers",
             "Virtual address space isolation (User space vs Kernel space), 4KB page frames, multi-level page tables, MMU hardware translation, TLB caching, and Transparent HugePages (THP).",
             "https://www.youtube.com/watch?v=qcBIv_6QY9E", "00:00", "Computerphile", "https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html"),
            ("4.4.2", "Memory Diagnostics: free, Buffer vs Cache, Swappiness & the OOM Killer",
             "Parsing /proc/meminfo, OS buffer cache vs dirty page writeback, swap partition paging, vm.swappiness sysctl tuning, and OOM killer heuristic scoring (oom_score, oom_score_adj).",
             "https://www.youtube.com/watch?v=Xh0Y6a_9N_w", "00:00", "Hussein Nasser", "https://man7.org/linux/man-pages/man1/free.1.html"),
            ("4.4.3", "System Performance Diagnostics: Load Averages, vmstat, mpstat & pidstat",
             "1/5/15-minute load average formulas, CPU run-queue vs uninterruptible disk sleep D-state threads, context switches, interrupt rates, and per-process CPU profiling with pidstat.",
             "https://www.youtube.com/watch?v=kYvH4tN_r2A", "00:00", "Brendan Gregg", "https://man7.org/linux/man-pages/man8/vmstat.8.html"),
            ("4.4.4", "Storage I/O Diagnostics: iostat, df, du, lsof & Kernel Page Cache Flushes",
             "Block I/O saturation, %util, await, r/s, w/s with iostat -xz 1, disk inode exhaustion with df -i, identifying open deleted file descriptors with lsof +L1, and sync/drop_caches.",
             "https://www.youtube.com/watch?v=0k5G_7W8s1c", "00:00", "Brendan Gregg", "https://man7.org/linux/man-pages/man1/iostat.1.html")
        ]
    },
    {
        "num": "4.5",
        "title": "Linux Networking Primitives, Sockets, IPTables & Troubleshooting",
        "desc": "Kernel network stack, socket inspection, packet routing, netfilter firewalls, and deep packet captures.",
        "concepts": [
            ("4.5.1", "Network Interfaces, IP Addressing & Routing Tables (iproute2)",
             "iproute2 modern tooling vs net-tools: ip addr, ip route, ip link; default gateway routing, ARP resolution with ip neigh, loopback interface, and /etc/resolv.conf DNS resolver.",
             "https://www.youtube.com/watch?v=Qi4w1i_2K_4", "00:00", "NetworkChuck", "https://man7.org/linux/man-pages/man8/ip.8.html"),
            ("4.5.2", "Socket States & Network Diagnostics: ss, netstat, lsof -i & curl / dig",
             "TCP finite state machine (LISTEN, ESTABLISHED, TIME_WAIT, CLOSE_WAIT), high-speed socket inspection with ss -tulpn, DNS debugging with dig +trace, and HTTP header tracing with curl -v.",
             "https://www.youtube.com/watch?v=1x0K_Q8s7Yc", "00:00", "Hussein Nasser", "https://man7.org/linux/man-pages/man8/ss.8.html"),
            ("4.5.3", "Packet Filtering & Firewalls: Netfilter, iptables, nftables & ufw",
             "Kernel netfilter hooks (PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING), tables (filter, nat, mangle), chains, stateful connection tracking with conntrack, and UFW / firewalld.",
             "https://www.youtube.com/watch?v=6T_pY9o7r1s", "00:00", "NetworkChuck", "https://netfilter.org/"),
            ("4.5.4", "Network Packet Capture & Deep Analysis: tcpdump & Wireshark Pcap Mechanics",
             "Capturing raw packets at socket layer with tcpdump -nnvv -i any, Berkeley Packet Filter (BPF) syntax, writing pcap dumps, and analyzing TCP 3-way handshakes and retransmissions.",
             "https://www.youtube.com/watch?v=0k1A_3W8s7c", "00:00", "NetworkChuck", "https://www.tcpdump.org/manpages/tcpdump.1.html")
        ]
    },
    {
        "num": "4.6",
        "title": "Advanced Text Processing, IPC, Pipelines & Shell Scripting",
        "desc": "File descriptors, text stream transformation engines, robust defensive scripting, and inter-process communication.",
        "concepts": [
            ("4.6.1", "Standard Streams, File Descriptors (0, 1, 2) & Pipeline Redirection",
             "POSIX file descriptors: stdin (0), stdout (1), stderr (2); redirection operators (>, >>, 2>&1, &>), tee duplicate splitting, anonymous pipes (|), and subshell execution.",
             "https://www.youtube.com/watch?v=9_6F1x8s0Yw", "00:00", "Traversy Media", "https://www.gnu.org/software/bash/manual/html_node/Redirections.html"),
            ("4.6.2", "Text Parsing Powerhouses: grep, sed Stream Editor & awk Field Processing",
             "PCRE regex filtering with grep -E/P, in-place non-interactive stream transformations with sed, and Turing-complete column/record data processing with awk (BEGIN, END, NR, NF, FS).",
             "https://www.youtube.com/watch?v=e_0k5G_7W8s", "00:00", "Luke Smith", "https://www.gnu.org/software/gawk/manual/gawk.html"),
            ("4.6.3", "Enterprise Bash Scripting: Robust Safety Flags, Traps & Exit Codes",
             "Defensive shell programming: set -euo pipefail, trap ERR/EXIT cleanup handlers, parameter expansion ($&#123;VAR:-default&#125;), POSIX test [[ ... ]], and exit code propagation.",
             "https://www.youtube.com/watch?v=v-F3YLd6fto", "00:00", "freeCodeCamp.org", "https://www.gnu.org/software/bash/manual/"),
            ("4.6.4", "Inter-Process Communication (IPC): Named Pipes (FIFOs), Unix Domain Sockets & Shared Memory",
             "Anonymous vs named pipes (mkfifo), high-performance IPC via Unix Domain Sockets (.sock), POSIX shared memory (/dev/shm), semaphores, and message queues.",
             "https://www.youtube.com/watch?v=W0v7W8s1c9o", "00:00", "Computerphile", "https://man7.org/linux/man-pages/man7/pipe.7.html")
        ]
    }
]

def render_subsections_html():
    out = []
    for sub in LINUX_SUBSECTIONS:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]
        out.append(f'''<div class="subsection">
<div class="subsection-head">
<span class="subsection-tag">{num}</span>
<h3>{html_lib.escape(title)}</h3>
<span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>
</div>
<div class="subsection-desc">{html_lib.escape(desc)}</div>
<ol class="concepts">''')
        for cid, cname, cdesc, vid, vtime, vchannel, doc in concepts:
            clean_name = re.sub(r'[^a-zA-Z0-9]+', ' ', cname).lower().strip()
            out.append(f'''<li data-cid="{cid}" data-name="{clean_name}">
<div class="done-check" title="Mark as done"></div>
<div class="bookmark-star" title="Bookmark">☆</div>
<div>
<div class="cname">{html_lib.escape(cname)}</div>
<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>
</div>
<div class="res-links"><a class="video" data-start="0" data-vchannel="{html_lib.escape(vchannel)}" data-vdur="" data-vtitle="{html_lib.escape(cname)}" href="{vid}" rel="noopener" target="_blank" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a><a href="{doc}" rel="noopener" target="_blank" title="Official Reference">🌐Doc</a></div>
</li>''')
        out.append('</ol>\n</div>')
    return '\n'.join(out)

def expand_tech_linux():
    p = os.path.join(ROOT, 'tech_linux.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Linux Engineering · Masterclass 02 · 6 Subsections · 24 Concepts</div>',
        html
    )

    # 2. Update stats block
    old_stats_match = re.search(r'(<div class="stats">[\s\S]*?</div>\s*(?=<div class="overall-progress">))', html)
    if old_stats_match:
        new_stats = '''<div class="stats">
    <div class="stat"><div class="n">6</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">24</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">30+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>\n\n  '''
        html = html.replace(old_stats_match.group(1), new_stats, 1)

    # 3. Update overall progress pct & search placeholder
    html = re.sub(r'<span class="pct" id="overall-pct">[^<]+</span>', '<span class="pct" id="overall-pct">0 / 24</span>', html)
    html = re.sub(r'placeholder="Search [^"]+"', 'placeholder="Search 24 concepts…"', html)

    # 4. Update focus bar & section banner
    html = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        html
    )
    html = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        html,
        count=1
    )
    html = re.sub(
        r'<div class="pct-text" data-pp-text="4">[^<]+</div>',
        '<div class="pct-text" data-pp-text="4">0 / 24</div>',
        html
    )

    # 5. Replace subsections inside section-4
    subs_html = render_subsections_html()
    sub_start = html.find('<div class="subsection">')
    sub_end = html.find('</section>', sub_start)
    if sub_start != -1 and sub_end != -1:
        html = html[:sub_start] + subs_html + '\n' + html[sub_end:]
        print("Updated subsections in tech_linux.html")
    else:
        raise ValueError("Could not find subsections in tech_linux.html")

    atomic_write(p, html)
    print("Saved tech_linux.html successfully!")

def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition & hero stats
    html = re.sub(
        r'<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; \d+ Subsections &bull; \d+ Concepts</div>',
        '<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; 53 Subsections &bull; 209 Concepts</div>',
        html
    )

    # Subsections: 50 -> 53, Concepts: 197 -> 209
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        r'\g<1>53\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        r'\g<1>209\g<2>',
        html
    )

    # 2. Update card-linux in domain deck
    card_linux_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-linux"[\s\S]*?</div>\s*</div>)', html)
    if card_linux_match:
        old_card = card_linux_match.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">Kernel, Processes, Bash & System Troubleshooting</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-linux in all_tech.html")

    # 3. Update Section 4 header, banner, and subsections
    sec4_match = re.search(r'(<section class="section domain-section"[^>]*id="section-4"[\s\S]*?</section>)', html)
    if sec4_match:
        sec4_text = sec4_match.group(1)
        
        sec4_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
            sec4_text
        )
        sec4_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">6 subsections · 24 concepts</div>',
            sec4_new
        )
        sec4_new = re.sub(
            r'<div class="pct-text" data-pp-text="4">[^<]+</div>',
            '<div class="pct-text" data-pp-text="4">0 / 24</div>',
            sec4_new
        )

        subs_html = render_subsections_html()
        sub_start = sec4_new.find('<div class="subsection">')
        sub_end = sec4_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec4_new = sec4_new[:sub_start] + subs_html + '\n' + sec4_new[sub_end:]
            html = html.replace(sec4_text, sec4_new, 1)
            print("Updated section-4 in all_tech.html")
        else:
            raise ValueError("Could not find subsections in section-4 of all_tech.html")
    else:
        raise ValueError("Could not find section-4 in all_tech.html")

    atomic_write(p, html)
    print("Saved all_tech.html successfully!")

if __name__ == '__main__':
    expand_tech_linux()
    expand_all_tech()
    print("Finished expanding Linux Masterclass!")
