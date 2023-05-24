import os,sys,json

root = os.getcwd()
tarfile1 = sys.argv[1]
tarfile2 = sys.argv[2]

tarfile1 = os.path.join(root,tarfile1)
tarfile2 = os.path.join(root,tarfile2)

# set 1
data_set1 = []
try:
	with open(tarfile1,'r') as f:
		for line in f:
			tmp = json.loads(line)
			data_set1.append(tmp)
except FileNotFoundError as e:
	print(e)

# set 2
data_set2 = []
try:
	with open(tarfile2,'r') as f:
		for line in f:
			tmp = json.loads(line)
			data_set2.append(tmp)
except FileNotFoundError as e:
	print(e)


offset = len(data_set2)
for item in data_set2:
	item['run'] = item['run'] + offset

merged_data = data_set1 + data_set2

try:
	if sys.argv[3] == 'cpu_tag_sort':
		final_data = sorted(merged_data, key=lambda x: x['uq_cpu_tag'])

	else:
		pass
except:
	final_data = merged_data

with open('merged.txt','w') as f:
        for line in final_data:
                f.write(json.dumps(line) + '\n')

