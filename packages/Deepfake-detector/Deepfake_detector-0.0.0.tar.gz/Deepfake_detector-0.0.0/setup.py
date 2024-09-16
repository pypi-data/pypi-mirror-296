from setuptools import setup, find_packages

setup(
    name='Deepfake_detector',
    description='Deepfake detection for images and videos',
    author='Adupa Nithin Sai',
    author_email='adupanithinsai@gmail.com',
    url='https://github.com/saiadupa/Deepfake-detector',
    packages=find_packages(),
    install_requires=[
        'tensorflow==2.13.0',
        'opencv-python==4.10.0.84',
        'numpy==1.24.3',
        'matplotlib==3.9.2',
    ],
    entry_points={
        'console_scripts': [
            'deepfake-detector=deepfake_detector.detector:predict_video',
        ],
    },
)
