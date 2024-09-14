from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension

setup(
    name="torch_thinning",
    version="1.0.0",
    author="Andranik Sargsyan",
    author_email="and.sargsyan@yahoo.com",
    description="Implementation of Zhang-Suen thinning in Torch",
    packages=["torch_thinning"],
    long_description="",
    ext_modules=[
        CUDAExtension(
            name="zhang_suen_thinning",
            sources=["torch_thinning/zhang_suen_thinning_kernel.cu"],
        )
    ],
    cmdclass={
        "build_ext": BuildExtension
    },
    include_package_data=True,
    install_requires=[
        "torch"
    ],
)