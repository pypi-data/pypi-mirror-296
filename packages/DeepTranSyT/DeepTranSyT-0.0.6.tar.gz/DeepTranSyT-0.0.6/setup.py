from setuptools import setup, find_packages

setup(
    name='DeepTranSyT',
    version='0.0.6',
    description="Transporters annotation using LLM's",
    author='Gonçalo Apolinário Cardoso',
    author_email='goncalocardoso2016@gmail.com',
    package_dir={"": "src"}, 
    packages=find_packages(where="src"),  
    install_requires=[ 
       "Bio==1.7.1",
       "biopython==1.79",
        "fair_esm==2.0.0",   
        "numpy==1.26.4",
        "pandas==2.2.2",
        "pytorch_lightning==2.2.5",
        "tensorflow==2.17.0",
        "torch==2.3.0",
    ],
    entry_points={
        'console_scripts': [
            'run-predictions=DeepTranSyT.main:main',
        ],
    },
)