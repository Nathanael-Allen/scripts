import os
from shutil import copy
import pathlib
from sys import argv

cwd = pathlib.Path.cwd()

input_file_path = os.path.join(cwd, argv[1])

input_file_path_object = pathlib.Path(input_file_path)

copy(input_file_path, '/mnt/c/Users/natha/school/finished/')
print("file successfully copied to /mnt/c/Users/natha/school/finished")
