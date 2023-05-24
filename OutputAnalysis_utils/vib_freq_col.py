import os,sys,csv,json
#import numpy as np
from ShellCommand import shellcommand as shell
import ParsingSupport as ps

from AppOutputExtractor.FHIaims.FHIaimsOutputExtractor import extractor
from AppOutputExtractor.FHIaims.FHIaimsMolecule import molecule as fmol
from AppOutputExtractor.FHIaims.FHIaimsMolecule import calculate_rmsd_molecules
from ShellCommand import shellcommand as shell

# Target Files
dirs = [ d for d in os.listdir('./') if 'run_' in d ]
dirs = sorted(dirs,key=lambda x: int(x.split('_')[1]))

root = os.getcwd()
target = 'std.out'
number_of_modes = 12
output = []

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

vvuq_log = sorted(vvuq_log, key=lambda x: int(x['name']))       # sorted by 'name' (eq. run_# id)

###
# Collation for the central point calculations
# Species Energy - intermediate_20
species = {}
species['Ba'] = -225147.479227887
species['O']  = -2041.708288962
species['Pb'] = -590155.339286187
species['Sn'] = -170362.550711674
species['Sr'] = -87201.125124913
ex = extractor()
sampling_fmol = fmol(root + '/sampling.geometry.in')
atomlist = sampling_fmol.get_atomlist()
# onsite energy 
onsite_e = 0.
for item in atomlist:
	onsite_e = onsite_e + species[item.get_type()]

###
# shell
sh = shell()

for i,item in enumerate(dirs):
	
	dirs[i] = os.path.join(root,item)
	directory = dirs[i]
	dirs[i] = os.path.join(dirs[i],target)

	uq_log = vvuq_log[i]

	coll = {}
	vib_out = []
	coll_tag = i+1

	try:
		with open(dirs[i],'r') as f:
		
			for line in f:
				vib_out.append(line)

		coll['run'] = coll_tag

		for offset, line in enumerate(vib_out):
			if 'finite difference calculation based on delta' in line:
				ls = line.split()
				coll['delta'] = float(ls[7])

			if 'Mode number' in line:
				mode_block = vib_out[offset+1:offset+1 + number_of_modes]
			

		coll['mode'] = {}

		for offset, line in enumerate(mode_block):
			ls = line.split()
			coll['mode'][ls[0]] = [ float(ls[1]), float(ls[2]), float(ls[3]) ]
			# feq (cm-1)/ zpe (eV)/ ir-intensity (D^2/Angs^2)
			

		coll['uq_run'] = uq_log['name']
		coll['uq_cpu_tag'] = uq_log['runtime']['allocation'].split('[')[1].split(']')[0]
		coll['uq_rtime'] = float(ps.time_to_seconds(uq_log['runtime']['rtime']))

		#print(coll)
		# finalise set collation
		output.append(coll)

	except FileNotFoundError as e:
		print(e)
	

	#### 
	central_out = 'fhivib.central.out'
	target_central = os.path.join(directory,central_out)

	# set target paths
	run_dir = directory
	#app_output = directory + '/FHIaims.out'
	app_output = os.path.join(directory,central_out)
	app_geometry_in = directory + '/geometry.in'			# input geometry
	app_geometry_out= directory + '/geometry.in.next_step'		# output geometry - possibly not necessary ...
	
	# set target paths to 'Extractor'
	ex.set_output_filepath(app_output)
	ex.set_input_geometry_filepath(app_geometry_in)
	ex.set_output_geometry_filepath(app_geometry_out)

	try:
		with open(target_central,'r') as f:

			# collation run info
			coll['run'] = coll_tag
			coll['filepaths'] = ex.check_filepaths()
			coll['success'] = ex.check_calculation_success()
			coll['ptasks'] = ex.check_parallel_task()

			coll['phys_data'] = {}
			ex.set_scf_blocks()

			coll['phys_data']['init_e'] = ex.get_total_energy(0) - onsite_e
			coll['phys_data']['fina_e'] = ex.get_total_energy( ) - onsite_e
			coll['phys_data']['init_dipole'] = ex.get_dipole(0)
			coll['phys_data']['fina_dipole'] = ex.get_dipole( )
			coll['phys_data']['init_homolumo'] = ex.get_homolumo(0)
			coll['phys_data']['fina_homolumo'] = ex.get_homolumo( )

			#print(coll['phys_data']['init_e'])
			#print(coll['phys_data']['fina_e'])
			#print(coll['phys_data']['init_dipole'])
			#print(coll['phys_data']['fina_dipole'])
			#print(coll['phys_data']['init_homolumo'])
			#print(coll['phys_data']['fina_homolumo'])

			# collation Geometry
			coll['geometry'] = {}
			if coll['filepaths'][1] != None:
				coll['geometry']['init_rmsd'] = calculate_rmsd_molecules(ex.input_geometry,sampling_fmol)
			else:
				coll['geometry']['init_rmsd'] = None
			if coll['filepaths'][2] != None:
				coll['geometry']['fina_rmsd'] = calculate_rmsd_molecules(ex.output_geometry,sampling_fmol)
			else:
				coll['geometry']['fina_rmsd'] = None


			#print(coll['geometry']['init_rmsd'])
			#print(coll['geometry']['fina_rmsd'])

	except FileNotFoundError as e:
		print(e)

	#print(coll)
	#sys.exit(1)




# summarise
with open('{}'.format(sys.argv[1]),'w') as f:
        for line in output:
                f.write(json.dumps(line) + '\n')
