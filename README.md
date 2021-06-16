# photo-editing-image-gallery-app-kivy
Cross-platform aplication developed in Kivy. <br>
## Functionalities:
- create image gallery from image folder
- open and edit single images (grayscaling and thresholding)
- save images after edit with renaming option available

## Project setup:
1. `pip install -r requirements.txt`
2. `python main.py`

## Debug
When running `python main.py` you might get `KeyError: 'kivy.garden.iconfonts'`. In this case run `garden install iconfonts` and then running `python main.py` should work. 
