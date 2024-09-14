from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

setup(
    name='yaml_plotter',
    version='0.1.0',
    description='A Python plotter using yaml',
    author='Yezheng Zhang',
    author_email='cozardzhang@gmail.com',
    url='https://github.com/pxxxl/yaml-plotter',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['example.yml']},
    entry_points={
        'console_scripts': [
            'yml_plot=yaml_plotter.copy_example:copy_example_yml',
        ],
    },
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
