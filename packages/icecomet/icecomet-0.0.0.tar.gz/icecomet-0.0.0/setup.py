from setuptools import setup, find_packages
versionInt = [0,0,0]

ve=f'{versionInt[0]}.{versionInt[1]}.{versionInt[2]}'
# import subprocess
# if True:
#     subprocess.run('python3 setup.py sdist bdist_wheel'.split(' '))
#     subprocess.run('twine upload dist/*'.split(' '))

setup(
    name='icecomet',
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





# vup=versionInt[2]+1
# import os
# file_path = __file__
# with open(file_path, 'r') as file:
#     content = file.readlines()
# rep = str(vup)
# content[1] = f'versionInt = [0,0,{rep}]\n'
# with open(file_path, 'w') as file:
#     file.writelines(content)


