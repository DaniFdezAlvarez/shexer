from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'shexer',
  packages = find_packages(exclude=["*.local_code.*"]), # this must be the same as the name above
  version = '1.2.0',
  description = 'Automatic schema extraction for RDF graphs',
  author = 'Daniel Fernandez-Alvarez',
  author_email = 'danifdezalvarez@gmail.com',
  url = 'https://github.com/DaniFdezAlvarez/shexerp3',
  download_url = 'https://github.com/DaniFdezAlvarez/shexerp3/archive/1.2.0.tar.gz',
  keywords = ['testing', 'shexer', 'shexerp3', "rdf", "shex", "shacl", "schema"],
  classifiers = [],
  install_requires=[            
          'Flask',
          'Flask-Cors',
		  'rdflib',
		  'SPARQLWrapper',
		  'rdflib-jsonld',
      'wlighter'
      ],
)