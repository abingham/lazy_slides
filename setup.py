from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'lazy_slides',
    version = '0.1',
    packages = find_packages(),

    # metadata for upload to PyPI
    author = 'Austin Bingham',
    author_email = 'austin.bingham@gmail.com',
    description = "Build a presentation by downloading images based on keywords.",
    license = 'MIT',
    keywords = 'presentation',
    # url = 'http://bitbucket.org/abingham/roid_rage',
    # download_url = 'https://bitbucket.org/abingham/roid_rage/src',
    long_description = 'With lazy_slides, you provide a sequence of keywords for the presentation slides you want to make. For each keyword, lazy_slides downloads an image that matches it and creates a slide for you. In the end, you have a presentation without all the work of having to actually create a presentation!',
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Presentation',
        ],
    platforms='any',
    setup_requires=[],
    install_requires=[
        'sqlalchemy',
        #'baker',
        #'decorator',
        # 'pycairo',
        #'pygame',
        ],

    package_data = {
        'lazy_slides.dummy': ['*.gif', '*.jpg'],
        },

    entry_points = {
        'console_scripts': [
            'lazy_slides = lazy_slides.slides:main',
            ],
        },
    )

