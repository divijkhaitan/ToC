class DFAState:
    def __init__(self, alphabet, name, is_final=False):
        self.is_final = is_final
        self.name = name
        self.alphabet = set(alphabet)
        self.transitions = {}  # Maps input symbols to sets of states

    def set_transitions(self, transitions):
        alph = [x[0] for x in transitions]
        if set(alph) != self.alphabet:
            print("Need to make sure every character in the alphabet has an out transition")
            return
        for x in transitions:
            self.transitions[x[0]] = x[1]

class DFA:
    def __init__(self, start_state, final_states, alphabet):
        self.start_state = start_state
        self.final_states = final_states
        self.alphabet = alphabet
    
    def run(self, input_string):
        current_state = self.start_state
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Input String has symbol {symbol} which is not in the alphabet")
            try: 
                current_state = current_state.transitions[symbol]
            except:
                raise ValueError(f"Defined state {current_state.name} without appropriate transition from symbol {symbol}. A DFA must have defined transition function for every input symbol.")
            
        return current_state.is_final
    
