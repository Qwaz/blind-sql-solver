import argparse
import os

parser = argparse.ArgumentParser(description='Shellcode Runner')
parser.add_argument('--output', '-o')
parser.add_argument('shellcode')

args = parser.parse_args()

code = '''int main() {
	char *code = "@@@";
	void (*pointer)(void);
	pointer = (void*)code;
	pointer();
}
'''

code = code.replace('@@@', args.shellcode)

f = open('tmp.c', 'w')
f.write(code)
f.close()

os.system('gcc tmp.c ' + ('-o %s' % args.output if args.output else ''))
os.system('rm tmp.c')
os.system('./' + args.output if args.output else './a.out')
