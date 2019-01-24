from distutils.core import setup
setup(
  name='PyDBQuery',
  packages = ['pydbquery'],
  version = '0.2dev',
  license='MIT',
  description = 'Functional query selector for databases.',
  author = 'HidekiHrk',
  author_email = 'hidekihiroki123@gmail.com',
  url = 'https://github.com/HidekiHrk/PyDBQuery',
  download_url = 'https://github.com/HidekiHrk/PyDBQuery/archive/v_0.2.tar.gz',
  keywords = ['python', 'db', 'database', 'better', 'query'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)