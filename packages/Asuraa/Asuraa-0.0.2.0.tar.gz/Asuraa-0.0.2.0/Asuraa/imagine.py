import random
import requests
import string,re,os,io
import json,time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from requests_html import HTMLSession
from PIL import Image


class Imagine:
    
    def __init__(self)->None:
        """Api for various purpose
    support group : https://t.me/AsuraaSupport
    owner : @AsuraaSupport
        """
        pass

    @staticmethod
    def imagine(prompt: str) -> bytes:
        """Generates an AI-generated image based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating the image.

        Returns:
            bytes: The generated image in bytes format.
            
        Example usage:
        >>> from Asuraa import api
        >>> generated_image= api.imagine("boy image")
        >>> print(generated_image)
        """
        url = 'https://ai-api.magicstudio.com/api/ai-art-generator'

        form_data = {
            'prompt': prompt,
            'output_format': 'bytes',
            'request_timestamp': str(int(time.time())),
            'user_is_subscribed': 'false',
        }

        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            try:
                if response.content:
                    return response.content
                else:
                    raise Exception("Failed to get image from the server.")
            except Exception as e:
                raise e
        else:
            raise Exception("Error:", response.status_code)

        
