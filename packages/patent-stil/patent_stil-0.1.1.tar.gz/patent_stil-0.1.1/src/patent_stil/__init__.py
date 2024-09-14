from .fpo_patent import *
from .google_patent import *
from .utils import createDirs,downloadFile
__all__ = [
    'downloadFile',
    'createDirs',
    'getFpoPatentInfo',
    "getFpoPatentInfoByUrl",
    "getFpoSearchResult",
    "downloadFpoPdf",
    "downloadFpoPdfByUrl",
    "autoFpoSpider",
    "getGooglePatentInfo",
    "getGooglePatentInfoByUrl"
]