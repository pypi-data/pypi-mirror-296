from setuptools import setup, find_packages

setup(
    name='imgboost',
    version='0.1.0',
    description='A package to enhance images with brightness, contrast, and sharpness adjustments.',
    author='Dione Alfarisi',
    author_email='ardionefarisi1322@gmail.com',
    url='https://github.com/dionealfarisi/imgboost',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'opencv-python',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'boost=imgboost.enhance:main',
        ],
    },
)