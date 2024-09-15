from setuptools import setup, find_packages

setup(
    name='orpheuspypractice',
    version='0.1.2',
    author='JGWill',
    author_email='jgi@jgwill.com',
    description='A Practice Package to Experiment with Orpheus\'s goals',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/orpheuspypractice',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "tlid",
        "requests",
        "music21",
        "ipython",
    ],
    entry_points={
        'console_scripts': [
            "jgabcli2 = src.jgcmlib.jgabcli:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)