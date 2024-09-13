import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='radiant-framework',
    version='0.1a26',
    packages=['radiant.framework'],
    # packages=find_packages(where="radiant.framework"),
    # packages=find_packages(),
    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',
    download_url='https://github.com/dunderlab/python-radiant.framework',
    install_requires=[
        'Jinja2',
        'tornado',
        'brython',
    ],
    include_package_data=True,
    license='BSD-2-Clause',
    description="Radiant Framework",
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    classifiers=[

        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',



        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
    ],
)
