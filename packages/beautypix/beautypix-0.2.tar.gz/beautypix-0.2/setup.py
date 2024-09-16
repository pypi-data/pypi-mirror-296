from setuptools import setup, find_packages 

setup(

    name='beautypix',
    description='BeautyPix is a versatile Python tool designed for capturing and managing screenshots of specified domains. It efficiently captures screenshots. Ideal for web developers, testers, and digital archivists, BeautyPix simplifies the process of monitoring and documenting web content',   
    version='0.2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Ankush Kumar Rajput (Mr.Horbio)',
    url='https://github.com/MrHorbio/bpix/blob/main/bpix_package/README.md',
    youtube="https://www.youtube.com/@Mr-Horbio",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        "selenium",
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python versions
)
