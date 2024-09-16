# Image extraction - Libraries
from PIL import Image, ExifTags
import requests
from lxml import html
from io import BytesIO
import re
from urllib.parse import urlparse
import os
import zipfile # Zip file library
from tqdm import tqdm  # For the progressbar

#____________________________________
# 1) Obtain list of individual image urls within Google Photos Album.

def extract_image_urls(googleAlbumURL, imageXpath, output_path): #, imageXpath = '//a[@tabindex="0"]/@href'):
  '''
  Take url and xpath and return the list of image urls.
  Parameters = "url of the google album", "(Optional) xpath of the image urls".
  Returns = "List of the image urls except 1st one (unnecessary)", "Name of the album".
  '''

  # The Google album URl from which the further image urls should be obtained.
  url = googleAlbumURL

  # Send a GET request to the URL
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Extract the full HTML content
      html_content = response.text
      # print("HTML content extracted successfully!\n")

      # Optionally, print the HTML content (useful for debugging)
      # print(html_content)
  else:
      print(f"Failed to retrieve HTML. Status code: {response.status_code}")


  # Parse HTML content
  parser = html.HTMLParser()
  tree = html.fromstring(html_content, parser=parser)

  # Extract all hrefs from the <a> tags where tabindex = 0
  #hrefs = tree.xpath('//a[@tabindex="0"]/@href')
  hrefs = tree.xpath(imageXpath)

  # Ignore the first element in the list and keep the rest
  list_imageURLs = hrefs[1:]  # Ignoring the first href

  if output_path == "defaultlocationpreference":

    # name of the album.
    is_album_name = tree.xpath('//meta[@property="og:title"]/@content')
    if is_album_name:
      album_name = str(is_album_name[0]) + ".zip"
    else:
      album_name = "Compressed_GoogleAlbum.zip"

  else:
    # Use designated output_path
    album_name = output_path

  # Returning the hrefs.
  return list_imageURLs, album_name

#____________________________________
# 2) Functions to convert image urls into full quality downloadable url.

def downloadable_image_url(image_url, url_prefix): #, url_prefix = "https://photos.google.com/"):
  '''
  This downloads the full resolution image from the Google photos individual image url.
  Parameters - image url
  Returns - Direct downloadable image url.
  '''

  # Use the prefix and prepare the image url.
  url = url_prefix + image_url

  # Fetch the HTML content
  response = requests.get(url)
  response.raise_for_status()  # Raise an error for bad responses

  # Parse the HTML content
  tree = html.fromstring(response.content)

  # Extract all script contents with a class attribute
  script_contents = tree.xpath('//script[@class]/text()')

  # Initialize a list to store extracted image URLs
  list_image_urls = []

  # Define the regular expression pattern for image URLs
  # image_url_pattern = r'https://lh3.googleusercontent.com/pw/'
  # image_url_pattern = r'https:\\/\\/lh3\.googleusercontent\.com\\/pw\\/[-\w]+'
  image_url_pattern = r'(https:\/\/lh3\.googleusercontent\.com\/pw\/[-\w]+)'

  # Check if script_content is not empty and convert the first element to string
  if script_contents:

      # Loop through all script contents and search for image URLs
      for content in script_contents:
          urls = re.findall(image_url_pattern, content)
          list_image_urls.extend(urls)

  # Desired image.
  downloadable_image_url = str(list_image_urls[0]) + "=s0-d-ip"

  # Return the extracted image URLs
  return downloadable_image_url

#____________________________________
# 3) Compress the image while retaining the metadata.

# Function to compress images with PIL and add original metadata.
def compress_image_PIL_with_metadata(image_url):
  '''
  Compress + Obtain real file name of an image using Pillow with a specified compression quality, overwriting existing metadata, and optionally saving without metadata.

  Args:
    image_url: URL to the input image.
    output_path: Path to save the compressed image.
    save_with_metadata (bool, optional): Whether to save the image with the provided metadata (default: True).

  Returns:
    Compressed image as BytesIO object,
    Original filename.
  '''

  # Send a GET request to the image URL
  response = requests.get(image_url, allow_redirects=True)
  response.raise_for_status()  # Ensure the request was successful

  #_________________

  # Obtaining the filename from the https requests.
  content_disposition = response.headers.get('content-disposition')

  # Proceeding if it exists.
  if content_disposition:
    # Content-Disposition: attachment; filename="example.jpg"
    filename = content_disposition.split('filename=')[-1].strip('"')

    # Conditionally processing only jpegs, further support for other formats will be added in the future.
    file_extension = filename.split(".")[-1]
  else:
    filename =  None

  if filename is None:
    # Fallback to URL-based filename extraction
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)

  #_________________

  # Process only if the file is a jpeg.
  if file_extension == 'jpg':

    # Obtain img_file as bytes stored in memory.
    img_file_bytes = BytesIO(response.content)

    # Load the image into PIL from the response content
    image = Image.open(img_file_bytes)

    img = image.convert('RGB')

    # Initiating the variable
    compressed_img_bytes = BytesIO()

    # extracting the exif or metadata info.
    # exif = img.info['exif']

    if 'exif' in img.info:
      exif = img.info['exif']
      img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True, exif = exif)

    else:
      img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True)


    # Apply compression with a customizable quality parameter (adjust as needed)
    #img.save(output_path, quality=40, format='JPEG', optimize=True, exif = exif)

    # Apply compression with a customizable quality parameter (adjust as needed)
    # Store as bytes in memory.
    #compressed_img_bytes = BytesIO()
    #img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True, exif = exif)

    # Return compressed_img_bytes, filenme..
    return compressed_img_bytes, filename

  # else, print the filename and reason. In future, this will be added as a txt file to the zip.
  else:
    print("Skipped non-JPEG/ non-JPG file: ", str(filename))

#____________________________________
# 4) In the End, Zip all the files together.

def zip_output(dict_compressedImages, output_path):
  '''
  Takes the dictionary of compressed images and the output_path and returns a zip file of the images.
  '''

  # Prepare ZIP file
  with zipfile.ZipFile(output_path, 'w') as zipf:
    # Loop and Write the images to the ZIP file.
    for filename, compressedimagebytes in dict_compressedImages.items():
      zipf.writestr(filename, compressedimagebytes.getvalue())


#____________________________________
# 5) Orchestrate the entire process and produce a zip file as the output.

def compress_GoogleAlbum_jpeg(googleAlbumURL, stats = True, output_path = "defaultlocationpreference", imageXpath = '//a[@tabindex="0"]/@href', url_prefix = "https://photos.google.com/"):
  '''
  Produces a zip file as the output.
  Parameters: googleAlbumURL = Photos album Url,
              stats = True (default),
              output_path = current code folder (default),
              imageXpath = '//a[@tabindex="0"]/@href' (default),
              url_prefix = "https://photos.google.com/" (default)
  Returns: A zip file of the compressed images (JPEGs).
  '''

  # Intiating an empty list, empty dict.
  list_image_urls = []
  dict_compressedImages = {}

  # Extracting the list of individual image urls.
  list_image_urls, output_path = extract_image_urls(googleAlbumURL, imageXpath=imageXpath, output_path = output_path)

  # Validating if stats is necessary.
  if stats:

    # Using for loop to loop through the album.
    for image_url in tqdm(list_image_urls, desc = "Compressing Images"):

      # Intiating an empty string.
      download_url = ''

      # Obtaining the downloadable image url.
      download_url = downloadable_image_url(image_url, url_prefix = url_prefix)

      # Compressing the image in the download_url and obtaining the output.
      # Return compressed_image as BytesIO object, file name.
      compressed_image, file_name = compress_image_PIL_with_metadata(download_url)

      # Adding the returned variables to a dictionary -> Key = file_name , Value = Compressed image as ByteIO object.
      dict_compressedImages[file_name] = compressed_image
    
  # If stats is not necessary
  else:

    # Using for loop to loop through the album.
    for image_url in list_image_urls:

      # Intiating an empty string.
      download_url = ''

      # Obtaining the downloadable image url.
      download_url = downloadable_image_url(image_url, url_prefix = url_prefix)

      # Compressing the image in the download_url and obtaining the output.
      # Return compressed_image as BytesIO object, file name.
      compressed_image, file_name = compress_image_PIL_with_metadata(download_url)

      # Adding the returned variables to a dictionary -> Key = file_name , Value = Compressed image as ByteIO object.
      dict_compressedImages[file_name] = compressed_image


  zip_output(dict_compressedImages, output_path)

#____________________________________
