import click
from pathlib import Path
import os
import shutil
import hashlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map             #concurrency
from itertools import repeat
import humanize
import json
from collections import Counter
from send2trash import send2trash
from time import perf_counter
from math import ceil

# from concurrent.futures import ProcessPoolExecutor

@click.group()
@click.version_option()
def cli() -> None:
    '''
    A simple program to find and remove duplciate files.
    '''
    pass

def get_hash(path: str, hash: str) -> str:
    with open(path, 'rb') as f:
        digest = hashlib.file_digest(f, hash)
    return digest.hexdigest(), path

@cli.command()
@click.argument('path', type = click.STRING)
@click.argument('hash', type = click.STRING)
@click.option('--depth_lowest', '-d', is_flag = True, help = 'keep the file with the lowest pathway depth')
@click.option('--depth_highest', '-D', is_flag = True, help = 'keep the file with the highest pathway depth')
@click.option('--shortest_name', '-s', is_flag = True, help = 'keep the file with the shortest name')
@click.option('--longest_name', '-S', is_flag = True, help = 'keep the file with the longest name')
@click.option('--created_oldest', '-c', is_flag = True, help = 'keep the file with the oldest creation date')
@click.option('--created_newest', '-C', is_flag = True, help = 'keep the file with the newest creation date')
@click.option('--modified_oldest', '-m', is_flag = True, help = 'keep the file with the oldest modification date')
@click.option('--modified_newest', '-M', is_flag = True, help = 'keep the file with the newest modification date')
@click.option('--number_of_cpus', '-ncpu', type = click.INT, help = 'Maximum number of workers (cpu cores) to use for the scan', default = 0)
@click.option('--chunksize', '-ch', type = click.INT, help = 'chunksize to give to workers, minimum of 2', default = 2)
def scan(path: str, hash: str, depth_lowest: bool, 
                               depth_highest: bool,
                               shortest_name: bool,
                               longest_name: bool,
                               created_oldest: bool,
                               created_newest: bool,
                               modified_oldest: bool,
                               modified_newest: bool,
                               number_of_cpus: int = 0,
                               chunksize: int = 2,) -> None:
    '''
    Scan recursively computes a hash of each file and puts the hash into
    a dictionary.  The keys are the hashes of the files, and the values
    are the file paths and metadata.  If an entry has more than 1 file
    associated, they are duplicates.  The original is determined by the
    flags or options (ex: -d).  The duplicates are added to a file called
    duple.delete.
    '''
    
    start = perf_counter()

    if hash not in hashlib.algorithms_available:
        click.secho(f'Hash must be one of the following: {hashlib.algorithms_available}')
        return

    if number_of_cpus > os.cpu_count():
        click.secho(f'Too many cpus (number_of_cpus too high), only using {os.cpu_count()} cpus')
        number_of_cpus = os.cpu_count()
    
    if number_of_cpus == 0:
        number_of_cpus = int(ceil(os.cpu_count() * 2/3))
    
    if chunksize < 2:
        click.secho(f'chunksize too low, setting to default of 2')
        chunksize = 2

    flags = [depth_lowest,
            depth_highest,
            shortest_name,
            longest_name,
            created_oldest,
            created_newest,
            modified_oldest,
            modified_newest]

    c = Counter(flags)
    if c[True] > 1:
        click.secho('Only one flag can be chosen at a time.')
        return
    
    filelist = list()
    for root, dirs, files in os.walk(path, followlinks=False):
        for file in files:
            if Path(f'{root}/{file}').exists():
                filelist.append(f'{root}/{file}')

    hash_start = perf_counter()
    hashes = process_map(get_hash, filelist, repeat(hash), max_workers = number_of_cpus, chunksize = 2)
    hash_finish = perf_counter()

    p_dict: dict = dict()
    for hash, file_path in hashes:
        if hash not in p_dict.keys():
            p_dict[hash] = list()
        p_dict[hash].append(file_path)

    result = {k: v for k, v in p_dict.items() if len(v) > 1}

    for k, v in result.items():
        stats = dict()
        for file in v:
            stat = Path(file).stat()
            stats[file] = stat
        result[k] = stats    
    
    # compute some statistics and create outputs
    total_size = 0
    file_count = 0
    for k, stats in result.items():
        for file, stat in stats.items():
            file_count += 1
            total_size += stat.st_size
        total_size -= stat.st_size
        file_count -= 1

    with open('duple.json', 'w') as f:
        json.dump(result, f, indent = 4)

    create_remove_list(result, *flags)

    click.secho()
    click.secho(f'Out of {click.style(len(filelist),fg = "green")} files, There are {click.style(file_count, fg = "red")} in {click.style(len(result.keys()), fg = "red")} groups')
    click.secho(f'Duplicates which can be removed: {humanize.naturalsize(total_size)}')
    click.secho()
    click.secho(f"Wrote {click.style('duple.json', fg = 'green')} with results.")
    click.secho(f"Wrote {click.style('duple.delete', fg = 'green')} with file paths to be deleted -> {click.style('`duple rm`', fg = 'green')}.")
    click.secho(f'Total Processing time: {round(perf_counter() - start, 4)} seconds, Hash processing time {round(hash_finish - hash_start,4)} seconds.')

def create_remove_list(scan_result: dict, depth_lowest: bool, 
           depth_highest: bool,
           shortest_name: bool,
           longest_name: bool,
           created_oldest: bool,
           created_newest: bool,
           modified_oldest: bool,
           modified_newest: bool) -> None:

    # define test functions
    def path_depth(path: str) -> int:
        return len(Path(path).parents)
    
    def name_length(path: str) -> int:
        return len(Path(path).name)
    
    def created_date(path: str) -> int:
        return Path(path).stat().st_birthtime
    
    def modified_date(path: str) -> int: 
        return Path(path).stat().st_mtime

    # select the test function based on flag
    options = [(depth_lowest , path_depth, 1),
               (depth_highest , path_depth, -1),
               (shortest_name , name_length, 1),
               (longest_name , name_length, -1),
               (created_oldest ,  created_date, 1),
               (created_newest , created_date, -1),
               (modified_oldest , modified_date, 1),
               (modified_newest , modified_date, -1)]
    
    for flag, function, option in options:
        if flag:
            test_fun = function
            negate = option
    
    delete_files = list()
    for item in scan_result.values():
        keys = list(item.keys())
        seed = test_fun(keys[0])
        result = keys[0]
        for path in item.keys():
            if negate * seed > negate * test_fun(path):
                seed = test_fun(path)
                result = path
        
        keys.remove(result)
        delete_files.extend(keys)
    
    with open('duple.delete', 'w') as f:
        for file in delete_files:
            f.write(f'{file}\n')

@cli.command()
def rm() -> None:
    '''
    rm sends all files specified in duple.delete to the trash folder
    '''

    if not duple_outputs_exist():
        return

    paths = get_delete_paths()
    
    for path in tqdm(paths):
        send2trash(path)

    remove_empty_directories()

@cli.command()
@click.argument('move_to_path', type = click.STRING)
def mv(move_to_path: str) -> None:
    '''
    mv will move all of the files in duple.delete to the specified path
    '''
    
    if not duple_outputs_exist():
        return

    paths = get_delete_paths()
    count = 0
    for path in tqdm(paths):
        if not Path(path).exists():
            click.secho(f'{path} -> does not exists, already deleted or moved')
        else:
            name = Path(path).name
            shutil.move(path, f'{move_to_path}/{name}')
            count += 1
    
    remove_empty_directories()
    click.secho(f'moved {count} out of {len(paths)} to {move_to_path}')

def remove_empty_directories() -> None:
    for root, folders, files in os.walk(os.getcwd()):
        if f'.DS_Store' in files:
            send2trash(f'{root}/.DS_Store')

    dirs = list()
    for root, folders, files in os.walk(os.getcwd()):
        if not files and not folders:
            dirs.append(root)
    dirs = sorted(dirs, key = lambda x: -1 * len(Path(x).parents))
    for dir in dirs:
        send2trash(dir)

def get_delete_paths() -> list:
    if not duple_outputs_exist():
        return
    
    with open('duple.delete', 'r') as f:
        paths = f.read().splitlines()
    return paths

def duple_outputs_exist() -> bool:
    if not Path('duple.delete').exists() or not Path('duple.json').exists():
        raise FileExistsError('duple.delete and/or duple.json do no exists - run duple scan to create these files')
        return False
    return True