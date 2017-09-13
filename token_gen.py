#!/usr/local/bin/python3
import xlrd as exc
import csv
import argparse
import str_token_gen as s
import reverse_token_gen as r
from abbv import abbvtool
import collections
import flattenlist as fl
def parse_args():
	parser=argparse.ArgumentParser( description ='supply file that need to be parsed')
	parser.add_argument('--filename',required=True)
	parser.add_argument('--outputname',required=True)
	return parser.parse_args()


def csvconvert(filename,outputname):
	workbook = exc.open_workbook(filename)
	intial_li=[]
	fieldnames = ['sheetname', 'parentObject', 'label','tag','value','context','acronym','pre','post']
	for i in workbook.sheet_names():
		processing_sheet=i
		worksheet = workbook.sheet_by_name(processing_sheet)
		for j in range(2, worksheet.nrows):
			acronym=abbvtool(worksheet.cell_value(j,3))
			txt_val = worksheet.cell_value(j,4)
			label = worksheet.cell_value(j,3)
			prefix=''
			suffix=''
			try:
				if label.upper() in txt_val.upper():
					prefix = txt_val.upper().split(label.upper())[0]
					suffix = txt_val.upper().split(label.upper())[1]
				elif  acronym.upper() in txt_val.upper():
					prefix = txt_val.upper().split(acronym.upper())[0]
					suffix = txt_val.upper().split(acronym.upper())[1]
				else:
					prefix='NA'
					suffix='NA'
			except:
				pass 
			intial_li.append([i]+worksheet.row_values(j)+[acronym]+[prefix]+[suffix]) 
	with open(outputname, "w",encoding='utf-8') as f:
		writer = csv.writer(f,delimiter='~',quotechar ='"',quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(fieldnames)
		writer.writerows(intial_li)
	pre_post_output=[]
	for l in intial_li:
		if 'DATA' in l[3].upper() and 'NA' not in l:
			reversed(r.reverse_lemma(l[-2]))
			#print( [l[5]]+r.reverse_lemma(l[-2])+['target'] +s.lemma(l[-1]))
			pre_post_ls=r.reverse_lemma(l[-2]) +s.lemma(l[-1])
			pre_post_output=pre_post_ls +pre_post_output
		
	counter=collections.Counter(pre_post_output)
	print(counter.most_common(1000))
	return intial_li


def main():
	args = parse_args()
	csvconvert(args.filename,args.outputname)


if __name__ == "__main__":
	main()	
