from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
	readme = readme_file.read()

requirements = ["python-dateutil>=2.8.2", "dill>=0.3.5.1", "networkx>=2.8.0", "psutil>=5.9.5", "requests>=2.29.0", "commonhelper>=0.0.5", "mphelper>=0.0.3", "biodata>=0.1.0", "simplevc>=0.0.3"]

setup(
	name="rmsp",
	version="0.1.0",
	author="Alden Leung",
	author_email="alden.leung@gmail.com",
	description="Resource management system for python",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/aldenleung/rmsp/",
	packages=find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	],
	entry_points = {
		'console_scripts': [
			'rmstools = rmsp.rmstools:main',
		],
	}	
	
)

