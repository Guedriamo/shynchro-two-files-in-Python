import os
import hashlib
import time

import argparse

#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--src", help="Source folder")
parser.add_argument("--dst", help="Replica folder")
parser.add_argument("--interval", help="Synchronization interval (in seconds)")
parser.add_argument("--log", help="Log file path")
args = parser.parse_args()

# Synchronization
while True:
    # iterate over all files
    for file in os.listdir(args.src):
        # compute the MD5 hash
        h = hashlib.md5(open(os.path.join(args.src, file), 'rb').read()).hexdigest()
        # log the file name,MD5 hash
        if os.path.exists(os.path.join(args.dst, file)):
            # check if the file is in the replica
            if h != hashlib.md5(

            if h != hashlib.md5(open(os.path.join(args.dst, file), 'rb').read()).hexdigest():
                # if the file is different, copy the file from the source folder to the replica folder
                output = "Copying {} from {} to {}".format(file, args.src, args.dst)
                print(output)
                with open(args.log, 'a') as log_file:
                    log_file.write(output + "\n")
                os.system("cp {} {}".format(os.path.join(args.src, file), args.dst))
        else:
            # if the file is not in the replica folder, copy the file from source to replica
            output = "Creating {} in {}".format(file, args.dst)
            print(output)
            with open(args.log, 'a') as log_file:
                log_file.write(output + "\n")
            os.system("cp {} {}".format(os.path.join(args.src, file), args.dst))
    # iterate over all files in replica
    for file in os.listdir(args.dst):
        # check if the file is in the source folder
        if not os.path.exists(os.path.join(args.src, file)):
            # if the file is not in the source folder, delete it from the replica folder
            output = "Removing {} from {}".format(file, args.dst)
            print(output)
            with open(args.log, 'a') as log_file:
                log_file.write(output + "\n")
            os.system("rm {}".format(os.path.join(args.dst, file)))
    # wait for the next synchronization
    time.sleep(int(args.interval))