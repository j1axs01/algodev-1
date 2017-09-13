#!/usr/local/bin/python3

import argparse

def parse_args():
        parser=argparse.ArgumentParser( description ='supply file that need to be parsed')
        parser.add_argument('--string',required=True)
        return parser.parse_args()

def abbvtool(str):
	ac = ''
	try:
		for i in str.split(' '):
			if len(i) > 3 :
				ac = ac+i[0]
	except:
		pass
	return ac.upper()

def main():
        args = parse_args()

if __name__ == "__main__" :
	main()
