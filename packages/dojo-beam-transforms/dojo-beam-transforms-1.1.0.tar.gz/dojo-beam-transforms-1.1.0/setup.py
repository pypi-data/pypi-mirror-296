from setuptools import setup, find_packages

setup(
    name='dojo-beam-transforms',
    version='1.1.0',
    url='https://github.com/DOJO-Smart-Ways/DOJO-Beam-Transforms',
    license='MIT',
    author='Dojo Technology',
    description="An Apache Beam collection of transforms",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'apache-beam[dataframe,gcp,interactive]==2.58.1',
        'pandas==2.0.3',
        'pandas-datareader==0.10.0',
        'PyMuPDF==1.23.22',
        'pypinyin==0.51.0',
        'unidecode==1.3.8',
        'openpyxl==3.0.10',
        'fsspec==2024.6.1',
        'gcsfs==2024.6.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
