#!/usr/bin/env python3
#
#       Yiğid BALABAN <fyb@fybx.dev>, 2024
#

# dotm
#
# [S] Description
# dotm is a simple dotfiles manager that can be used to backup and deploy dotfiles.
#
# It manages a git repository to deploy a list of files and directories to
# the local .config directory. When the backup command is executed, it
# copies the files and directories in the deploy_list to the
# local repository. git is used to keep track of changes.
#
# Deploying a configuration is possible by either directly calling it, or
# by specifying a git tag. The tag is used to checkout the repository to a
# specific commit, and then deploy the configuration on that time.
#
# Similar to deploying, backing up a configuration is possible by specifying
# a tag name. The tag is created after the files and directories are copied,
# essentially creating a snapshot of the configuration at that time.

# [S] Details
# * The configuration file for dotm is located in      $HOME/.config/dotm/config
# * The deploy list for selecting what and what not     $HOME/.config/dotm/deploy_list
#   to backup/deploy is searched in
# * The repository managed by dotm is located in      $HOME/.local/state/dotm/managed_repo

import os
import shutil
import sys

from git.repo import Repo
from crispy.crispy import Crispy
from tomlkit import dumps as toml_dumps
from tomlkit import parse as toml_parse
from tomlkit.items import String as toml_String
from tomlkit.items import Item as toml_Item
from os.path import join, relpath

VER = '1.0.1'
help_message = f'''dotm {VER} dotfiles/home backup helper by Yigid BALABAN

Commands:
=> init         Initialize dotm installation
-u, --url       [required] the URL of remote
-l, --local     [optional] create repository locally
-d, --deploy    [optional] deploy configuration

=> backup       Backups configuration to managed_repo (pushes to remote)
=> deploy       Deploys configuration in place from managed_repo (pulls remote)
=> help         Prints this message.
=> version      Prints the version.
'''

INITIALIZED = False
dir_home = os.path.expandvars('$HOME')
dir_config = join(dir_home, '.config')
dir_state = join(dir_home, '.local', 'state')
params = {}


def u_path(mode, path):
    if mode == 'deploy':
        return join(params['managed_repo'], relpath(path, dir_home))
    elif mode == 'backup':
        return join(params['managed_repo'], relpath(path, dir_home))
    else:
        raise ValueError(mode)


def u_get_files(directory: str) -> list[str]:
    if not os.path.exists(directory):
        return []

    files = []
    for root, _, filenames in os.walk(directory):
        files.extend(join(root, filename) for filename in filenames)
    return files


def t_init():
    global INITIALIZED
    if INITIALIZED:
        return
    INITIALIZED = True

    global params
    params = {
        'managed_repo': f'{dir_state}/dotm/managed_repo',
        'deploy_list': f'{dir_config}/dotm/deploy_list',
        'config_file': f'{dir_config}/dotm/config',
        'repo_url': '',
    }

    if os.path.exists(params['config_file']):
        with open(params['config_file'], 'r') as f:
            data = toml_parse(f.read())
            params.update({k: str(v) if isinstance(v, (toml_String, toml_Item)) else v for k, v in data.items()})
    else:
        with open(params['config_file'], 'w') as f:
            f.write(toml_dumps(params))


is_local_repo_created = lambda: os.path.exists(f"{params['managed_repo']}/.git")


def t_make_repo(from_url: str, local = False, check = True):
    """
    Create the local repository either by cloning from a remote, or by initializing it.

    :param str from_url: URL of the remote
    :param bool local: Whether to create locally (default = False)
    :param bool check: Whether to check if local repository exists (default = True)
    """
    if check and is_local_repo_created():
        print('[W] dotm: a managed repository was initialized. overriding contents')
    if local:
        r = Repo.init(params['managed_repo'])
        r.create_remote('origin', url=from_url)
        r.git.checkout('-b', 'main')
        return
    print(f'[I] dotm: cloning from remote {params['repo_url']}')
    Repo.clone_from(from_url, params['managed_repo'])


def t_pull_repo(overwrite: bool):
    try:
        # clone the repo from remote if local doesn't exist
        # or if we are allowed to overwrite existing local
        p_local_exists = is_local_repo_created()
        if not p_local_exists or overwrite:
            if p_local_exists:
                shutil.rmtree(params['managed_repo'])
            t_make_repo(params['repo_url'], check=False)
        else:
            # repo exists and it's forbidden to overwrite
            repo = Repo(params['managed_repo'])
            repo.remotes.origin.pull()
    except Exception as e:
        print(f'[E] dotm: unhandled error in \'t_pull_repo\': {e}')
        return False
    return True


def t_set_params(param_key: str, param_value: str):
    params[param_key] = param_value
    with open(params['config_file'], 'w') as f:
        f.write(toml_dumps(params))


def t_list(p_list: str) -> list[str]:
    l_i, l_d = [], []

    with open(p_list, 'r') as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l]

    for line in lines:
        ignore_it = False

        if line.startswith('#'):
            continue

        if line.startswith('!'):
            ignore_it = True
            line = line.removeprefix('!')
        elif '.git' in line:
            ignore_it = True

        line = join(dir_config, line[1:]) if line.startswith('%') else join(dir_home, line)

        if os.path.isfile(line):
            if ignore_it:   l_i.append(line)
            else:           l_d.append(line)
        else:
            if ignore_it:   l_i.extend(u_get_files(line))
            else:           l_d.extend(u_get_files(line))

    for element in l_i:
        if element in l_d:
            l_d.remove(element)

    with open(join(dir_state, 'dotm', 'dotm.log'), 'w') as f:
        f.writelines(map(lambda x: x + '\n', l_d))
    return l_d


def a_backup():
    l_deploy = t_list(params['deploy_list'])

    if len(l_deploy) == 0:
        print('[W] dotm: deploy_list is not created or empty. nothing will be backed up.')
        return False

    for file in l_deploy:
        file_in_repo = u_path('backup', file)
        os.makedirs(os.path.dirname(file_in_repo), exist_ok=True)
        shutil.copy(file, file_in_repo)

    repo = Repo(params['managed_repo'])
    repo.git.add(all=True)

    if repo.index.diff(None) or repo.untracked_files:
        repo.git.commit('-m', 'committed by dotm')
        repo.remotes.origin.push('main')
    return True


def a_deploy(use_deploy_list_in_managed_repo = False):
    l_deploy = t_list(os.path.join(params['managed_repo'], 'dotm', 'deploy_list')) if use_deploy_list_in_managed_repo else t_list(params['deploy_list'])

    if len(l_deploy) == 0:
        print('[W] dotm: deploy_list is not created or empty. nothing will be deployed.')
        return False

    for file in l_deploy:
        file_in_repo = u_path('deploy', file)
        os.makedirs(os.path.dirname(file), exist_ok=True)
        shutil.copy(file_in_repo, file)
    return True


def main():
    if len(sys.argv) == 1:
        print(help_message)
        sys.exit(0)

    t_init()
    c = Crispy()
    c.add_subcommand('init', 'Initialize dotm for use')
    c.add_subcommand('config', 'Configure dotm')
    c.add_variable('url', str)
    c.add_variable('local', bool)
    c.add_variable('deploy', bool)

    c.add_subcommand('deploy', 'Deploy a configuration to place')
    c.add_subcommand('backup', 'Backup current state following a deploy list')
    c.add_variable('tag', str)

    subcommand, args = c.parse_arguments(sys.argv[1:])

    match subcommand:
        case 'init':
            if args['url'] and type(args['url']) == str:
                t_set_params('repo_url', str(args['url']))
                if not args['local']:
                    s_pull = t_pull_repo(overwrite=True)
                    if args['deploy'] and s_pull:
                        a_deploy(True)
                else:
                    t_make_repo(args['url'], True)
        case 'config':
            if args['url']: t_set_params('repo_url', str(args['url']))
        case 'deploy':
            if t_pull_repo(False):
                a_deploy()
        case 'backup':
            a_backup()
        case 'help':
            print(help_message)
        case 'version':
            print(VER)
        case _:
            print(help_message)


if __name__ == '__main__':
    main()


# def backup(tag=''):
#     """Copies files and directories denoted in deploy_list from their source to
#     managed_repo directory.
# 
#     Args:
#         tag (str, optional): Git tag to publish for the commit. Defaults to ''.
#     """
#     if tag != '':
#         if tag in map(lambda x: x.replace('refs/tags/', ''), repo.tags):
#             return
#         created_tag = repo.create_tag(tag)
#         repo.remotes.origin.push(created_tag.name)


# def deploy(tag=''):
#     """Copies files and directories in managed Git repository to 
#     local .config directory, if they are present in the deploy list.
#     
#     Optinally, a tag can be specified to deploy a specific configuration.
# 
#     Args:
#         tag (str, optional): Git tag for a specific configuration. Defaults to ''.
#     """
#     if tag != '':
#         repo = Repo(params['managed_repo'])
#         repo.git.checkout(tag)
#         t_list()
#     
#     for file in list_deploy:
#         file_in_repo = util_path('deploy', file)
#         os.makedirs(os.path.dirname(file), exist_ok=True)
#         shutil.copy(file_in_repo, file)


