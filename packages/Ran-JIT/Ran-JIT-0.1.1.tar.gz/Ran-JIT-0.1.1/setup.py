from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Ran-JIT',
  version='0.1.1',
  description='A python lib when imported boosts your code using JIT',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Coden',
  author_email='codenrblx@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='booster',
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
        'numba>=0.53.1',       # Just-In-Time compilation for Python
        'psutil>=5.8.0',       # System and process utilities
        'requests>=2.25.1',    # HTTP library
        'requests-cache>=0.5', # Caching for requests
        'aiohttp>=3.7.4',      # Asynchronous HTTP client
        'asyncio',             # Async support (builtin library, no version required)
        'httpx>=0.18.2',       # HTTP client for async and sync requests
        'urllib3>=1.26.5'  
   ],
)