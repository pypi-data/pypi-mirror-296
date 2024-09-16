from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pywinmemscanner",  # Your package name
    version="0.1.3",  # Version of your package
    author="Srinath Gudi",  # Your name
    author_email="srinathngudi11@gmail.com",  # Your email
    description="A library for scanning memory of other processes",  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/Srinath-N-Gudi/pywinmemscanner",  # GitHub or project URL
    packages=[
        'pywinmemscanner',
        'pywinmemscanner.source',
        'pywinmemscanner.utils',
        'pywinmemscanner.errors',
        'pywinmemscanner.utils.backend',
        'pywinmemscanner.utils.backend.dist',
        'pywinmemscanner.utils.backend.dist.__pycache__',
        'pywinmemscanner.utils.backend.dist.pyarmor_runtime_000000',
        'pywinmemscanner.utils.backend.dist.pyarmor_runtime_000000.__pycache__',
    ],  # Automatically find packages in your project
    package_data={
        'pywinmemscanner': ['utils/backend/dist/pyarmor_runtime_000000/pyarmor_runtime.pyd',
                            'utils/backend/MemoryScanner.dll']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",  # Python version requirement
    include_package_data=True,  # Include files listed in MANIFEST.in
)
