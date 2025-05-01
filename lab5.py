from collections import defaultdict, deque
import copy

class CFGtoCNFConverter:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = defaultdict(list)
        for left, right in productions:
            self.productions[left].append(right)
        self.start_symbol = start_symbol
        self.new_symbol_index = 1

    def _get_new_variable(self):
        while True:
            new_var = f"X{self.new_symbol_index}"
            self.new_symbol_index += 1
            if new_var not in self.variables:
                self.variables.add(new_var)
                return new_var

    def remove_epsilon_productions(self):
        nullable = set()
        for A in self.productions:
            for rule in self.productions[A]:
                if rule == ['ε']:
                    nullable.add(A)

        changed = True
        while changed:
            changed = False
            for A in self.productions:
                for rule in self.productions[A]:
                    if all(symbol in nullable for symbol in rule) and A not in nullable:
                        nullable.add(A)
                        changed = True

        new_productions = defaultdict(list)
        for A in self.productions:
            for rule in self.productions[A]:
                subsets = [[]]
                for symbol in rule:
                    new_subsets = []
                    for s in subsets:
                        if symbol in nullable:
                            new_subsets.append(s + [symbol])
                            new_subsets.append(s)  # skip nullable
                        else:
                            new_subsets.append(s + [symbol])
                    subsets = new_subsets
                for s in subsets:
                    if s and s not in new_productions[A]:
                        new_productions[A].append(s)
        self.productions = new_productions

    def remove_unit_productions(self):
        new_productions = defaultdict(list)
        for A in self.productions:
            queue = deque([A])
            visited = set()
            while queue:
                B = queue.popleft()
                for rule in self.productions[B]:
                    if len(rule) == 1 and rule[0] in self.variables:
                        if rule[0] not in visited:
                            queue.append(rule[0])
                            visited.add(rule[0])
                    else:
                        if rule not in new_productions[A]:
                            new_productions[A].append(rule)
        self.productions = new_productions

    def remove_non_productive_symbols(self):
        productive = set()
        changed = True
        while changed:
            changed = False
            for A in self.productions:
                for rule in self.productions[A]:
                    if all(symbol in self.terminals or symbol in productive for symbol in rule):
                        if A not in productive:
                            productive.add(A)
                            changed = True

        self.productions = {A: [r for r in self.productions[A] if all(s in productive or s in self.terminals for s in r)]
                            for A in productive}
        self.variables = productive

    def remove_inaccessible_symbols(self):
        accessible = set()
        queue = deque([self.start_symbol])
        while queue:
            A = queue.popleft()
            if A not in accessible:
                accessible.add(A)
                for rule in self.productions.get(A, []):
                    for symbol in rule:
                        if symbol in self.variables and symbol not in accessible:
                            queue.append(symbol)
        self.productions = {A: self.productions[A] for A in accessible}
        self.variables = accessible

    def convert_to_cnf(self):
        # Step 1: Replace terminals in long rules
        terminal_map = {}
        for A in list(self.productions):
            new_rules = []
            for rule in self.productions[A]:
                new_rule = []
                for symbol in rule:
                    if symbol in self.terminals and len(rule) > 1:
                        if symbol not in terminal_map:
                            new_var = self._get_new_variable()
                            terminal_map[symbol] = new_var
                            self.productions[new_var] = [[symbol]]
                        new_rule.append(terminal_map[symbol])
                    else:
                        new_rule.append(symbol)
                new_rules.append(new_rule)
            self.productions[A] = new_rules

        # Step 2: Convert long rules to binary rules
        updated = defaultdict(list)
        for A in self.productions:
            for rule in self.productions[A]:
                while len(rule) > 2:
                    B, C = rule[0], rule[1]
                    new_var = self._get_new_variable()
                    updated[new_var].append([B, C])
                    rule = [new_var] + rule[2:]
                updated[A].append(rule)
        self.productions = updated

    def get_grammar(self):
        return self.variables, self.terminals, self.productions, self.start_symbol

    def print_grammar(self):
        print("Productions in CNF:")
        for A in sorted(self.productions):
            for rule in self.productions[A]:
                print(f"{A} → {' '.join(rule)}")


# Input grammar (from your description)
VN = {'S', 'A', 'B', 'C', 'E'}
VT = {'a', 'b'}
P = [
    ('S', ['a', 'B']),
    ('S', ['A', 'C']),
    ('A', ['a']),
    ('A', ['A', 'C', 'S', 'C']),
    ('A', ['B', 'C']),
    ('B', ['b']),
    ('B', ['a', 'A']),
    ('C', ['ε']),
    ('C', ['B', 'A']),
    ('E', ['b', 'B']),
]
S = 'S'

converter = CFGtoCNFConverter(VN, VT, P, S)
converter.remove_epsilon_productions()
converter.remove_unit_productions()
converter.remove_non_productive_symbols()
converter.remove_inaccessible_symbols()
converter.convert_to_cnf()
converter.print_grammar()
