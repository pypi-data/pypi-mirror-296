from setuptools import setup, find_packages

setup(
    name='DeepTranSyT',
    version='0.0.7',
    description="Transporters annotation using LLM's",
    author='Gonçalo Apolinário Cardoso',
    author_email='goncalocardoso2016@gmail.com',
    package_dir={"": "src"}, 
    packages=find_packages(where="src"),  
    install_requires=[ 
       "Bio",                             
       "biopython",
        "fair_esm",   
        "numpy",
        "pandas",
        "pytorch_lightning",
        "tensorflow",
        "torch",
    ],
    entry_points={
        'console_scripts': [
            'run-predictions=DeepTranSyT.main:main',
        ],
    },
)