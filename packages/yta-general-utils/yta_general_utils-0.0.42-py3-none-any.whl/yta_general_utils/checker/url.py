import requests
import mimetypes


def url_is_ok(url: str):
    """
    Checks if the provided url is valid. It returns True if yes or
    False if not. This method uses a head request to check the 
    status_code of the response.
    """
    if not url:
        return False

    if not isinstance(url, str):
        raise Exception('The "url" parameter provided is not a str.')
    
    try:
        response = requests.head(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        print('Something went wrong with "' + url + '" (exception raised).')
        return False
    
def verify_image_url(url: str):
    """
    This method will check that the provided 'url' is a valid one, that
    it is an image, and also will return the image file extension (if
    available), or False if not valid 'url'.

    Use this method before trying to download an image from a url.

    This method will send a head request to the provided 'url', check
    the status_code and also the content-type.
    """
    if not url:
        # TODO: Maybe raise Exception (?) I think no...
        return False
    
    try:
        response = requests.head(url)

        if response.status_code != 200: # Maybe more than only 200 are valid
            return False
        
        if not response.headers['content-type'].startswith('image/'):
            return False
        
        # This below is like 'image/jpeg', 'application/pdf' so maybe we can just
        # split by '/' and obtain the second part, because when I guess from a
        # 'image/jpeg' content-type, the response is '.jpg' and not '.jpeg'...
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)

        # TODO: Review this below when tested 
        # This 'other_extension' below could be a better choice maybe (read above)
        other_extension = '.' + content_type.split('/')[1]

        return extension
    except requests.ConnectionError as e:
        print('Something went wrong with "' + url + '" (exception raised).')
        return False
    
def is_google_drive_url(google_drive_url: str):
    """
    Checks if the provided 'google_drive_url' is a string with a
    valid Google Drive url format or not. It returns True if yes
    or False if not.
    """
    if google_drive_url.startswith('https://drive.google.com/file/d/') or google_drive_url.startswith('drive.google.com/file/d/'):
        return True
    
    return False