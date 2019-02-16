from conversions import PDODecoder
from pathlib import Path
from string import Template
import sys

def main():
    if len(sys.argv) < 2:
        print('No input file')
        sys.exit(-1)
    file_in = Path(sys.argv[1])
    file_out = Path('decoded.out')
    decoder = PDODecoder()

    with open(file_in, 'r') as input:
        with open(file_out, 'w+') as output:
            for line in input:
                if line.startswith('***'):
                    continue
                fields = line.split(' ')
                # Keep timestamp as it is
                output.write(fields[0])
                id = '0' + fields[3][2:]
                data = ''.join(fields[6:-1])
                message = decoder.decode_pdo(int(id, 16), bytes.fromhex(data))
                if message:
                    output.write(' ')
                    output.write(str(message))
                else:
                    output.write(' ')
                    output.write(id)
                    output.write(' ')
                    output.write(data)
                    output.write(' ')
                    output.write('Not implemented')
                output.write('\n')
    print(Template('Prosecced $total items, $ok ok and $fail failed').substitute(total=decoder.ok_parses()+decoder.fail_parses(), ok=decoder.ok_parses(), fail=decoder.fail_parses()))
                
if __name__=="__main__":
    main()