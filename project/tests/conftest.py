import os

os.environ["DB__SQLALCHEMY_URL"] = "sqlite:///:memory:"
os.environ["DB__ECHO"] = "True"
os.environ[
    "AUTH__JWT_SECRET_KEY"
] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
os.environ["AUTH__JWT_ALGORITHM"] = "HS256"
