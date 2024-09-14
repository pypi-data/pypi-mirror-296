from setuptools import setup, find_packages

setup(
    name='BlueLights',
    version='0.2.1',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [ 
        'bleak',
        'qasync',
        'PyQt6',
        'python-dotenv',
        'nest_asyncio',
        'asyncio',
        'colorsys'
    ],
    entry_points = {
        'console_scripts': [ 
            'bluelights=manager.main:main',
        ],
    },
    author = 'Walkercito',
    author_email = 'walkercitoliver@gmail.com',
    description ='A library for controlling MohuanLED lights via Bluetooth',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent", 
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.8'
)
