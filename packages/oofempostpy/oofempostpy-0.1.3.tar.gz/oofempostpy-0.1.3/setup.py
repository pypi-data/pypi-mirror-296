from setuptools import setup, find_packages

setup(
    name='oofempostpy',
    version='0.1.3',
    description='A Python package to parse OOFEM simulation logs and export data to CSV',
    author='Cunyi (Bruce) Li',
    author_email='cunyicom@outlook.com',
    license='GPLv3+',
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.6',
)
