def get_block_cnt(node):
    if not node:
        return 0
    total = 1
    for child in node.get('children', []):
        total += get_block_cnt(child)
    return total

def get_total_branch(node):
    return get_block_cnt(node) - 1

def get_depth_sum(node, depth=1):
    if not node:
        return 0
    total = depth
    if 'children' in node:
        for child in node['children']:
            total += get_depth_sum(child, depth + 1)
    return total

def get_lmcc(tree_node):
    ALPHA = 0.8
    total_branch = get_total_branch(tree_node)
    depth_sum = get_depth_sum(tree_node, depth=1)
    return depth_sum*(1-ALPHA) + total_branch*ALPHA
