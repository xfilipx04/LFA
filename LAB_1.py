import random

class Grammar:
    def __init__(self):
        self.VN = {"S", "B", "C", "D"}  # Non-terminals
        self.VT = {"a", "b", "c"}  # Terminals
        self.P = {
            "S": ["aB"],
            "B": ["bS", "aC", "b"],
            "C": ["bD"],
            "D": ["a", "bC", "cS"]
        }
        self.start_symbol = "S"
    
    def generate_string(self, max_length=10):
        """Generate a random valid string based on the grammar rules."""
        word = self.start_symbol
        while any(symbol in self.VN for symbol in word) and len(word) < max_length:
            for i, symbol in enumerate(word):
                if symbol in self.VN:
                    replacement = random.choice(self.P[symbol])  # Choose a random rule
                    word = word[:i] + replacement + word[i+1:]  # Replace non-terminal
                    break  # Apply one rule per iteration
        return word if all(s not in self.VN for s in word) else self.generate_string(max_length)  # Ensure only terminals remain
    
    def generate_strings(self, count=5):
        """Generate multiple unique valid strings from the grammar."""
        unique_strings = set()
        while len(unique_strings) < count:
            new_string = self.generate_string()
            unique_strings.add(new_string)
        return list(unique_strings)

class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.VN
        self.alphabet = grammar.VT
        self.start_state = grammar.start_symbol
        self.transitions = {}
        self.final_states = set()

        # Construct transitions and final states based on the grammar
        for non_terminal, productions in grammar.P.items():
            for production in productions:
                if all(symbol in self.alphabet for symbol in production):
                    self.final_states.add(non_terminal)  # If production consists only of terminals, mark as final state
                else:
                    symbol, next_state = production[0], production[1:]  # Extract transition details
                    self.transitions.setdefault((non_terminal, symbol), []).append(next_state)

    def accepts(self, input_string):
        """Check if the input string is accepted by the FA."""
        current_states = {self.start_state}  # Start from initial state
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])  # Move to next states
            if not next_states:
                return False  # If no valid transitions, reject string
            current_states = next_states  # Update current states
        return any(state in self.final_states for state in current_states)  # Check if any final state is reached

# Usage
grammar = Grammar()
generated_strings = grammar.generate_strings()
print("Generated Strings:", generated_strings)

fa = FiniteAutomaton(grammar)
test_string = "a"
print(f"Does the FA accept '{test_string}'?", test_string in generated_strings)
