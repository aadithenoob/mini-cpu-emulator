memory = [0] * 4096

reg = { 
    "v0": 0,
    "v1": 0,
    "v2": 0,
    "e0": 0,
    "e1": 0,
    "e2": 0
}

flags = {
    "zero": False,
    "greater": False,
    "smaller": False
}

def parse(tokens, operation):
    if operation in reg:
        print(reg[tokens[0]])

    elif operation == "mov":
        dest_reg = tokens[1]
        val = int(tokens[2])
        reg[dest_reg] = val
    elif operation == "cmp":
        r1 = tokens[1]
        r2 = tokens[2]
        flags["zero"] = reg[r1] == reg[r2]
        flags["greater"] = reg[r1] > reg[r2]
        flags["smaller"] = reg[r1] < reg[r2]
    elif operation == "je":
        if flags["zero"]:
            return int(tokens[1])    
    elif operation == "jmp":
        return int(tokens[1])
    elif operation == "st":
        if len(tokens) > 2:
            src_val = tokens[1]
            dest = tokens[2]

            if dest in reg:
                addr = reg[dest]

                if 0 <= addr < len(memory):
                    if src_val in reg:
                        memory[addr] = reg[src_val]
                    else:
                        memory[addr] = int(src_val)
                else:
                    print("segmentation fault: address value out of bounds.")
                    return -1
            else:
                print("error: address value must be in a register.")
        else:
            print("error: invalid number of arguments.")

    elif operation == "ld":
        if len(tokens) > 2:
            dest = tokens[1]
            src = tokens[2]

            if src in reg:
                addr = reg[src]

                if 0 <= addr < len(memory):
                    if dest in reg:
                        reg[dest] = memory[addr]
                    else:
                        print(f"error: invalid register {dest}.")
                else:
                    print("segmentation fault: address value out of bounds.")
                    return -1
            else:
                print("error: address value must be in a register.")
        else:
            print("error: invalid number of arguments.")
                    
    elif operation == "halt":
        return -1
    else:
        alu(operation, tokens)
        
def alu(operation, tokens):
    val1 = reg[tokens[1]]
    val2 = reg[tokens[2]]

    if operation == "add":
        result = val1 + val2
    elif operation == "sub":
        result = val1 - val2
    elif operation == "mul":
        result = val1 * val2
    elif operation == "div":
        result = val1 // val2
    
    reg[tokens[1]] = result
    
    print(result)

ip = 0

while True:
    inp = input('> ')

    if inp.lower() in ("exit", "e"):
        print("Exiting.")
        break

    tokens = inp.split()
    tokens = [x.lower() for x in tokens]

    if tokens[0] == "run":
        ip = 0
        program = []

        file = tokens[1]

        try:
            with open(file, "r") as f:
                for line in f:
                    program.append(line.rstrip('\n'))
        except FileNotFoundError as e:
            print("Error: File not found.")

        while ip < len(program):
            toks = program[ip].split(" ")
            toks = [x.lower() for x in toks]
            operation = toks[0]
            new_ip = parse(toks, operation) 

            if new_ip is None:
                ip += 1
            elif new_ip == -1:
                break
            else:
                ip = new_ip

        continue

    operation = tokens[0]
    result = parse(tokens, operation)
    
    if result == -1:
        break