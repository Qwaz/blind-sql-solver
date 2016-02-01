import argparse
import codecs
import sys

parser = argparse.ArgumentParser(description='String Unescape')

sys.stdout.write(codecs.decode(sys.stdin.read(), 'unicode_escape'))

