from spyder_index.readers.directory import DirectoryReader
from spyder_index.readers.s3 import S3Reader
from spyder_index.readers.watson_discovery import  WatsonDiscoveryReader

__all__ = [
    "DirectoryReader",
    "S3Reader",
    "WatsonDiscoveryReader",
]
