from setuptools import setup

setup(name='FigSync',
      author='author',
      author_email='germanespinosa@gmail.com',
      long_description=open('./FigSync/README.md').read() + '\n---\n<small>Package created with Easy-pack</small>\n',
      long_description_content_type='text/markdown',
      packages=['FigSync'],
      install_requires=['watchdog', 'pymupdf'],
      license='MIT',
      include_package_data=True,
      version='0.0.6',
      zip_safe=False)
