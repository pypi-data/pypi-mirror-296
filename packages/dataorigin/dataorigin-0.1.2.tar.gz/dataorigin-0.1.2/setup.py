from setuptools import setup, find_packages

setup(
    name='dataorigin', 
    version='0.1.2', 
    description='Librería para la integración de DataOrigin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DataOrigin/dataorigin', 
    project_urls={
        'Homepage': 'https://github.com/DataOrigin/dataorigin', 
        'Website': 'http://dataorigin.es/', 
    },
    author='DataOrigin',
    author_email='info@dataorigin.es',
    license='GNU General Public License v3 (GPLv3)', 
    packages=find_packages(), 
    install_requires=[], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
