import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="mycryptool",
	version="1.0",
	author="ChopperCP",
	author_email="568624486@qq.com",
	description="A python package that include commonly used cryptographic algorithm and tools.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ChopperCP/MyCrptool",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
