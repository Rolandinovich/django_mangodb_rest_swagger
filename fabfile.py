import fnmatch
import os
import tarfile

from fabric import task
from invoke import Responder

EXCLUDED_LIST_PATTERN = ['*git*', '*site*', '*idea*', '*media*', '*Dockerfile',
                         '*.yaml', '*.sqlite3', '.*yaml', '*fabfile.py',
                         '*.pyc', '*credentials.txt']


def filter_function(tarinfo):
    for ex_pattern in EXCLUDED_LIST_PATTERN:
        if fnmatch.fnmatch(tarinfo.name, ex_pattern):
            return
    return tarinfo


@task(hosts=['srv145228.hostiman.com'])
def deploy(c):
    password = c.config['connect_kwargs']['password'] + '\n'
    sudopass = Responder(pattern=r'\[sudo\] password:', response=password, )
    c.sudo('supervisorctl stop djremo', pty=True, watchers=[sudopass])
    with tarfile.open('djremo.tar.gz', 'w:gz') as tar:
        for root, dirs, files in os.walk('.'):
            for file in files:
                tar.add(os.path.join(root, file), filter=filter_function)

    c.run('mkdir -p temp_djremo')
    c.put('fitsup.tar.gz', 'temp_djremo')
    c.local('del djremo.tar.gz')
    c.run('mkdir -p djremo')

    c.run('tar -xzvf temp_djremo/djremo.tar.gz -C djremo')
    c.run('rm -rf temp_djremo')

    c.run('''. ./venv/djremo/bin/activate
cd djremo
pip install -r requirements.txt
python3 manage.py migrate 

''', pty=True)

    c.sudo('supervisorctl start fitsup', pty=True, watchers=[sudopass])

