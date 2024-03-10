from avl_tree import insert, find

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
    
    
def test_find():
    tree = insert(None, 1020, 'a')
    tree = insert(tree, 520, 'b')
    tree = insert(tree, 720, 'c')
    tree = insert(tree, 1320, 'd')
    tree = insert(tree, 220, 'e')
    tree = insert(tree, 9020, 'f')
    
    assert find(tree, 10) == None
    assert find(tree, 520) == 'b'
    assert find(tree, 9020) == 'f'
    