from setuptools import setup, find_packages

setup(
    name='VAssure',
    version='v1.1',
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True,  # Ensures .robot and other non-Python files are included
    author='Sukumar Kutagulla',
    author_email='your.email@example.com',
    description='A VAssure Automation Framework',
    long_description=open('README.md', encoding='utf-8').read(),  # Reading with encoding
    long_description_content_type='text/markdown',
    url='https://github.com/Spotline-Inc/V-Assure.git',  # Replace with actual project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'selenium',
        'robotframework',
        'robotframework-pabot',                  # Parallel execution for Robot Framework
        'robotframework-seleniumlibrary',        # Selenium Library for web automation
        'pycryptodome',                          # Cryptography library
        'pymongo',                               # MongoDB support
        'pytz',                                  # Timezone handling
        'requests',                              # HTTP library
        'ratelimit',                             # Rate limiting support
        # Add more dependencies as needed
    ],
    package_data={
        'VAssure': [
            'CommonResources/*.robot',           # Include .robot files from CommonResources
            'HubConfiguration/*.robot',          # Include .robot files from HubConfiguration
            'VaultUtilities/*.robot',            # Include .robot files from VaultUtilities
            'CustomKeywords/*.py',               # Include Python files from CustomKeywords
            'CustomLibrary/*.py',                # Include Python files from CustomLibrary
            'VeevaWorkFlowPreReqAPIs/*.py',      # Include Python files from VeevaWorkFlowPreReqAPIs
            'WonderPharmaResources/*.robot',     # Include .robot files from WonderPharmaResources
        ],
    },
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            # Define any CLI scripts here if needed
        ],
    },
)
