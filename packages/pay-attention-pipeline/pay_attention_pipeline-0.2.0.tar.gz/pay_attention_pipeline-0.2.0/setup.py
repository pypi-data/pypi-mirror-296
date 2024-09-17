from setuptools import setup, find_packages


setup(
    name="pay-attention-pipeline",
    version="0.2.0",
    author="Pedro Silva",
    author_email="pedrolmssilva@gmail.com",
    description="A pipeline for computing **Influence** and performing **Generation with GUIDE** to enhance transformer model explainability and performance.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/netop-team/pay_attention_pipeline",  # Replace with your GitHub repo or project URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch>=2.4.0",
        "transformers>=4.44.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)