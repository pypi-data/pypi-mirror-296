from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '1.0'
DESCRIPTION = 'face matching'
LONG_DESCRIPTION = 'A package that allows two images and compare them to check if face in both images are same or not, also youcan use this package to detect face in image'

# Setting up
setup(
    name="facialmatch",
    version=VERSION,
    author="Hemang Baldha",
    author_email="hemang9705@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'numpy', 'scikit-learn'],
    keywords=['python', 'face', 'face matching', 'face detection', 'face recognition', 'opencv', 'opencv-python', 'numpy', 'scikit-learn'],
)