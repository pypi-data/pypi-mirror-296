from setuptools import setup, find_packages

setup(
	name="dl_data_analysis",
	version="0.1",
	packages = find_packages(),
	install_requires=[
		"numpy>=1.26.4", 
		"matplotlib>=3.7.5",
		"sklearn>=1.2.2",
		"pandas>=2.2.2",
	],
	)