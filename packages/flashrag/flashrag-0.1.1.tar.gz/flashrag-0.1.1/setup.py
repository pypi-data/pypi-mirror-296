from setuptools import setup, find_packages

with open("requirements.txt") as fp:
    requirements = fp.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()

extras_require = {
    'core': requirements,
    'retriever': ['pyserini', 'sentence-transformers>=3.0.1'],
}
extras_require['full'] = sum(extras_require.values(), [])

setup(
    name="flashrag",
    version="0.1.1",
    packages=find_packages(),
    url="https://github.com/ignorejjj/FlashRAG",
    license="MIT License",
    author="Jiajie Jin, Yutao Zhu, Chenghao Zhang, Xinyu Yang",
    author_email="jinjiajie@ruc.edu.cn",
    description="A library for efficient Retrieval-Augmented Generation research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={"flashrag": ["/config/basic_config.yaml"]},
    install_requires=extras_require['core'],
    extras_require=extras_require,
    python_requires=">=3.8",
)
