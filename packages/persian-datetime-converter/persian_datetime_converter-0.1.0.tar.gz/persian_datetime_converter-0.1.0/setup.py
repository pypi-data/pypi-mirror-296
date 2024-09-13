# setup.py

from setuptools import setup, find_packages

setup(
    name='persian_datetime_converter',
    version='0.1.0',
    description='Convert Python datetime objects to Persian (Jalali) calendar dates.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohammad Reza Bahmani',
    author_email='bahmanymb@gmail.com',
    url='https://github.com/bahmany/persian_datetime_converter',  # Replace with your GitHub URL
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)
