# ripikutils

ripikutils is a Python package providing utility functions for MongoDB operations and AWS S3 interactions, specifically designed for internal use at Ripik Tech.

[![PyPI version](https://badge.fury.io/py/ripikutils.svg)](https://badge.fury.io/py/ripikutils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

You can install ripikutils using pip:

```
pip install ripikutils
```

## Features

- MongoDB data filtering, inserting, updation, and deletion
- AWS S3 operations (upload, download)
- Temporary directory management for image processing

## Usage

### MongoDB Operations

#### Basic Filters

<!-- ```python
from ripikutils.mongo import apply_basic_filter

# Apply basic filter to your MongoDB query
filtered_data = apply_basic_filter(collection, filter_params)
``` -->

#### Advanced Filters

<!-- ```python
from ripikutils.mongo import apply_advanced_filter

# Apply advanced filter with additional options
filtered_data = apply_advanced_filter(collection, filter_params, additional_options)
``` -->

### AWS S3 Operations

#### Upload File
<!-- 
```python
from ripikutils.aws import upload_to_s3

# Upload a file to S3
upload_to_s3(file_path, bucket_name, object_name)
``` -->

#### Download File

<!-- ```python
from ripikutils.aws import download_from_s3

# Download a file from S3
download_from_s3(bucket_name, object_name, local_file_path)
``` -->

#### Process Multiple Images

<!-- ```python
from ripikutils.aws import process_multiple_images

# Download images to a temp directory, process them, and upload results
result_paths = process_multiple_images(bucket_name, image_keys)
``` -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or support, please contact the Ripik Tech team at [vaibhav@ripik.ai](mailto:vaibhav@ripik.ai).