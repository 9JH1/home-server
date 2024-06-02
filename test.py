import os,shutil




def get_full_size():
    return shutil.disk_usage("/").free
def get_size_of_dir(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return int(total_size)
def get_free():
    return get_full_size() - get_size_of_dir(".")/1e+9