#!/usr/bin/env python
import argparse
import re
from distutils.util import strtobool
from subprocess import Popen, PIPE

def yes_no_prompt(question):
	print('%s [y/n]' % question)
	while True:
		try:
			return strtobool(raw_input().lower())
		except ValueError:
			print('Please respond with \'y\' or \'n\'.')

parser = argparse.ArgumentParser(description='Shellcode extractor')
parser.add_argument('--begin', default='main')
parser.add_argument('input')

args = parser.parse_args()

process = Popen(["objdump", "-d", args.input], stdout=PIPE)
(output, err) = process.communicate()
output = output.strip()
exit_code = process.wait()

if exit_code != 0:
	print("Error Occurred")
	print(err)
else:
	main_found = False
	result = ''
	for block in re.split(r'\n\n+', output):
		lines = block.split('\n')
		block_heads = re.split(r'[ <>:]+', lines[0])
		if not main_found:
			if len(block_heads) >= 2 and block_heads[1] == args.begin:
				main_found = True
			else:
				continue
		if yes_no_prompt('include '+block_heads[1]+'?'):
			for line in lines[1:]:
				for code in line.split('\t')[1].strip().split():
					if code != '...':
						result += r'\x'+code
		else:
			break
	if r'\x00' in result:
		print(r"WARNING: \x00 exists")
	print(result)
