from avl_tree import insert

def test_balance():
    def height(node): return node.height if node else 0
    def balance(node): return height(node.left) - height(node.right) if node else 0
    def balanced(node): return abs(balance(node)) <= 1
    
    tree = None
    tree = insert(tree, 5)
    tree = insert(tree, 7)
    tree = insert(tree, 13)
    tree = insert(tree, 2)
    tree = insert(tree, 90)
    
    assert balanced(tree)
    
def test_keys():
    tree = insert(None, 10)
    tree = insert(tree, 5)
    tree = insert(tree, 7)
    tree = insert(tree, 13)
    tree = insert(tree, 2)
    tree = insert(tree, 90)
    
    keys = []
    stack = [tree]
    while stack:
        node = stack.pop()
        keys.append(node.key)
        if node.left: stack.append(node.left)
        if node.right: stack.append(node.right)
        
    correct = {10, 5, 7, 13, 2, 90}
    
    assert len(keys) == len(correct)
    assert all([key in correct for key in keys])
    
    
    