import setuptools


setuptools.setup(
    name='ansible-hostmanager',
    version='0.2.2',

    author='Max Zheng',
    author_email='maxzheng.os@gmail.com',

    description='CLI script to work with Ansible hosts file',
    long_description=open('README.rst').read(),

    url='https://github.com/maxzheng/ansible-hostmanager',

    install_requires=open('requirements.txt').read(),

    license='MIT',

    packages=setuptools.find_packages(),
    include_package_data=True,

    python_requires='>=3.6',
    setup_requires=['setuptools-git'],

    entry_points={
       'console_scripts': [
           'ah = ansible_hostmanager:main',
       ],
    },

    classifiers=[
      'Development Status :: 5 - Production/Stable',

      'Intended Audience :: Developers',
      'Topic :: Software Development :: User Interfaces',

      'License :: OSI Approved :: MIT License',

      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
    ],

    keywords='list ssh Ansible hosts file',
)
