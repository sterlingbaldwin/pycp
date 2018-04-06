import os
import sys
import logging
import argparse
from glob import glob
from tqdm import tqdm
from subprocess import Popen, PIPE

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        nargs='+',
        help='Path to input files')
    parser.add_argument(
        'output',
        help='Path to output directory where the files should be copied to')
    parser.add_argument(
        '-n',
        '--no-clobber',
        action='store_true',
        help='Dont overwrite exiting files')
    parser.add_argument(
        '-m',
        '--move',
        action='store_true',    
        help='Move files instead of copy')
    args = parser.parse_args()
    if not args.input or not args.output:
        parser.print_help()
        sys.exit()
    else:
        log_path = os.path.join(os.getcwd(), 'pycp.log')
        logging.basicConfig(
            format='%(asctime)s:%(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=log_path,
            filemode='w',
            level=logging.DEBUG)
        mode = 'move' if args.move else 'copy'
        no_clobber = True if args.no_clobber else False
        return args.input, os.path.abspath(args.output), mode, no_clobber

def copy(input_files_path, out_path, mode, no_clobber):
    if mode == 'copy':
        cmd_prefix = ['cp']
    elif mode == 'move':
        cmd_prefix = ['mv']
    if no_clobber:
        cmd_prefix.append('-n')
    for inpath in tqdm(input_files_path):
        _, tail = os.path.split(inpath)
        cmd = cmd_prefix + [os.path.abspath(inpath), os.path.join(out_path, tail)]
        msg = 'running command {}'.format(cmd)
        logging.info(msg)
        _, err = Popen(cmd, stdin=PIPE, stderr=PIPE).communicate()
        if err:
            print err
            logging.error(err)
            return 1
    return 0

if __name__ == "__main__":
    input_files_path, out_path, mode, no_clobber = init()
    ret = copy(input_files_path, out_path, mode, no_clobber)
    sys.exit(ret)
