from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="cipherspy",
    version="0.4.1",
    author="Fathi AbdelMalek",
    author_email="abdelmalek.fathi.2001@gmail.com",
    url="https://github.com/fathiabdelmalek/cipherspy.git",
    description="Strong Passwords Generator made with python.",
    license="OSI Approved :: MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['cipherspy', 'cipherspy.cipher'],
    python_requires=">=3",
    install_requires=["numpy"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ]
)
