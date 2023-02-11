import argparse
import os

opcodes = {
    'nop': 0b0000,
    'lda': 0b0001,
    'add': 0b0010,
    'sub': 0b0011,
    'out': 0b0100,
    'sta': 0b0101,
    'ldi': 0b0110,
    'jmp': 0b0111,
    'jc':  0b1000,
    'jz':  0b1001,
    'jnz': 0b1010,
    'hlt': 0b1111
}


class AssemblySyntaxError(Exception):
    pass


def assemble(input_file_name, bytes_file_name=None):
    with open(input_file_name, "r") as input_file:
        asm = input_file.read()
        lines = asm.split('\n')

        tokens = list()
        labels = dict()
        num_data_labels = 0

        for line in lines:
            line = line.split(';', 1)[0].strip().lower()

            if len(line) == 0:
                continue

            if ':' in line:
                label = line.split(':', 1)
                name = label[0].strip()
                value = label[1].strip()
                if len(value) > 0:
                    if 'db' in value:
                        value = value.split('db')[1].strip()
                        labels.update({name: {"value": value, "loc": num_data_labels}})
                        num_data_labels += 1
                    else:
                        raise AssemblySyntaxError('label values must include a db (define byte) expression')
                elif len(name) > 0:
                    labels.update({name: {"value": len(tokens), "loc": None}})
                else:
                    raise AssemblySyntaxError('label must have a valid name')

            else:
                instruction = line.split(' ', 1)

                opcode = instruction[0]
                operand = instruction[1] if len(instruction) > 1 else None

                tokens.append({"opcode": opcode, "operand": operand})

        byte_array = [0] * (len(tokens) + num_data_labels)

        if len(byte_array) > 16:
            raise AssemblySyntaxError(f'Code is {len(byte_array) - 16} bytes too large')

        for i, token in enumerate(tokens):
            byte = opcodes[token["opcode"]] << 4
            if token["operand"] in labels.keys():
                if labels[token["operand"]]["loc"] is None:
                    byte += labels[token["operand"]]["value"]
                else:
                    byte += len(tokens) + labels[token["operand"]]["loc"]
            elif token["operand"] is not None:
                if token["operand"].isdigit() and int(token["operand"]) >= 16:
                    raise AssemblySyntaxError('immediate values must be less than 16')
                byte += int(token["operand"])
            byte_array[i] = byte

        for key in labels.keys():
            if labels[key]["loc"] is not None:
                if int(labels[key]["value"]) > 255:
                    raise AssemblySyntaxError('data values must be less than 255')
                byte_array[labels[key]["loc"]+len(tokens)] = int(labels[key]["value"])

        output = bytearray(byte_array)

    if bytes_file_name is not None:
        if not os.path.isdir("bin"):
            os.makedirs("bin")
        with open(f'bin/{bytes_file_name}', "wb") as bytes_file:
            bytes_file.write(output)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='sap_1_extended_assembler',
        description='SAP-1 extended Assembler',
    )
    parser.add_argument('-i', '--input-file', type=str, default=None, help='Input file name')
    parser.add_argument('-o', '--bytes-file', type=str, default=None, help='bytes file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print bytes to terminal')

    args = parser.parse_args()

    bytecode = assemble(args.input_file, args.bytes_file)
    if args.verbose:
        print(f'bytes: {bytecode.hex(" ")}')
