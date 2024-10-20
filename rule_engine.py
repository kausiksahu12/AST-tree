import re

class Node:
    """Defines the structure of an AST Node."""
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # left child node
        self.right = right  # right child node
        self.value = value  # value if it's an operand node (e.g., condition)

def parse_condition(condition):
    """Parses a condition (e.g., 'age > 30') into an AST operand node."""
    match = re.match(r'(\w+)\s*([><=]+)\s*(\w+)', condition)
    if match:
        field, operator, value = match.groups()
        return Node('operand', value={"field": field, "operator": operator, "value": value})
    return None

def create_rule(rule_string):
    """Converts a rule string into an AST."""
    rule_string = rule_string.strip()
    
    # Handle parenthesis
    if rule_string.startswith('(') and rule_string.endswith(')'):
        rule_string = rule_string[1:-1]
    
    # Split the rule string into components based on AND/OR
    if ' AND ' in rule_string:
        parts = rule_string.split(' AND ')
        left = create_rule(parts[0])
        right = create_rule(parts[1])
        return Node('operator', left=left, right=right, value='AND')
    
    if ' OR ' in rule_string:
        parts = rule_string.split(' OR ')
        left = create_rule(parts[0])
        right = create_rule(parts[1])
        return Node('operator', left=left, right=right, value='OR')
    
    # If it's a simple condition
    return parse_condition(rule_string)

def combine_rules(rules):
    """Combines multiple ASTs into a single AST using 'AND' logic."""
    if len(rules) == 1:
        return create_rule(rules[0])
    
    root = create_rule(rules[0])
    for rule in rules[1:]:
        next_rule_ast = create_rule(rule)
        root = Node('operator', left=root, right=next_rule_ast, value='AND')
    
    return root

def evaluate_condition(node, data):
    """Evaluates a single condition node (operand) against the provided data."""
    field = node.value['field']
    operator = node.value['operator']
    value = node.value['value']
    
    if field in data:
        if operator == '>':
            return data[field] > int(value)
        elif operator == '<':
            return data[field] < int(value)
        elif operator == '=':
            return str(data[field]) == str(value)
    return False

def evaluate_rule(node, data):
    """Evaluates the rule represented by the AST against the provided data."""
    if node.type == 'operand':
        return evaluate_condition(node, data)
    
    elif node.type == 'operator':
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)
        
        if node.value == 'AND':
            return left_eval and right_eval
        elif node.value == 'OR':
            return left_eval or right_eval
    
    return False
