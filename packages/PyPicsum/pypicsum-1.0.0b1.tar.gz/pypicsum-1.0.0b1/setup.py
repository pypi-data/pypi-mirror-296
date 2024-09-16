from setuptools import setup, find_packages

setup(
    name='PyPicsum',
    version='v1.0.0-beta1',
    description='PyPicsum is a port of the Picsum library but ported for Python Tkinter. It uses Pillow to handle images!',
    author='EchoTheDeveloper',
    author_email='admin@echothedeveloper.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pillow',
        # 'tkinter' is part of the Python standard library and does not need to be listed as a dependency
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
)



