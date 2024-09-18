from setuptools import setup, find_packages

setup(
    name='Mensajes-JavierCh',
    version='6.0',
    description='Un paquete para saludar y despedirse',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Javier Chávez Hernández',
    author_email='javierchavezsw@gmail.com',
    url='https://www.javchav11.dev',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() 
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
)

