#!/usr/bin/env python3

import os
from setuptools import setup

# importlib-metadata dependency can be removed when RHEL8 and other 3.6 based systems are not in support cycles

install_requires = [
    'empy',
    'importlib-metadata; python_version < "3.8"',
    'pexpect',
    'packaging',
    'urllib3',
]

# docker API used to be in a package called `docker-py` before the 2.0 release
docker_package = 'docker'
try:
    import docker
except ImportError:
    # Docker is not yet installed, pick library based on platform
    # Use old name if platform has pre-2.0 version
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release') as fin:
            content = fin.read()
        if 'xenial' in content:
            docker_package = 'docker-py'
else:
    # Docker is installed, pick library based on what we found
    ver = docker.__version__.split('.')
    if int(ver[0]) < 2:
        docker_package = 'docker-py'

install_requires.append(docker_package)

kwargs = {
    'name': 'rocker',
    'version': '0.2.19',
    'packages': ['rocker'],
    'package_dir': {'': 'src'},
    'package_data': {'rocker': ['templates/*.em']},
    'entry_points': {
        'console_scripts': [
            'rocker = rocker.cli:main',
            'detect_docker_image_os = rocker.cli:detect_image_os',
        ],
        'rocker.extensions': [
            'cpu_limits = rocker.constraint_extensions:CpuLimits',
            'cuda = rocker.nvidia_extension:Cuda',
            'detach = rocker.extensions:Detach',
            'devices = rocker.extensions:Devices',
            'dev_helpers = rocker.extensions:DevHelpers',
            'env = rocker.extensions:Environment',
            'expose = rocker.extensions:Expose',
            'git = rocker.git_extension:Git',
            'group_add = rocker.extensions:GroupAdd',
            'home = rocker.extensions:HomeDir',
            'hostname = rocker.extensions:Hostname',
            'ipc = rocker.extensions:Ipc',
            'memory_limits = rocker.constraint_extensions:MemoryLimits',
            'name = rocker.extensions:Name',
            'network = rocker.extensions:Network',
            'nvidia = rocker.nvidia_extension:Nvidia',
            'port = rocker.extensions:Port',
            'privileged = rocker.extensions:Privileged',
            'pulse = rocker.extensions:PulseAudio',
            'rmw = rocker.rmw_extension:RMW',
            'shm_size = rocker.constraint_extensions:ShmSize',
            'ssh = rocker.ssh_extension:Ssh',
            'ulimit = rocker.ulimit_extension:Ulimit',
            'user = rocker.extensions:User',
            'volume = rocker.volume_extension:Volume',
            'x11 = rocker.nvidia_extension:X11',
        ]
    },
    'author': 'Tully Foote',
    'author_email': 'tfoote@osrfoundation.org',
    'keywords': ['Docker'],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'A tool to run docker containers with customized extras',
    'long_description': 'A tool to run docker containers with customized extra added like nvidia gui support overlayed.',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',

    'install_requires': install_requires,
    'extras_require': {
        'test': [
            'pytest'
        ]
    },
    'url': 'https://github.com/osrf/rocker'
}

setup(**kwargs)
