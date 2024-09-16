# Python Package - gPhotosAlbum_JPEGcompression

## Overview

Short Description:
Takes Google Photos Album (visible to anyone with url) and produces a zip file with compressed JPEGS.

USP:
- The JPEGS retain the metadata.
- 1.5x to 15x reduction in file size depending on the JPEG.
- Larger files with higher megapixel undergo very good compression.
- Almost perfect image clarity up to 250% magnification.


## Release Notes

### version 1.4.3
- Some fixes (as always).


### version 1.4.2
- First public release of gPhotosAlbum_JPEGcompression.
- JPEGS retain metadata.


## Installation

You can install the package using pip:

```bash
pip install gPhotosAlbum_JPEGcompression
```

## Methods

### compress_GoogleAlbum_jpeg

Takes the Google Photos Album url as Input. Ensure that the Photos are set to "Accesible by anyone with the url".

Returns: A zip file of the compressed images (JPEGs).


```python
from gPhotosAlbum_JPEGcompression import compress_GoogleAlbum_jpeg


googleAlbumURL = "https://photos.app.goo.gl/loremimpsunm56"

compress_GoogleAlbum_jpeg(googleAlbumURL)
```

#### Parameters:

- **googleAlbumURL** (str): Photos album Url.
- **stats** (Boolean, Optional, default="True"): Progress bar and stats.
- **output_path** (str, Optional, default=current directorty): The output path for the zip file, Kindly ensure the directories exist..
- **imageXpath** (str, Optional, default=xpath): Xpath for webscrpaing purposes, only provided as optional to use if  Google changes the xpath.
- **url_prefix** (str, Optional , default="https://photos.google.com/"): Url prefix used for Webscraping, setting as an optional variable for future proofing and handling changes.
