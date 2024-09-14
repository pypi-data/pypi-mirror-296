from setuptools import setup

NAME = "smpaul"
VERSION = "0.1.0"

REQUIRES = [
  "requests",
]

setup(
    name=NAME,
    version=VERSION,    
    description="OMI Payment Integration",
    url='https://github.com/shuds13/pyexample',
    author='Paul Almerino',
    author_email='paul.almerino@smsupermalls.com',
    license='BSD 2-clause',
    packages=[NAME],
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)