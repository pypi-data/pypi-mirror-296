from setuptools import setup, find_packages

DESCRIPTION = "A python script that allows users to check current storage and storage limits"
LONG_DESCRIPTION = "A python script that allows user to check current storage and storage limits on gaea system. Provides output which includes home quota, gpfs quota, and total data usage" 

setup(
        name='checkquota', 
        version='0.1', 
        author='Halle Derry',
        author_email='Halle.Derry@noaa.gov', 
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        license='MIT',
        entry_points={
            'console_scripts': [
                'checkquota=checkquota.checkquota.py:main', 
                ]
            },
    )

