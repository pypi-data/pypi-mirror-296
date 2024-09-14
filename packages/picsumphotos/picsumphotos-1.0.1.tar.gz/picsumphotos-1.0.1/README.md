# Image Utility Package

This package provides utility functions for working with images using the Picsum API. It includes functionalities to validate URLs, fetch image data, generate image URLs with various parameters, retrieve a list of image URLs, and save images to disk.

## Features

- **Validate URLs**: Check if a given URL is valid.
- **Fetch Image Data**: Retrieve the binary content of an image from a URL.
- **Generate Image URLs**: Create URLs for fetching images from the Picsum API with various parameters.
- **Fetch Image**: Get an image from the Picsum API and its binary content.
- **Retrieve Image List**: Get a list of image URLs from the Picsum API.
- **Save Image**: Save an image to a specified path from either a URL or raw binary data.

## Installation

You can install the package using pip. Make sure you have `requests` and `urllib3` installed:

```bash
pip install requests urllib3
```

## Usage

### Validate URL

```python
from image_utils import isValidUrl

url = "https://example.com/image.jpg"
print(isValidUrl(url))  # Output: True or False
```

### Fetch Image Data

```python
from image_utils import getImageBinary
url = "https://example.com/image.jpg"
binary_data = getImageBinary(url)
```

### Generate Image URL

```python
from image_utils import createUrl

url = createUrl(width=800, height=600, seed="example", blur=5, grayscale=True)
print(url)  # Output: Constructed URL with specified parameters
```

### Fetch Image

```python
from image_utils import getImage

image_url, binary_data = getImage(width=800, height=600, seed="example")
print(image_url)  # Output: Image URL
```

### Retrieve Image List

```python
from image_utils import getImageList

image_urls = getImageList(limit=10)
print(image_urls)  # Output: List of image URLs
```

### Save Image

```python
from image_utils import saveImage

image_url = "https://example.com/image.jpg"
# Or
image_url = "binary_image_data"
saveImage(imageDataOrUrl=image_url, path="path/to/directory", fileName="image", imageFormat="jpg")
```

## Functions

```python
isValidUrl(url: str) -> bool
```
Verifies if the provided URL is valid by checking if it contains a scheme and a host.

```python
getImageBinary(url: str) -> bytes
```
Fetches the binary content of an image from a given URL.

```python
createUrl(width: int, height: int, seed: str = None, picId: int = None, blur: int = None, grayscale: bool = False) -> str
```
Generates a URL for fetching images from the Picsum API with optional parameters.

```python
getImage(width: int = 200, height: int = 200, seed: str = None, picId: int = None, blur: int = None, grayscale: bool = False) -> tuple
```
Fetches an image from Picsum API and returns both its URL and binary content.

```python
getImageList(limit: int = 30) -> list
```
Retrieves a list of image URLs from the Picsum API based on the specified limit.

```python
saveImage(imageDataOrUrl: str, path: str, fileName: str, imageFormat: str, secure: bool = True) -> None
```
Saves an image either from a URL or raw binary data to the specified path.

## Notes

- Ensure that ```path``` in ```saveImage``` is a valid directory path.
- The ```secure``` flag in ```saveImage``` helps in warning about untested image formats

## License

This package is licensed under the Apache2 License. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0.txt) file for details.

## Contact

For any questions, please reach out to packages@escapedshadows.com.

## Disclaimer
I do not own any rights to the provided License file; all rights are owned by the Apache Foundation. Additionally, I am not affiliated with [picsum.photos](https://picsum.photos) in any way. This package is a community-driven project designed to simplify interaction with the [picsum.photos](https://picsum.photos) API directly from your Python Script.