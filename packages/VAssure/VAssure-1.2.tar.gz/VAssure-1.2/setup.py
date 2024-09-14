from setuptools import setup, find_packages

setup(
    name='VAssure',
    version='1.2',  # Remove 'v' prefix
    packages=find_packages(),  # Automatically find all packages in your project
    include_package_data=True,  # Ensures .robot and other non-Python files are included
    author='Sukumar Kutagulla',
    author_email='sukumar@spotline.com',
    description='A VAssure Automation Framework',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Spotline-Inc/V-Assure.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'selenium',
        'robotframework',
        'robotframework-pabot',
        'robotframework-seleniumlibrary',
        'pycryptodome',
        'pymongo',
        'pytz',
        'requests',
        'ratelimit',
    ],
    package_data={
        'V-Assure': [
            'VAssureCommonResources/*.robot',
            'VAssureHubConfiguration/*.robot',
            'VAssureVaultUtilities/*.robot',
            'VAssureCustomKeywords/*.py',
            'VAssureCustomLibrary/*.py',
            'VAssureAPIPreRequisites/*.py',
            'WonderPharmaResources/*.robot',
        ],
    },
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            # Define any CLI scripts here if needed
        ],
    },
)
