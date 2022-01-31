import sys
import pathlib
import re
import shutil

if __name__ == "__main__":

    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python no_binaries_in_staging_area.py <path>")
        exit()

    # check if file exists
    path = sys.argv[1]

    if not pathlib.Path(path).is_dir():
        print("Dir does not exist")
        exit()

    # check if path is git repo
    if not pathlib.Path(path + "/.git").is_dir():
        print("Not a git repo")
        exit()

    # get list of files in staging area with pathlib
    staging_area = path + "/.git/info/sparse-checkout"
    files = []
    for file in pathlib.Path(staging_area).iterdir():
        files.append(file)

    # check if there are any binaries in staging area
    # binaries include: executables, shared libraries, static libraries, object files, archives, images, and unknown files
    binaries = []
    for file in files:
        if re.search(r"\.(exe|dll|so|a|o|ar|img|bin|unknown)$", file.name):
            binaries.append(file)

    # if there are binaries in staging area, move them to .git/info/sparse-checkout/binaries
    if len(binaries) > 0:
        binaries_dir = path + "/.git/info/sparse-checkout/binaries"
        if not pathlib.Path(binaries_dir).is_dir():
            pathlib.Path(binaries_dir).mkdir(parents=True, exist_ok=True)
        for binary in binaries:
            shutil.move(binary, binaries_dir)
        print(f"Moved {len(binaries)} binaries to {binaries_dir}")
    else:
        print("No binaries in staging area")
        exit()

    # remove .git/info/sparse-checkout/binaries if empty
    if not pathlib.Path(binaries_dir).is_dir():
        shutil.rmtree(binaries_dir)
