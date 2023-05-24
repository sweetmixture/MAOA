import json,os,sys

target_paths = []

target_paths.append('/Users/woongkyujee/Desktop/PAX_VVUQ/Meeting2/collation/example/PbO_N2_sig01_set1.txt')
target_paths.append('/Users/woongkyujee/Desktop/PAX_VVUQ/Meeting2/collation/example/PbO_N2_sig01_set2.txt')

data = [ [] for i in range(len(target_paths)) ]

for i,item in enumerate(target_paths):

	try:
		with open(item,'r') as f:
			for line in f:
				tmp = json.loads(line)
				data[i].append(tmp)

	except FileNotFoundError as e:
		print(e)

'''
for i,(itemA,itemB) in enumerate(zip(data[0],data[1])):
	print(itemA['run'],itemB['run'])
'''

#print(len(data[0]),len(data[1]))

for item in data[1]:
	item['run'] = item['run'] + 1000

for itemA,itemB in zip(data[0],data[1]):
	print(itemA['run'],itemB['run'])

with open('testing_merge.json','w') as f:

	for line in data[0]:
		f.write(json.dumps(line) + '\n')

	for line in data[1]:
		f.write(json.dumps(line) + '\n')

'''
'''
merged_data = data[0] + data[1]
cpu_tag_sorted = sorted(merged_data, key=lambda x: x['uq_cpu_tag'])

with open('testing_sorted_cputag.json','w') as f:

	for line in cpu_tag_sorted:
		f.write(json.dumps(line) + '\n')





