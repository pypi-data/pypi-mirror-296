# coding:UTF-8
import setuptools

setuptools.setup(
    name="Allinonechay",
    version="4.0.3",
    author="Chay",
    author_email="lichenyi_2020@qq.com",
    url="https://github.com/lichenyichay/All-in-one-Including/",
    description="All-in-one",
    long_description="多功能一体机",
    python_requires=">=3.5",
    install_requires=["sympy>=1.13.1","mpmath>=1.3.0","lotterytickets>=2.0.0","numberandchinese>=1.0.0"],
    packages_dir={"": "src"},
    packages_data={"": ["*.txt", "*.info", "*.properties"], "": ["data/*.*"]},
    exclude=["*.test", "*.test.*", "test.*", "test"],
    classifiers=['Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 3"
                 ]
)
