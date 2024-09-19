from setuptools import setup, find_packages

setup(
    name='TOOLS-IDM',
    version='1.0.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ess=ess.ess:main',
        ],
    },
    description='Script untuk memverifikasi lisensi dan menghasilkan barcode',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nama Anda',
    author_email='email@domain.com',
    url='https://github.com/username/repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)