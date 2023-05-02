
#from Demo.AppOutputAnalysis.AppOutputExtractor.FHIaims import FHIaimsOutputExtractor as fe

import AppOutputExtractor.FHIaims.FHIaimsOutputExtractor as fe


file_root = '/Users/woongkyujee/Desktop/Python/FHI22_samples/runs/run_1'
main_output = file_root + '/FHIaims.out'
input_geo   = file_root + '/geometry.in'
output_geo  = file_root + '/geometry.in.next_step'

te = fe.extractor()
te.set_output_filepath(main_output)
te.set_input_geometry_filepath(input_geo)
te.set_output_geometry_filepath(output_geo)

print(te.check_filepaths())

te.set_scf_blocks()

init_e = te.get_total_energy(0)
print(init_e)
fina_e = te.get_total_energy()
print(fina_e)

fina_hl = te.get_homolumo()
print(fina_hl)

te.output_geometry.show_info()


#def collect_all(aimsExtractor):
#
#	finalE = aimsExtractor.get_total_energy()
#	homolumo = aimsExtractor.get_homolumo()
#
#	return {'energy':finalE,'homolumo':homolumo}
#
#target = collect_all(te)
#print(target)
