reg = { 
    "v0": 0,
    "v1": 0,
    "v2": 0
}

def parse(tokens):
    if operation == "mov":
        dest_reg = tokens[1]
        val = int(tokens[2])

        reg[dest_reg] = val
    else:
        alu(tokens)

def alu(tokens):
    val1 = reg[tokens[1]]
    val2 = reg[tokens[2]]

    if operation == "add":
        result = val1 + val2
    if operation == "sub":
        result = val1 - val2
    if operation == "mul":
        result = val1 * val2
    if operation == "div":
        result = val1 / val2
    
    reg["v2"] = result
    
    print(result)

while True:
    inp = input('> ')

    if inp.lower() == "exit":
        print("Exiting.")
        break

    tokens = inp.split(" ")
    tokens = [x.lower() for x in tokens]

    if tokens[0] == "run":
        ip = 0
        program = []

        file = tokens[1]

        with open(file, "r") as f:
            for line in f:
                program.append(line.rstrip('\n'))

        while ip < len(program):
            toks = program[ip].split(" ")
            toks = [x.lower() for x in toks]
            operation = toks[0]
            parse(toks)
            ip += 1

        continue

    operation = ""
    operation = tokens[0]
    parse(tokens)
