from setuptools import setup, find_packages
versionInt = [0,0,0]

ve=f'{versionInt[0]}.{versionInt[1]}.{versionInt[2]}'


setup(
    name='icodetoyou',
    version=ve,
    description="I'am icecomet",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library',  # หรือ URL ของโปรเจกต์
    author='icecomet',
    author_email='icecomet634@gmail.com',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)





