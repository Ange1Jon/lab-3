# missing import statements should be added here
import wikipedia
import cv2
from images import get_wikipedia_page_thumbnail_url, download_image_from_url

def prompt_for_image():
    """
    Prompts the user for the name of a Wikipedia page and obtains the URL of the thumbnail image of the page.
    
    return url, page_name: str, str
    """
    search_query = input("Enter name of a personality: ")
    try:
        results = wikipedia.search(search_query, results=3, suggestion=False)
        if len(results) == 0: return None, None

        print("Select a name from the following list:")
        for i, result in enumerate(results):
            print(f"{i+1}. {result}")
        choice = 0
        while choice < 1 or choice > len(results):
            choice = int(input("Enter the number of the desired name: "))
            if choice < 1 or choice > len(results):
                print("Invalid choice. Please try again.")

        return get_wikipedia_page_thumbnail_url(results[choice-1]), results[choice-1]
    except Exception as e:
        print(f"Error: Unable to find image for the given name: {e}")
        return None, None
    
def convert_image_to_cartoon(image_path):
    """
    Converts an image to a cartoon given the image_path.
    """
    img = cv2.imread(image_path)
    
    # Image tranformation from https://dev.to/ethand91/cartoon-filter-using-opencv-and-python-3nj5
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 200, 200)
    cartoon = cv2.bitwise_and(color, color, mask = edges)

    cv2.imwrite(image_path, cartoon)


    
if __name__ == "__main__":
    image_url, name = prompt_for_image()
    while image_url is None: image_url, name = prompt_for_image()
    path = download_image_from_url(image_url, name)
    convert_image_to_cartoon(path)
    print(f"Cartoon image of {name} saved as {path}")

