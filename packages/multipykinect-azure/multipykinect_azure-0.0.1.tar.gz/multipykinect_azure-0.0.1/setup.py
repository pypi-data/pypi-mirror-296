from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='multipykinect_azure',
    version='0.0.1',
    license='MIT',
    description='Python library to run Kinect Azure DK SDK functions which support multiple devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ibai Gorordo, JiaweiDing',
    url='https://github.com/MojiCartman/pyKinectAzure',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
)