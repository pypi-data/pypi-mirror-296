from setuptools import setup, find_packages

setup(
    name='Deepfake-detector',
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'tensorflow==2.13.0',
        'opencv-python==4.10.0.84',
        'numpy==1.24.3',
        'matplotlib==3.9.2',
        'gdown',
    ],
    description='A Python library for detecting deepfake images and videos.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Adupa Nithin Sai',
    author_email='adupanithinsai@gmail.com',
    url='https://github.com/saiadupa/Deepfake-detector',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3', 
)
