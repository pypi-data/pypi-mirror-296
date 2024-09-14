from setuptools import setup, find_packages

setup(
    name='farsi_wordcloud',
    version='0.1.0',
    author='Alireza Parvaresh',
    author_email='parvvaresh@gmail.com',
    description='A package to generate Farsi word clouds with proper text rendering.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/parvvaresh/word_cloud_fa',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=3.4.0',
        'wordcloud>=1.8.1',
        'arabic-reshaper>=2.1.0',
        'python-bidi>=0.4.2',
    ],
)
