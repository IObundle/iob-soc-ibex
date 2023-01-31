# This script is called during setup.
# You can use 'setup_module' to access the contents of the iob_soc_setup.py python module
import os
import shutil

# Delete all test*.expected files from build_dir
dirpath=os.path.join(setup_module.build_dir, "hardware/simulation/src")
for file in os.listdir(dirpath):
    if file.startswith("test") and file.endswith(".expected"):
        os.remove(os.path.join(dirpath,file))

# Find out correct test.expected filename
test_file_name='test'
#Check if setup with INIT_MEM (check if macro exists)
if next((i for i in setup_module.confs if i['name']=='INIT_MEM'), False) and setup_module.confs['INIT_MEM']['val'] != 'NA':
    test_file_name+='_initmem'
#Check if setup with RUN_EXTMEM (check if macro exists)
if next((i for i in setup_module.confs if i['name']=='RUN_EXTMEM'), False):
    test_file_name+='_extmem'
test_file_name+='.expected'

# Copy correct test.expected file to build dir
shutil.copyfile(os.path.join(setup_module.setup_dir, "hardware/simulation/src", test_file_name),os.path.join(dirpath,"test.expected"))

