from setuptools import setup, find_packages

setup(
    name='BJ_LED_M',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 
        'bleak',
        'qasync',
        'PyQt6',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [ 
            'bjled-cli=bj_led.main:main',
        ],
    },
    author='Walkercito',
    author_email='walkercitoliver@gmail.com',
    description='A library for controlling MohuanLED lights via Bluetooth',
    long_description=open('README.md').read(),
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
