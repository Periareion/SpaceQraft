from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Simple Quaternion-based 3D Engine'

setup(
    name="qraft",
    version=VERSION,
    author="Periareion (Anton Sollman)",
    author_email="<periareion05@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'pyopengl', 'numpy'],
    keywords=['python', '3D', 'graphics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)