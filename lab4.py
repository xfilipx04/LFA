import random

def parse_regex(pattern):
    """Parse the regex into a structured format."""
    i = 0
    parsed = []
    while i < len(pattern):
        char = pattern[i]
        if char == '(':
            # Handle alternation groups (a|b|c)
            end = pattern.find(')', i)
            options = pattern[i + 1:end].split('|')
            parsed.append(('group', options))
            i = end
        elif char == '^':
            # Handle repetitions (X^+), (X^*), (X^n)
            if pattern[i + 1] == '+':
                parsed[-1] = ('repeat', parsed[-1], 1, 3)  # At least 1, max 3
                i += 1
            elif pattern[i + 1] == '*':
                parsed[-1] = ('repeat', parsed[-1], 0, 3)  # 0 to 3
                i += 1
            elif pattern[i + 1].isdigit():
                end = i + 2
                while end < len(pattern) and pattern[end].isdigit():
                    end += 1
                count = int(pattern[i + 1:end])
                parsed[-1] = ('repeat', parsed[-1], count, count)
                i = end - 1
        elif char == '[':
            # Handle alternation groups [abc]
            end = pattern.find(']', i)
            options = list(pattern[i + 1:end])
            parsed.append(('group', options))
            i = end
        elif char == '{':
            # Handle explicit repetitions {min,max}
            end = pattern.find('}', i)
            min_max = pattern[i + 1:end].split(',')
            min_count = int(min_max[0])
            max_count = int(min_max[1]) if len(min_max) > 1 else min_count
            parsed[-1] = ('repeat', parsed[-1], min_count, max_count)
            i = end
        elif char == '?':
            # Handle optional quantifier (X?)
            parsed[-1] = ('repeat', parsed[-1], 0, 1)  # Zero or one occurrence
        else:
            # Handle regular characters
            parsed.append(('char', char))
        i += 1
    return parsed

def generate_from_parsed(parsed):
    """Generate a string from the parsed regex structure."""
    result = []
    for token in parsed:
        if token[0] == 'char':
            result.append(token[1])
        elif token[0] == 'group':
            result.append(random.choice(token[1]))
        elif token[0] == 'repeat':
            _, sub_token, min_count, max_count = token
            count = random.randint(min_count, max_count)
            for _ in range(count):
                result.append(generate_from_parsed([sub_token]))
    return ''.join(result)

def generate_from_regex(pattern, num_samples=10):
    """Generate multiple strings from a regex."""
    parsed = parse_regex(pattern)
    return [generate_from_parsed(parsed) for _ in range(num_samples)]

# Variant 1
regexes = [
    "(a|b)(c|d)E^+G?", 
    "P(Q|R|S)T(UV|W|X)^*Z^+", 
    "1(0|1)^*2(3|4)^5 36"  
]

# Generate valid strings
for regex in regexes:
    print(f"Regex: {regex}")
    print(generate_from_regex(regex))
    print("-")