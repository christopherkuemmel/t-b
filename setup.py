"""Setup configuration."""
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tnb',
    version='0.0.1',
    author='Christopher Kuemmel',
    # author_email='',
    description="Transformers'n'Blockchain",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/christopherkuemmel/tnb',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'pandas==1.5.*',
        'pylint==2.15.*',
        'pytest==7.1.*',
        'torch==1.12.*',
        'torchaudio==0.12.*',
        'torchvision==0.13.*',
        'tqdm==4.64.*',
        'yapf==0.32.*',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
)