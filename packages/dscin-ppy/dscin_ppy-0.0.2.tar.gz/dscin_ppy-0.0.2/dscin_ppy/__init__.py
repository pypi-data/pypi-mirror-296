from .functions import *
from .db_utils import *
from .etl_job import *
from .aws_utils import *

import os
bucket = os.getenv("S3_TRANSDICT_BUCKET")
key = os.getenv("S3_TRANSDICT_KEY")

download_object_from_s3(
    bucket, key, "src/translation_dictionaries.py"
)