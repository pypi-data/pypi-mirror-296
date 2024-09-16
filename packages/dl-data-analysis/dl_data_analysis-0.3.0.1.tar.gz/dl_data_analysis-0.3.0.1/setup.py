from setuptools import setup, find_packages
with open("readme.md", "r") as f:
	description = f.read()

setup(
	name="dl_data_analysis",
	version="0.3.0.1",
	packages = find_packages(),
	install_requires=[
		"numpy", 
		"matplotlib",
		"scikit-learn",
		"pandas",
		"imblearn",
	],
	long_description = description,
    long_description_content_type = 'text/markdown'
	)