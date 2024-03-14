from typing import Optional


class Node:
    def __init__(self, key, value = None) -> None:
        self.key = key
        self.value = value
        self.height = 1
        self.left = None
        self.right = None

def _get_height(node: Node) -> int:
    return node.height if node else 0

def _get_balance(node: Node) -> int:
    return _get_height(node.left) - _get_height(node.right) if node else 0

def _update_height(node: Node) -> int:
    return 1 + max(_get_height(node.left), _get_height(node.right))

def _rotate_left(node: Node) -> Node:
    right = node.right
    node.right = right.left
    right.left = node
    
    node.height = _update_height(node)
    right.height = _update_height(right)
    return right

def _rotate_right(node: Node) -> Node:
    left = node.left
    node.left = left.right
    left.right = node
    
    node.height = _update_height(node)
    left.height = _update_height(left)
    return left

def insert(node: Node, key, value = None) -> Node:
    if not node:
        return Node(key, value)
    
    if key < node.key:
        node.left = insert(node.left, key, value)
    else:
        node.right = insert(node.right, key, value)
        
    node.height = _update_height(node)
    
    # Rebalance the tree
    balance = _get_balance(node)
    
    # Left-left
    if balance > 1 and key < node.left.key:
        return _rotate_right(node)
    
    # Right-right
    if balance < -1 and key > node.right.key:
        return _rotate_left(node)
    
    # Left-right
    if balance > 1 and key > node.left.key:
        node.left = _rotate_left(node.left)
        return _rotate_right(node)
    
    # Right-left
    if balance < -1 and key < node.right.key:
        node.right = _rotate_right(node.right)
        return _rotate_left(node)
    
    return node
    
def find(node: Node, key) -> Optional[any]:
    if not node: return None
    if key < node.key: return find(node.left, key)
    if key > node.key: return find(node.right, key)
    return node.value

# TODO: remove
