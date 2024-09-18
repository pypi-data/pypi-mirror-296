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
def cli() -> None:
    pass

def get_hash(path: str, hash: str) -> str:
    with open(path, 'rb') as f:
        digest = hashlib.file_digest(f, hash)
    return digest.hexdigest(), path

def dict_from_stat(stats: os.stat_result) -> dict:
    temp = repr(stats).replace('os.stat_result(', '').replace(')','').replace(' ', '').split(',')
    result = dict()
    for item in temp:
        temp_item = item.split('=')
        result[temp_item[0]] = int(temp_item[1])
    return result

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
    if c[True] == 0:
        click.secho('Must select at least one flag to determine handling of duplicates, ex: -d')
        return
    
    # filelist = list()
    # for root, dirs, files in os.walk(path, followlinks=False):
    #     for file in files:
    #         if Path(f'{root}/{file}').exists():
    #             filelist.append(f'{root}/{file}')

    #eliminate files with unique sizes from analysis - if a file has a unique size it isn't a duplicate of another file
    rawfilesdict = dict()
    filedict = dict()
    # click.secho('Preprocessing Directories....')
    for root, dirs, files in tqdm(os.walk(path, followlinks=False), desc = 'Preprocessing Directories'):
        for file in files:
            temp = f'{root}/{file}'
            tempPath = Path(temp)
            tempStat = dict_from_stat(tempPath.stat())
            if tempPath.exists():
                rawfilesdict[temp] = tempStat
                if tempStat['st_size'] not in filedict.keys():
                    filedict[tempStat['st_size']] = list()
                filedict[tempStat['st_size']].append(temp)

    filelist = list()
    for k, v in filedict.items():
        if len(v) > 1:
            filelist.extend(v)
    #/eliminate files with unique sizes from analysis

    hash_start = perf_counter()
    hashes = process_map(get_hash, filelist, repeat(hash), max_workers = number_of_cpus, chunksize = 2, desc = 'Hashing Files...')
    hash_finish = perf_counter()

    p_dict: dict = dict()
    for hash, file_path in hashes:
        if hash not in p_dict.keys():
            p_dict[hash] = list()
        p_dict[hash].append(str(Path(file_path).absolute()))

    result = {k: v for k, v in p_dict.items() if len(v) > 1}

    for k, v in result.items():
        stats = dict()
        for file in v:
            stat = Path(file).stat()
            stats[file] = dict_from_stat(stat)
        result[k] = stats    
    
    # compute some statistics and create outputs
    total_size = 0
    file_count = 0
    for k, stats in result.items():
        for file, stat in stats.items():
            file_count += 1
            total_size += stat['st_size']
        total_size -= stat['st_size']
        file_count -= 1

    raw_size = 0
    for k, v in rawfilesdict.items():
        raw_size += v['st_size']

    with open('duple.json', 'w') as f:
        json.dump(result, f, indent = 4)
    
    with open('duple.all_files.json', 'w') as f:
        json.dump(rawfilesdict, f, indent = 4)

    create_remove_list(result, *flags)

    click.secho()
    click.secho(f'{click.style(len(rawfilesdict.keys()),fg = "green")} files there were scanned with a total size of {click.style(humanize.naturalsize(raw_size), fg = "green")}; there are {click.style(len(filelist), fg = "green")} potential duplicates.')
    click.secho(f'Further processing yielded {click.style(file_count, fg = "red")} duplicates in {click.style(len(result.keys()), fg = "red")} groups')
    click.secho(f'Duplicates which can be removed: {click.style(humanize.naturalsize(total_size), fg = "red")}')
    click.secho()
    click.secho(f"Wrote {click.style('duple.json', fg = 'green')} with results.")
    click.secho(f"Wrote {click.style('duple.delete', fg = 'green')} with file paths to be deleted -> {click.style('`duple rm`', fg = 'green')}.")
    click.secho(f"Wrote {click.style('duple_all_files.json', fg = 'green')}, file statistics on all files within {click.style(str(Path(path).absolute()), fg = 'green')}")
    click.secho(f'Total Processing time: {click.style(round(perf_counter() - start, 4), fg = "green")} seconds, Hash processing time: {click.style(round(hash_finish - hash_start,4), fg = "green")} seconds.')

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
        
        for key in keys:
            if key == result:
                delete_files.append(f'orig: {key}')
            else:
                delete_files.append(f'dupe: {key}')

        delete_files.append('')
        # keys.remove(result)
        # delete_files.extend(keys)
    
    with open('duple.delete', 'w') as f:
        for file in delete_files:
            f.write(f'{file}\n')

@cli.command()
def rm() -> None:
    '''
    rm sends all 'dupe' files specified in duple.delete to the trash folder
    '''

    if not duple_outputs_exist():
        return

    paths = get_delete_paths()
    
    for path in tqdm(paths):
        if path[:6] == 'dupe: ' and path and Path(path[:6]).exists():
            # click.secho(f'deleteing file: {path[6:]}')
            send2trash(path[6:])

    remove_empty_directories()

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

@cli.command()
def version() -> str:
    '''
    A simple program to find and remove duplciate files.
    '''
    path = Path(__file__).parent
    if version:
        with open(f'{path}/pyproject.toml', 'r') as f:
            lines = f.read().splitlines()
        
        for line in lines:
            if line[:7] == 'version':
                click.secho(f'duple version: {line[-6:-1]}')