import argparse
import os

opcodes = {
    'NOP': 0x00,
    'HLT': 0x01,
    'LDI': 0x02,
    'LDA': 0x03,
    'STA': 0x04,
    'STM': 0x05,
    'ADI': 0x06,
    'ADD': 0x07,
    'SUI': 0x08,
    'SUB': 0x09,
    'CMI': 0x0A,
    'CMP': 0x0B,
    # 0x0C
    # 0x0D
    # 0x0E
    # 0x0F
    'JMP': 0x10,
    'JC': 0x11,
    'JZ': 0x12,
    'JNZ': 0x13,
    'PAGE0': 0x14,
    'PAGE1': 0x15,
    'RESET': 0x16,
    # 0x17
    'OUTA': 0x18,
    'OUTB': 0x19,
    'OUTC': 0x1A,
    'OUTD': 0x1B,
    'OUTE': 0x1C,
    'OUTF': 0x1D,
    'INA': 0x1E,
    'INB': 0x1F
}


class AssemblySyntaxError(Exception):
    pass


def assemble(input_file_name, output_file_name=None):
    with open(input_file_name, "r") as input_file:
        asm = input_file.read()
        lines = asm.split('\n')
        sanitised_lines = []
        for line in lines:
            line = line.split(';', 1)[0].upper()
            line = line.replace('DB', '')
            if 'ORG' in line:
                line = f"{line.split('ORG', 1)[1].strip()}:"
            if ':' in line:
                sanitised_lines.append(f"{line.split(':', 1)[0]}:".strip())
                sanitised_lines.append(line.split(':', 1)[1].strip())
            else:
                line = line.strip()
                if ' ' in line:
                    sanitised_lines.append(line.split(' ', 1)[0].strip().upper())
                    sanitised_lines.append(line.split(' ', 1)[1].strip().upper())
                else:
                    sanitised_lines.append(line.upper())

        lines_filter_blank = list(filter(lambda l: len(l) > 0, sanitised_lines))

        j = 0
        labels_as_indexes = []
        labels = dict()

        for line in lines_filter_blank:
            if ':' in line:
                label = line.split(':', 1)[0]
                if label.isnumeric():
                    j = int(label)
                    labels_as_indexes.append(line)
                else:
                    labels.update({label: j})
                    labels_as_indexes.append(f"{j}:")
            else:
                labels_as_indexes.append(line)
                j += 1

        print(labels)

        instruction_array: list = [0] * 256
        j = 0

        for line in labels_as_indexes:
            if line in opcodes.keys():
                instruction_array[j] = int(opcodes[line])
                j += 1
            elif line.isnumeric():
                instruction_array[j] = int(line)
                j += 1
            elif line in labels.keys():
                instruction_array[j] = int(labels[line])
                j += 1
            elif ':' in line:
                j = int(line.split(':', 1)[0])

        output_bytes = bytearray(instruction_array)

    if output_file_name is not None:
        if not os.path.isdir("bin"):
            os.makedirs("bin")
        with open(f'bin/{output_file_name}', "wb") as output_file:
            output_file.write(output_bytes)

    return output_bytes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='assembler.py',
        description='SAP-8 Assembler.',
    )
    parser.add_argument('-i', '--input-file', type=str, default=None, help='input file name')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='output file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='print output bytes to terminal')

    args = parser.parse_args()

    bytecode = assemble(args.input_file, args.output_file)
    if args.verbose:
        print('###   START BYTES   ###')
        print_output = bytecode.hex(":", 1)
        for i in range(32):
            print(f'{print_output[(i*23)+i:23+(i*23)+i]}')
        print('###    END BYTES    ###')
