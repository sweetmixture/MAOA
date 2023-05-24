import os,json,sys
import ParsingSupport as ps

from AppOutputExtractor.FHIaims.FHIaimsOutputExtractor import extractor
from AppOutputExtractor.FHIaims.FHIaimsMolecule import molecule as fmol
from AppOutputExtractor.FHIaims.FHIaimsMolecule import calculate_rmsd_molecules


# LOADING APP DIRS
root = os.getcwd()
dirs = [ d for d in os.listdir('./') if 'run_' in d ]
dirs = sorted(dirs,key=lambda x: int(x.split('_')[1]))
for i,item in enumerate(dirs):
	dirs[i] = os.path.join(root,item)

# LOADING VVUQ JOBS REPORT
vvuq_log_path = root + '/jobs.report'
vvuq_log = []

try:
	with open(vvuq_log_path,'r') as f:
		for line in f:
			data = json.loads(line)
			vvuq_log.append(data)
except FileNotFoundError as e:
	print(e,'vvuq report file is not found')

vvuq_log = sorted(vvuq_log, key=lambda x: int(x['name']))	# sorted by 'name' (eq. run_# id)

# test
#name = vvuq_log[0]['name']
#rtime= vvuq_log[0]['runtime']['rtime']
#print(name,rtime,ps.time_to_seconds(rtime))

# sorting again w.r.t used cores
#vvuq_log = sorted(vvuq_log, key=lambda x: x['runtime']['allocation'])
#for item in vvuq_log:
#	print(item)

# LOADING SAMPLING STRUCTURE
sampling_fmol = fmol(root + '/sampling.geometry.in')
#sampling_fmol.show_info()

# main loop - looping directories
ex = extractor()	# FHIaims Output AnalysisTool

'''
	Manual Settings
'''
# Species Energy - intermediate_20
species = {}
species['Ba'] = -225147.479227887
species['O']  = -2041.708288962
species['Pb'] = -590155.339286187
species['Sn'] = -170362.550711674
species['Sr'] = -87201.125124913

onsite_e = 0.
atomlist = sampling_fmol.get_atomlist()

# onsite energy 
for item in atomlist:
	onsite_e = onsite_e + species[item.get_type()]

# for writing later
output = []

for i, (item,uq_log) in enumerate(zip(dirs,vvuq_log)):

	#code = item.split('run_')[1]
	#print(code,uq_log['name'])
	#sys.exit(1)

	# set target paths
	run_dir = item
	app_output = item + '/FHIaims.out'
	app_geometry_in = item + '/geometry.in'
	app_geometry_out= item + '/geometry.in.next_step'

	# set target paths to 'Extractor'
	ex.set_output_filepath(app_output)
	ex.set_input_geometry_filepath(app_geometry_in)
	ex.set_output_geometry_filepath(app_geometry_out)

	# check target files
	if None in ex.check_filepaths():
		coll_if_paths = False
	else:
		coll_if_paths = True
	# app run 'success' check
	coll_if_success = ex.check_calculation_success()

	coll_tag = i+1
	coll_tmp = {}

	# collation run info
	coll_tmp['run'] = coll_tag
	coll_tmp['filepaths'] = ex.check_filepaths()
	coll_tmp['success'] = ex.check_calculation_success()
	coll_tmp['ptasks'] = ex.check_parallel_task()

	if coll_tmp['success']:
		coll_tmp['app_rtime'] = float(ex.check_calculation_runtime())
	else:
		coll_tmp['app_rtime'] = None

	# collation from vvuq_log
	coll_tmp['uq_run']     = uq_log['name'] 
	coll_tmp['uq_cpu_tag'] = uq_log['runtime']['allocation'].split('[')[1].split(']')[0]
	coll_tmp['uq_rtime']   = float(ps.time_to_seconds(uq_log['runtime']['rtime']))
	
	# collation overhead
	if coll_tmp['success']:
		coll_tmp['overhead'] = coll_tmp['uq_rtime'] - coll_tmp['app_rtime']
	else:
		coll_tmp['overhaed'] = None

	# collation PhysData
	coll_tmp['phys_data'] = {}

	if coll_tmp['filepaths'][0] != None and coll_tmp['success'] == True:
		ex.set_scf_blocks()	# setting scf blocks
		coll_tmp['phys_data']['init_e'] = ex.get_total_energy(0) - onsite_e
		coll_tmp['phys_data']['fina_e'] = ex.get_total_energy( ) - onsite_e
		coll_tmp['phys_data']['init_dipole'] = ex.get_dipole(0)
		coll_tmp['phys_data']['fina_dipole'] = ex.get_dipole( )
		coll_tmp['phys_data']['init_homolumo'] = ex.get_homolumo(0)
		coll_tmp['phys_data']['fina_homolumo'] = ex.get_homolumo( )
	else:
		coll_tmp['phys_data']['init_e'] = None
		coll_tmp['phys_data']['fina_e'] = None
		coll_tmp['phys_data']['init_dipole'] = None
		coll_tmp['phys_data']['fina_dipole'] = None
		coll_tmp['phys_data']['init_homolumo'] = None
		coll_tmp['phys_data']['fina_homolumo'] = None

	# collation Geometry
	coll_tmp['geometry'] = {}

	if coll_tmp['filepaths'][1] != None:
		coll_tmp['geometry']['init_rmsd'] = calculate_rmsd_molecules(ex.input_geometry,sampling_fmol)
	else:
		coll_tmp['geometry']['init_rmsd'] = None

	if coll_tmp['filepaths'][2] != None:
		coll_tmp['geometry']['fina_rmsd'] = calculate_rmsd_molecules(ex.output_geometry,sampling_fmol)
	else:
		coll_tmp['geometry']['fina_rmsd'] = None


	# finalise set collation
	output.append(coll_tmp)

	#print('\rretrieving run_id: {} - success: {}'.format(coll_tmp['run'],coll_tmp['success']),end='')
	#print('retrieving run_id: {} - success: {}'.format(coll_tmp['run'],coll_tmp['success']))


# summarise
with open('{}'.format(sys.argv[1]),'w') as f:

	for line in output:
		f.write(json.dumps(line) + '\n')

