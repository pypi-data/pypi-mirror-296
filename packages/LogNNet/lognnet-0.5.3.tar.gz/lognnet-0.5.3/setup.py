from setuptools import setup, find_packages

VERSION = '0.5.3'


def readme():
    with open('README.md', 'r') as f:
        return f.read()


requirements = [
    'numpy>=2.1.0',
    'pandas>=2.2.2',
    'scikit-learn>=1.5.1',
    'scipy>=1.14.0',
    'setuptools>=73.0.1',
    'joblib>=1.4.2'
]


setup(
    name='LogNNet',
    version=VERSION,
    description='LogNNet is a neural network that can be applied to both classification and regression tasks, '
                'alongside other networks such as MLP, RNN, CNN, LSTM, Random Forest, and Gradient Boosting. '
                'One of the key advantages of LogNNet is its use of a customizable chaotic reservoir, which is '
                'represented as a weight matrix filled with chaotic mappings. In this version, a congruent '
                'generator is used, producing a sequence of chaotically changing numbers.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/izotov93/LogNNet',
    author="Andrei Velichko and Yuriy Izotov",
    author_email='izotov93@yandex.ru',
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.11',
    include_package_data=True,
)
