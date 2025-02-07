import requests
import re

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

def get_wikipedia_page_thumbnail_url(page_title):
    """
    Fetches the URL of the thumbnail image of a Wikipedia page.

    page_title: str (title of the Wikipedia page)

    return image_url: str (URL of the thumbnail image)
    """

    try:
        headers = {'User-Agent': 'CS2132_Cartoon/1.0'}
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=pageimages&format=json&pithumbsize=500"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        page_id = next(iter(data['query']['pages']))
        image_url = data['query']['pages'][page_id].get('thumbnail', {}).get('source')
        
        return image_url
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching image URL: {e}")
    except Exception as e:
        print(f"Error: Unable to find image for the given name: {e}")
        return None

def download_image_from_url(url, save_name):
    """
    Downloads an image from a given URL and saves it with the correct file extension.
    
    url: URL of the image to download
    save_name: Name of the file (without extension) to save the image as

    return save_path: str (the path where the image is saved)
    """
    try:
        headers = {'User-Agent': 'CS2132_Cartoon/1.0'}
        
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image'):
            raise Exception("Unable to read image from URL")
        
        extension = content_type.split('/')[-1]
        
        save_name = re.sub(r'[ /]', '_', save_name)
        save_path = f"{save_name}.{extension}"
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        return save_path
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error downloading image: {e}")
