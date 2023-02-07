import operator

opcodes = {
    'nop': 0b0000,
    'lda': 0b0001,
    'add': 0b0010,
    'sub': 0b0011,
    'out': 0b0100,
    'hlt': 0b1111
}


class InvalidAssemblyException(Exception):
    pass


if __name__ == '__main__':
    with open("programs/calculator.asm") as asm_file:
        asm = asm_file.read()
        lines = asm.split('\n')

        tokens = list()
        labels = dict()

        output: str = ''

        for line in lines:
            line = line.split(';', 1)[0].strip().lower()

            if len(line) == 0:
                continue

            if ':' in line:
                label = line.split(':', 1)
                name = label[0].strip()
                value = label[1].strip()
                if 'db' in value:
                    value = value.split('db')[1].strip()
                else:
                    raise InvalidAssemblyException('label values must include a db (define byte) expression')
                labels.update({name: {"value": value, "loc": len(labels)}})

            else:
                instruction = line.split(' ', 1)

                opcode = instruction[0]
                operand = instruction[1] if len(instruction) > 1 else None

                tokens.append({"opcode": opcode, "operand": operand})

        for token in tokens:
            output += f'{opcodes[token["opcode"]]:04b}'
            if token["operand"] in labels.keys():
                output += f'{len(tokens) + labels[token["operand"]]["loc"]:04b}'
            else:
                output += f'{0:04b}'

        data = [''] * len(labels)

        for key in labels.keys():
            data[labels[key]["loc"]] = labels[key]["value"]

        output += ''.join(f'{int(d):08b}' for d in data)

        print(output)



