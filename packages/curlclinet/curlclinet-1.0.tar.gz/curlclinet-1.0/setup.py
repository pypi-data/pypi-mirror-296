import setuptools
from setuptools.command.install import install as _install
import subprocess
import sys

class InstallWithCurl(_install):
    def run(self):
        _install.run(self)
        if 'termux' in sys.version.lower():
            try:
                subprocess.check_call(["pkg", "install", "-y", "curl"])
            except:
                print("Failed to install curl. Please install it manually.")
        elif sys.platform.startswith('linux'):
            try:
                subprocess.check_call(["pkg", "install", "-y", "curl"])
            except:
                print("Failed to install curl")
                try:
                    subprocess.check_call(["sudo", "apt-get", "install", "-y", "curl"])
                except:
                    try:
                        subprocess.check_call(["sudo", "dnf", "install", "-y", "curl"])
                    except:
                        print("Failed to install curl. Please install it manually.")
                    
        elif sys.platform == 'darwin':
            try:
                subprocess.check_call(["brew", "install", "curl"])
            except subprocess.CalledProcessError:
                print("Failed to install curl. Please install it manually.")
        else:
            print("Unsupported operating system. Please install curl manually.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curlclinet",
    version="1.0",
    author="Ahmed",
    author_email="esszz12345678@gmail.com",
    description="A simple library for making HTTP requests on Linux, macOS, and Termux systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Psoidh/SimpleClient",
    project_urls={
        "Bug Tracker": "https://github.com/Psoidh/SimpleClient/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Android",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
    cmdclass={
        'install': InstallWithCurl,
    }
)
