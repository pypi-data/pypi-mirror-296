from setuptools import setup, find_namespace_packages

setup(
    name="easyhtr",
    version="0.1.1",
    description="Handwritten sentence recognition pipeline.",
    author="Faiq Ali",
    packages=find_namespace_packages(include=["htr_pipeline", "htr_pipeline.*"]),
    url="https://github.com/syedfaiqueali",
    install_requires=[
        "numpy>=1.17,<2.0",
        "onnxruntime==1.19.2",
        "opencv-python==4.10.0.84",
        "scikit-learn==1.5.2",
        "editdistance==0.8.1",
        "path==17.0.0",
    ],
    python_requires=">=3.9",
    package_data={"htr_pipeline.models": ["*"]},
)
