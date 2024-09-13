from setuptools import setup

setup(
    name='TSVZ',
    version='2.57',  
    py_modules=['TSVZ'],  # List of module names (without .py)
    description='An simple in memory wrapper around a TSV file to function as a database',
    author='Yufei Pan',
    author_email='pan@zopyr.us',
    url='https://github.com/yufei-pan/TSVZ',  # URL to the project’s homepage
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
)
