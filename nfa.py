class InputError(Exception):
    pass

class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}  # Maps input symbols to sets of states
        self.epsilon_transitions = []  # List of states reachable via epsilon transitions

    def add_transition(self, symbol, state):
        if symbol:
            if symbol not in self.transitions:
                self.transitions[symbol] = set()
            self.transitions[symbol].add(state)
        else:
            self.epsilon_transitions.append(state)

    def epsilon_closure(self):
        """Compute the epsilon closure for this state."""
        closure = {self}
        stack = [self]
        while stack:
            state = stack.pop()
            for next_state in state.epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

class NFA:
    def __init__(self, start_state, final_states):
        self.start_state = start_state
        self.final_states = final_states

    def run(self, input_string):
        # Start with the epsilon closure of the start state
        current_states = self.start_state.epsilon_closure()
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    for next_state in state.transitions[symbol]:
                        next_states = next_states.union(next_state.epsilon_closure())
            current_states = next_states
        
        # Check if any of the current states are final states
        return any(state.is_final for state in current_states)

def literal_nfa(literal):
    start = State()
    end = State(is_final=True)
    start.add_transition(literal, end)
    return NFA(start, {end})

def concatenate(nfa1, nfa2):
    for final_state in nfa1.final_states:
        final_state.is_final = False
        final_state.epsilon_transitions.extend([nfa2.start_state])
    return NFA(nfa1.start_state, nfa2.final_states)

def union(nfa1, nfa2):
    start = State()
    start.epsilon_transitions.extend([nfa1.start_state, nfa2.start_state])
    final_states = nfa1.final_states.union(nfa2.final_states)
    return NFA(start, final_states)

def kleene_star(nfa):
    start = State()
    end = State(is_final=True)
    start.epsilon_transitions.append(nfa.start_state)
    start.epsilon_transitions.append(end)
    for final_state in nfa.final_states:
        final_state.is_final = False
        final_state.epsilon_transitions.append(nfa.start_state)
        final_state.epsilon_transitions.append(end)
    return NFA(start, {end})

def parse_tree_to_nfa(node):
    if node.value.isnumeric() or node.value.isalpha():
        return literal_nfa(node.value)
    
    elif node.value == '.':
        nfa_left = parse_tree_to_nfa(node.left)
        nfa_right = parse_tree_to_nfa(node.right)
        return concatenate(nfa_left, nfa_right)
    
    elif node.value == '|':
        nfa_left = parse_tree_to_nfa(node.left)
        nfa_right = parse_tree_to_nfa(node.right)
        return union(nfa_left, nfa_right)
    
    elif node.value == '*':
        child_nfa = parse_tree_to_nfa(node.child())
        return kleene_star(child_nfa)
    