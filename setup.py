from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = ''

setup(
    name="qqq",
    version=VERSION,
    author="Periareion (Anton Sollman)",
    author_email="<periareion05@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'numpy'],
    keywords=['python', '3D', 'graphics'],
)