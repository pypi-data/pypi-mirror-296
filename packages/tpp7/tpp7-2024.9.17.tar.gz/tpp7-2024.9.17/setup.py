import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="tpp7", # Replace with your own username
	version="2024.9.17",
	author="Olivier Cardoso",
	author_email="Olivier.Cardoso@univ-paris-diderot.fr",
	description="Un paquetage pour les TP de Physique d'Université Paris-Cité",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/cardosoo/tp",
	package_dir={'': 'src'},
	# include_package_data=True,
	packages=setuptools.find_packages(where='src'),
	scripts=[
		'tests/minimalTPUsage.py',
		#'tests/minimalTPUsage.ipynb',
		#'tests/scripts/Oscil.py',
		#'tests/scripts/Oscillo.bsh',
		#'tests/scripts/OscilloGraph.py',
		#'tests/cmpl/20--permissions-usbtmc-Oscillo.rules',
		#'tests/cmpl/Oscillo.desktop',
		#'tests/cmpl/Oscillo.png'			
	],
	# package_data = {"cmpl": ["Oscillo.desktop"], "scripts": ["*"]},
	#data_files=[('cmpl', ['cmpl/Oscillo.desktop'])],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		'numpy', 'scipy', 'matplotlib', 'python-usbtmc', 'pandas', 'pyusb', 'fitutils'
	],
	python_requires='>=3.6',
)
