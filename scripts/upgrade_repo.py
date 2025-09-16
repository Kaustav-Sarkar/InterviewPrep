#!/usr/bin/env python3
"""
One-time upgrade script to:
- Add additional graph/container data structures
- Enrich each Markdown with practice scenarios (8–10 per DS)
- Prefix core docs with 1.0_ so they sort first
- Rebuild README with Core / Graphs / Extended sections

Run once, then remove scripts/ per project guidance.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

BASE_DIR = Path('/Users/ks/Coding/Prep/InterviewPrep').resolve()

# Existing comprehensive list + approved additions
ALL_DS: List[str] = [
    # Linear / foundational
    'Array',
    'LinkedList_Singly',
    'LinkedList_Doubly',
    'Stack',
    'Queue',
    'Deque',
    'CircularQueue',
    'CircularBuffer',
    'MonotonicStack',
    'MonotonicQueue',

    # Priority queues & heaps
    'PriorityQueue_BinaryHeap',
    'MinMaxHeap',
    'Heap_Binomial',
    'Heap_Fibonacci',

    # Associative / hashing
    'HashTable',
    'Set',
    'BitSet_Bitmap',

    # Probabilistic
    'BloomFilter',
    'CuckooFilter',
    'CountMinSketch',
    'HyperLogLog',

    # Strings / tries / suffix structures
    'String_Rope',
    'Trie_PrefixTree',
    'PatriciaTrie',
    'TernarySearchTree',
    'SuffixArray',
    'SuffixTree',
    'SuffixAutomaton',

    # Disjoint sets
    'DisjointSet_UnionFind',

    # Trees
    'BinaryTree_Generic',
    'BinarySearchTree',
    'AVLTree',
    'RedBlackTree',
    'Treap',
    'SplayTree',
    'OrderStatisticTree',
    'CartesianTree',

    # Range / index structures
    'SegmentTree',
    'SegmentTree_LazyPropagation',
    'FenwickTree',
    'IntervalTree',
    'SparseTable',

    # Spatial / B-trees
    'KdTree',
    'BTree',
    'BPlusTree',
    'SkipList',

    # Graph representations (existing)
    'Graph_AdjacencyList',
    'Graph_AdjacencyMatrix',
    'Graph_EdgeList',

    # Caching
    'LRUCache',
    'LFUCache',

    # Misc bucket
    'Misc_SpecializedStructures',

    # NEW (approved): Graph forms
    'Graph_CSR',
    'Graph_COO',
    'Graph_AdjacencySet',
    'Graph_AdjacencyMap',
    'Graph_Multigraph',

    # NEW (approved): Additional container flavors
    'Map_Dictionary',
    'OrderedMap_TreeMap',
    'OrderedSet_TreeSet',
    'Multiset_Bag',
    'Multimap',
]

# Core set to be prefixed as 1.0_ in docs (filesystem ordering only)
CORE: List[str] = [
    'Array',
    'LinkedList_Singly',
    'LinkedList_Doubly',
    'Stack',
    'Queue',
    'Deque',
    'HashTable',
    'Set',
    'PriorityQueue_BinaryHeap',
    'MinMaxHeap',
    'Graph_AdjacencyList',
    'Graph_AdjacencyMatrix',
    'Graph_EdgeList',
    'BinaryTree_Generic',
    'BinarySearchTree',
    'Trie_PrefixTree',
    'LRUCache',
]


def camel_from_name(name: str) -> str:
    if '_' in name:
        parts = name.split('_')
        return ''.join(p[:1].upper() + p[1:] for p in parts)
    return name[0].upper() + name[1:]


def snake_from_name(name: str) -> str:
    tmp = name.replace('_', ' ')
    tmp = re.sub(r'(?<!^)(?=[A-Z])', ' ', tmp)
    return '_'.join(tmp.lower().split())


def friendly_title(name: str) -> str:
    tmp = name.replace('_', ' ')
    tmp = re.sub(r'(?<!^)(?=[A-Z])', ' ', tmp)
    tmp = tmp.replace('Avl', 'AVL').replace('Kd', 'KD').replace('Btree', 'B-Tree').replace('B Plus Tree', 'B+ Tree')
    tmp = tmp.replace('R B', 'Red Black').replace('Redblack', 'Red Black')
    return ' '.join(tmp.split()).title().replace('Avl', 'AVL').replace('Kd', 'KD').replace('B+ Tree', 'B+ Tree')


def ds_category(name: str) -> str:
    if name.startswith('Graph_'):
        return 'graph'
    if name in {'Array'}:
        return 'array'
    if name.startswith('LinkedList'):
        return 'linkedlist'
    if name in {'Stack', 'MonotonicStack'}:
        return 'stack'
    if name in {'Queue', 'CircularQueue', 'MonotonicQueue'}:
        return 'queue'
    if name == 'Deque' or name == 'CircularBuffer':
        return 'deque'
    if name in {'HashTable', 'Map_Dictionary', 'Multimap'}:
        return 'hashmap'
    if name in {'Set', 'OrderedSet_TreeSet'}:
        return 'set'
    if 'Heap' in name or name.startswith('PriorityQueue_'):
        return 'heap'
    if name in {'BinaryTree_Generic', 'BinarySearchTree'}:
        return 'tree_basic'
    if name in {'AVLTree', 'RedBlackTree', 'SplayTree', 'Treap', 'OrderStatisticTree', 'CartesianTree'}:
        return 'balanced_tree'
    if name in {'SegmentTree', 'SegmentTree_LazyPropagation', 'FenwickTree', 'SparseTable'}:
        return 'range'
    if name == 'IntervalTree':
        return 'interval'
    if name in {'Trie_PrefixTree', 'PatriciaTrie', 'TernarySearchTree'}:
        return 'trie'
    if name in {'String_Rope'}:
        return 'string_rope'
    if name in {'SuffixArray', 'SuffixTree', 'SuffixAutomaton'}:
        return 'suffix'
    if name in {'DisjointSet_UnionFind'}:
        return 'dsu'
    if name in {'BloomFilter', 'CuckooFilter', 'CountMinSketch', 'HyperLogLog'}:
        return 'probabilistic'
    if name in {'LRUCache', 'LFUCache'}:
        return 'cache'
    if name in {'KdTree'}:
        return 'spatial'
    if name in {'BTree', 'BPlusTree'}:
        return 'btree'
    if name in {'SkipList'}:
        return 'skiplist'
    if name in {'OrderedMap_TreeMap'}:
        return 'ordered_map'
    return 'generic'


def scenarios_for(name: str) -> List[str]:
    cat = ds_category(name)
    if cat == 'graph':
        return [
            'Find shortest path in an unweighted graph (BFS on adjacency list).',
            'Detect cycles in a directed graph (DFS, recursion stack).',
            'Topological sort for task scheduling (Kahn/DFS).',
            'Check if a graph is bipartite (BFS coloring).',
            'Count connected components in an undirected graph.',
            'Design adjacency representation for sparse vs dense graphs (CSR vs matrix).',
            'Implement Dijkstra on adjacency list with a min-heap.',
            'Model a grid as a graph to solve shortest path with obstacles.',
            'Track parallel edges/self-loops in a multigraph.',
            'Store weighted graphs with map-of-maps (AdjacencyMap).',
        ]
    if cat == 'array':
        return [
            'Two-sum and k-sum with sorting/two-pointers.',
            'Maximum subarray (Kadane).',
            'Prefix sums for range sum queries.',
            'Move zeros in-place maintaining order.',
            'Rotate array by k steps in-place.',
            'Merge overlapping intervals after sorting.',
            'Remove duplicates from sorted array.',
            'Dutch National Flag (3-way partition).',
            'Find kth element via quickselect.',
            'Sliding window for fixed-size averages.',
        ]
    if cat == 'linkedlist':
        return [
            'Reverse a singly linked list (iterative/recursive).',
            'Detect cycle (Floyd’s) and find entry point.',
            'Merge two sorted linked lists.',
            'Remove Nth node from end (two pointers).',
            'Copy list with random pointer (hash map).',
            'LRU cache node splicing with doubly linked list.',
            'Palindrome check using slow/fast pointers.',
            'Partition list by pivot (stable).',
        ]
    if cat == 'stack':
        return [
            'Validate parentheses/brackets.',
            'Evaluate RPN expression.',
            'Implement min-stack with O(1) min.',
            'Largest rectangle in histogram (monotonic stack).',
            'Next greater element using monotonic stack.',
            'Decode nested strings (stack of states).',
            'Infix to postfix conversion.',
        ]
    if cat == 'queue' or cat == 'deque':
        return [
            'Implement stack using two queues or queue using two stacks.',
            'Sliding window maximum with deque (monotonic).',
            'Round-robin scheduling with circular queue.',
            'Level-order traversal (BFS) of a tree.',
            'Producer–consumer buffer with circular buffer.',
            'Rate limiting/token bucket queueing.',
        ]
    if cat == 'hashmap':
        return [
            'Group anagrams with signature hashing.',
            'Two-sum using hash set/map.',
            'First unique character index.',
            'Frequency counting and bucket grouping.',
            'LRU index map for O(1) updates.',
            'Design multimap for one-to-many relationships.',
            'Implement symbol table for interpreter.',
            'Deduplicate stream items.',
        ]
    if cat == 'set':
        return [
            'Check if two arrays have common elements.',
            'Compute union, intersection, difference.',
            'Detect near-duplicates with rolling window.',
            'Track visited states in BFS/DFS.',
            'Unique substrings of length k.',
            'Membership checks for blacklist/whitelist.',
        ]
    if cat == 'heap':
        return [
            'Find kth largest/smallest in stream.',
            'Merge k sorted lists.',
            'Task scheduler based on priority.',
            'Maintain median of a stream (two heaps).',
            'Top-k frequent elements with min-heap.',
            'Online interval scheduling with PQ.',
        ]
    if cat == 'tree_basic':
        return [
            'Inorder traversal to get sorted order in BST.',
            'Validate BST property.',
            'Lowest common ancestor in BST.',
            'Compute tree height, diameter.',
            'Serialize/deserialize binary tree.',
            'Check symmetry and balanced height.',
        ]
    if cat == 'balanced_tree':
        return [
            'Maintain ordered map/set with guaranteed log-time ops.',
            'Order statistics: kth element/rank queries.',
            'Interval indexing with treap priorities.',
            'Self-adjusting access patterns (splay).',
            'Randomized balancing for simple code (treap).',
            'Persistent versions via path-copying (conceptual).',
        ]
    if cat == 'range':
        return [
            'Range sum query with point updates (Fenwick).',
            'Range min/max with segment tree.',
            'Lazy propagation for range add/assign.',
            'RMQ via sparse table (static array).',
            '2D BIT/segment tree for grids.',
            'Kth order statistics in range (augmented).',
        ]
    if cat == 'interval':
        return [
            'Calendar booking conflict detection.',
            'Find all intervals overlapping a query interval.',
            'Stabbing queries for points.',
            'Room scheduling minimum count.',
            'Genome feature overlap queries.',
        ]
    if cat == 'trie':
        return [
            'Autocomplete and prefix search.',
            'Spell-check with edit distance pruning.',
            'Word break with dictionary prefixes.',
            'Longest common prefix among words.',
            'IP routing prefix matching (Patricia).',
            'Ternary search tree for memory-efficient dictionary.',
        ]
    if cat == 'string_rope':
        return [
            'Efficient insert/delete in large text buffers.',
            'Concatenate many strings without quadratic blowup.',
            'Subsequence splicing and substring operations.',
            'Text editor gap/rope trade-offs.',
            'Undo/redo via persistent ropes.',
        ]
    if cat == 'suffix':
        return [
            'Substring search (pattern occurs?)',
            'Count distinct substrings.',
            'Number of different substrings repeated at least twice.',
            'Longest repeated substring.',
            'Longest common substring among strings.',
            'Lexicographic suffix order for indexing.',
        ]
    if cat == 'dsu':
        return [
            'Count connected components dynamically.',
            'Kruskal’s MST union operations.',
            'Detect cycles while adding edges.',
            'Merge accounts (emails/users).',
            'Percolation connectivity in grids.',
        ]
    if cat == 'probabilistic':
        return [
            'Fast membership test with limited memory (Bloom).',
            'Approximate distinct count in streams (HLL).',
            'Heavy hitters / frequency estimation (CMS).',
            'Duplicate suppression in pipelines.',
            'Spam filtering / URL cache pre-check.',
        ]
    if cat == 'cache':
        return [
            'Design LRU/LFU cache for key-value store.',
            'Page replacement simulation.',
            'API rate limiters with TTL-like eviction.',
            'Database buffer pool policy comparison.',
            'Image thumbnail cache.',
        ]
    if cat == 'spatial':
        return [
            'k-NN search in 2D/3D points.',
            'Range search in rectangles.',
            'Collision detection broad-phase.',
            'Geospatial proximity queries.',
            'Clustering acceleration (approximate).',
        ]
    if cat == 'btree':
        return [
            'Disk-friendly ordered index (DB storage engine).',
            'Range scans with minimal IO (B+ tree leaves).',
            'Implement key compression / high fan-out nodes.',
            'Multi-version concurrency (conceptual).',
            'Filesystem directory indexing.',
        ]
    if cat == 'skiplist':
        return [
            'Ordered map/set with randomized balancing.',
            'Concurrent-friendly ordered structure.',
            'Time-series index with fast inserts.',
            'Leaderboard ordered by score.',
            'Range queries by pointers.',
        ]
    return [
        'Design a data structure supporting required operations efficiently.',
        'Choose appropriate structure for access/update patterns.',
        'Trade-offs among time, space, and implementation complexity.',
        'Optimize for streaming vs batch workloads.',
        'Scale to large N with appropriate representation.',
        'Memory locality and cache-aware considerations.',
        'Concurrency implications and safe iteration.',
        'Debugging invariants and test strategies.',
    ]


def md_template(name: str) -> str:
    camel = camel_from_name(name)
    snake = snake_from_name(name)
    title = friendly_title(name)
    scenarios = scenarios_for(name)
    lines: List[str] = []
    lines.append(f"### {title}")
    lines.append("")
    lines.append("#### Definition & core idea")
    lines.append("Concise definition and the intuition behind the structure.")
    lines.append("")
    lines.append("#### Time–space complexity")
    lines.append("| Operation | Average | Worst | Space |\n|---|---|---|---|\n| Insert | TBD | TBD | TBD |\n| Delete | TBD | TBD | TBD |\n| Search/Access | TBD | TBD | TBD |")
    lines.append("")
    lines.append("#### Real-world use-cases")
    lines.append("- Add concrete scenarios where this excels (systems, apps, infra).")
    lines.append("")
    lines.append("#### When to choose over alternatives")
    lines.append("- Guidance on trade-offs vs. neighboring structures.")
    lines.append("")
    lines.append("#### Implementations")
    lines.append(f"- Native: [Python](../python/native/{snake}.py), [Java](../java/native/{camel}.java)")
    lines.append(f"- Std-lib–based: [Python](../python/stdlib/{snake}_std.py), [Java](../java/stdlib/{camel}Std.java)")
    lines.append("")
    lines.append("#### Practice scenarios & interview-style questions")
    for s in scenarios[:10]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("#### Further reading")
    lines.append("- See curated notes in `../docs/`.")
    lines.append("")
    return "\n".join(lines)


def write_file(path: Path, content: str, overwrite: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding='utf-8')


def py_native_template(name: str) -> str:
    camel = camel_from_name(name)
    return f'''"""Native implementation scaffold for {camel}."""\n\nclass {camel}:\n    """High-level description of {camel} behavior and invariants."""\n\n    def __init__(self) -> None:\n        pass\n\n    def __repr__(self) -> str:\n        return f"<{camel} />"\n'''


def py_stdlib_template(name: str) -> str:
    camel = camel_from_name(name)
    return f'''"""Stdlib-backed wrapper scaffold for {camel}.\n\nThis class demonstrates idiomatic usage of Python built-ins/stdlib to model {camel}.\n"""\n\nclass {camel}Std:\n    """Wrapper around Python built-ins that behaves like {camel}."""\n\n    def __init__(self) -> None:\n        pass\n\n    def __repr__(self) -> str:\n        return f"<{camel}Std />"\n'''


def java_native_template(name: str) -> str:
    camel = camel_from_name(name)
    return f'''/** Native implementation scaffold for {camel}. */\npublic class {camel} {{\n    public {camel}() {{}}\n    @Override public String toString() {{ return "<{camel} />"; }}\n}}\n'''


def java_stdlib_template(name: str) -> str:
    camel = camel_from_name(name)
    return f'''/** Stdlib-backed wrapper scaffold for {camel}. */\npublic class {camel}Std {{\n    public {camel}Std() {{}}\n    @Override public String toString() {{ return "<{camel}Std />"; }}\n}}\n'''


def build_readme(core_names: List[str], graph_names: List[str], extended_names: List[str]) -> str:
    lines: List[str] = []
    lines.append('### DSA Documentation & Implementations')
    lines.append('')
    lines.append('This is a study reference guide with native and stdlib-backed implementations in Python and Java.')
    lines.append('')
    lines.append('#### Core (1.0)')
    for ds in core_names:
        lines.append(f'- [1.0_{ds}](datastructures/1.0_{ds}.md)')
    lines.append('')
    lines.append('#### Graphs (representations)')
    for ds in graph_names:
        lines.append(f'- [{ds}](datastructures/{ds}.md)')
    lines.append('')
    lines.append('#### Extended structures')
    for ds in extended_names:
        lines.append(f'- [{ds}](datastructures/{ds}.md)')
    return "\n".join(lines) + "\n"


def generate():
    ds_dir = BASE_DIR / 'datastructures'
    py_native_dir = BASE_DIR / 'python' / 'native'
    py_std_dir = BASE_DIR / 'python' / 'stdlib'
    java_native_dir = BASE_DIR / 'java' / 'native'
    java_std_dir = BASE_DIR / 'java' / 'stdlib'

    ds_dir.mkdir(parents=True, exist_ok=True)
    py_native_dir.mkdir(parents=True, exist_ok=True)
    py_std_dir.mkdir(parents=True, exist_ok=True)
    java_native_dir.mkdir(parents=True, exist_ok=True)
    java_std_dir.mkdir(parents=True, exist_ok=True)

    # Write docs and code
    for ds in ALL_DS:
        camel = camel_from_name(ds)
        snake = snake_from_name(ds)

        # Markdown path with 1.0_ prefix for core
        md_name = f'1.0_{ds}.md' if ds in CORE else f'{ds}.md'
        md_path = ds_dir / md_name
        write_file(md_path, md_template(ds), overwrite=True)

        # If core, remove old unprefixed duplicate doc to avoid confusion
        if ds in CORE:
            old_path = ds_dir / f'{ds}.md'
            if old_path.exists():
                try:
                    old_path.unlink()
                except Exception:
                    pass

        # Python native
        write_file(py_native_dir / f'{snake}.py', py_native_template(ds), overwrite=False)
        # Python stdlib
        write_file(py_std_dir / f'{snake}_std.py', py_stdlib_template(ds), overwrite=False)
        # Java native
        write_file(java_native_dir / f'{camel}.java', java_native_template(ds), overwrite=False)
        # Java stdlib
        write_file(java_std_dir / f'{camel}Std.java', java_stdlib_template(ds), overwrite=False)

    # Build README sections
    core_list = [ds for ds in CORE]
    graph_list = [ds for ds in ALL_DS if ds.startswith('Graph_') and ds not in CORE]
    extended_list = [ds for ds in ALL_DS if ds not in CORE and not ds.startswith('Graph_')]

    readme_path = BASE_DIR / 'README.md'
    readme_content = build_readme(core_list, graph_list, extended_list)
    write_file(readme_path, readme_content, overwrite=True)


if __name__ == '__main__':
    generate()
    print(f'Upgraded repository: {len(ALL_DS)} data structures, core docs prefixed, scenarios added.')


