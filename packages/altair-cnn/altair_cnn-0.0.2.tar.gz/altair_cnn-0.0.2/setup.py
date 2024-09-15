from setuptools import setup, find_packages

setup(
    name='altair_cnn',
    version='0.0.2',
    description="A theme for Python's Altair statistical visualization library",
    long_description="A theme for Python's Altair statistical visualization library",
    long_description_content_type='text/x-rst',
    author='Matt Stiles',
    author_email='matt.stiles@cnn.com',
    url='http://www.github.com/turnercode/altair-cnn',
    license="MIT",
    packages=find_packages(), 
    install_requires=[
        'altair>=5.4.0', 
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6', 
)