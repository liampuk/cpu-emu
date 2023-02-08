import argparse
import os

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


def assemble(input_file_name, bytes_file_name=None):

    with open(input_file_name, "r") as input_file:
        asm = input_file.read()
        lines = asm.split('\n')

        tokens = list()
        labels = dict()

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

        byte_array = [0] * (len(tokens) + len(labels))

        for i, token in enumerate(tokens):
            byte = opcodes[token["opcode"]] << 4
            if token["operand"] in labels.keys():
                byte += len(tokens) + labels[token["operand"]]["loc"]
            byte_array[i] = byte

        for key in labels.keys():
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
        prog='sap_1_assembler',
        description='SAP-1 Assembler',
    )
    parser.add_argument('-i', '--input-file', type=str, default=None, help='Input file name')
    parser.add_argument('-o', '--bytes-file', type=str, default=None, help='bytes file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print bytes to terminal')

    args = parser.parse_args()

    bytecode = assemble(args.input_file, args.bytes_file)
    if args.verbose:
        print(f'bytes: {bytecode.hex(" ")}')
