from setuptools import setup, find_packages

from flashcommit.version import version

setup(
    name='flashcommit',
    version=version,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fcommit=flashcommit.main:main',
        ],
    },
    python_requires=">=3.8.0",
    install_requires=[
        'setuptools',
        'requests',
        'argparse',
        'pydantic',
        'gitpython',
        'pydriller',
        'python-dotenv~=1.0.1',
        'websocket-client',
        'rich',
        'prompt_toolkit',
    ],
)
