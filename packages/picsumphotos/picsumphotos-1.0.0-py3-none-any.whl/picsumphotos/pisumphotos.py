import requests
import urllib3
from urllib3.exceptions import LocationParseError

def isValidUrl(url: str) -> bool:
    """
    Verifies if the provided URL is valid by checking if it contains a scheme and a host.

    Args:
        url (str): The URL string to be validated.

    Returns:
        bool: True if the URL is valid, otherwise False.
    """
    try:
        parsedUrl = urllib3.util.parse_url(url)
        return parsedUrl.scheme is not None and parsedUrl.host is not None
    except LocationParseError:
        return False

def getImageBinary(url: str) -> bytes:
    """
    Fetches the binary content of an image from a given URL.

    Args:
        url (str): The URL of the image.

    Returns:
        bytes: The binary content of the image.

    Raises:
        HTTPError: If the request is unsuccessful (status code not 200).
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()

def createUrl(width: int, height: int, seed: str = None, picId: int = None, blur: int = None, grayscale: bool = False) -> str:
    """
    Generates a URL for fetching images from the Picsum API with optional parameters.

    Args:
        width (int): Width of the image in pixels.
        height (int): Height of the image in pixels.
        seed (str, optional): Seed value for generating a specific random image. Defaults to None.
        picId (int, optional): ID of a specific image from the Picsum database. Defaults to None.
        blur (int, optional): Blur intensity for the image. Higher values mean more blur. Defaults to None.
        grayscale (bool, optional): If True, the image will be grayscale. Defaults to False.

    Returns:
        str: The constructed URL with the specified parameters.
    """
    if seed is not None:
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    elif picId is not None:
        url = f"https://picsum.photos/id/{picId}/{width}/{height}"
    else:
        url = f"https://picsum.photos/{width}/{height}"
    
    params = []
    if grayscale:
        params.append("grayscale")
    if blur is not None:
        params.append(f"blur={blur}")

    if params:
        url += "?" + "&".join(params)

    return url

def getImage(width: int = 200, height: int = 200, seed: str = None, picId: int = None, blur: int = None, grayscale: bool = False) -> tuple:
    """
    Fetches an image from Picsum API and returns both its URL and binary content.

    Args:
        width (int, optional): Width of the image in pixels. Defaults to 200.
        height (int, optional): Height of the image in pixels. Defaults to 200.
        seed (str, optional): Seed value for generating a specific random image. Defaults to None.
        picId (int, optional): ID of a specific image from the Picsum database. Defaults to None.
        blur (int, optional): Blur intensity for the image. Defaults to None.
        grayscale (bool, optional): If True, the image will be grayscale. Defaults to False.

    Returns:
        tuple: A tuple containing the image URL and its binary content.
    """
    imageUrl = createUrl(width=width, height=height, seed=seed, picId=picId, blur=blur, grayscale=grayscale)
    binaryData = getImageBinary(imageUrl)
    
    return imageUrl, binaryData

def getImageList(limit: int = 30) -> list:
    """
    Retrieves a list of image URLs from the Picsum API based on the specified limit.

    Args:
        limit (int, optional): The maximum number of image URLs to return. Defaults to 30.

    Returns:
        list: A list of image URLs.
    """
    maxImageId = limit - 1
    imageUrls = []
    page = 1
    running = True

    while running:
        response = requests.get(url=f"https://picsum.photos/v2/list?page={page}&limit=100")
        for item in response.json():
            if int(item["id"]) > maxImageId:
                running = False
                break
            else:
                imageUrls.append(item["download_url"])
        page += 1
    
    return imageUrls

def saveImage(imageDataOrUrl: str, path: str, fileName: str, imageFormat: str, secure: bool = True) -> None:
    """
    Saves an image either from a URL or raw binary data to the specified path.

    Args:
        imageDataOrUrl (str): Either a URL or binary data of the image.
        path (str): The directory path where the image will be saved.
        fileName (str): The name of the file without the extension.
        imageFormat (str): The format in which to save the image ('png', 'jpg', 'jpeg', 'webp').
        secure (bool, optional): If True, checks the format for compatibility. Defaults to True.
    
    Notes:
        - The function assumes the provided format is valid unless 'secure' is set to False.
    """
    validFormats = ["png", "jpg", "jpeg", "webp"]
    if imageFormat.lower() not in validFormats and secure:
        print("Warning: The image format provided is not tested and may not work! "
              "If you want to proceed anyway, set 'secure=False' in the 'saveImage' function call.")

    if isValidUrl(imageDataOrUrl):
        # If imageDataOrUrl is a URL, download the image data
        binaryData = getImageBinary(imageDataOrUrl)
    else:
        # Assume imageDataOrUrl is binary data
        binaryData = imageDataOrUrl

    # Save the binary data directly to the file
    with open(f"{path}\\{fileName}.{imageFormat}", "wb") as file:
        file.write(binaryData)