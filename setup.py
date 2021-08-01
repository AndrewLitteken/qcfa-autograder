from setuptools import setup

setup(
    name='qcfa_autograder',
    version='0.1',
    description='Quantum Computing for All Autograder',
    packages=[
        'qcfa_autograder',
    ],
    install_requires = [
        'qiskit==0.28',
        'numpy',
        'networkx',
    ]
)
