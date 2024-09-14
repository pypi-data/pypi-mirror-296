import random
import requests
import string,re,os,io
import base64,json,time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from requests_html import HTMLSession
from Asuraa.function import (MORSE_CODE_DICT,payloads_response,gpt_4_mode,payload8)
from base64 import b64decode as m,b64encode as n
from PIL import Image, ImageDraw, ImageFont
__version__ = "0.0.1.0"

__all__ = ["api"]


class Asuraa:
    
    def __init__(self)->None:
        """Api for various purpose
    support group : https://t.me/the_support_chat
    owner : @itzAsuraa"""
        pass
    
    @staticmethod
    def datagpt(args:str):
        """
        Sends a query to a specified datagpt API endpoint to retrieve a response based on the provided question.

        Args:
            args (str): The question or input for the datagpt.

        Returns:
            str: The response text from the datagpt API.

        Example usage:
        >>> from Asuraa import api
        >>> response = =.datagpt("What are the latest trends in AI?")
        >>> print(response)
        """
        url = m("aHR0cHM6Ly9hcHAuY3JlYXRvci5pby9hcGkvY2hhdA==").decode("utf-8")
        payload = {
            "question": args,
            "chatbotId": "712544d1-0c95-459e-ba22-45bae8905bed",
            "session_id": "8a790e7f-ec7a-4834-be4a-40a78dfb525f",
            "site": "datacareerjumpstart.mykajabi.com"
        }

        try:
            response = requests.post(url, json=payload)
            extracted_text = re.findall(r"\{(.*?)\}", response.text, re.DOTALL)
            extracted_json = "{" + extracted_text[0] + "}]}"
            json_text = extracted_json.replace('\n', ' ')

            data = json.loads(json_text)
            return {"results":data["text"],"join": "@AsuraaSupport", "success": True
                    }
        except Exception as e:
            return e   
    
    @staticmethod
    def blackpink(args):
        """generate blackpink  image from text
    """
        text = args
        font_path = os.path.dirname(__file__)+"blackpink.otf"
        font_size = 230
        font = ImageFont.truetype(font_path, font_size)
        fontsize = int(font.getlength(text))
        img = Image.new("RGB", (fontsize + 100, font_size + 100), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text(
            ((img.width - fontsize) / 2, 0),
            text,
            fill=(255, 148, 224),
            font=font,
            align="center",
        )
        draw.rectangle([0, 0, img.width, img.height], outline="#ff94e0", width=20)
        img2 = Image.new("RGB", (fontsize + 800, font_size + 300), color=(0, 0, 0))
        img2.paste(img, (350, 100))

        buffered = io.BytesIO()
        img2.save(buffered, format="JPEG")
        img_str = n(buffered.getvalue()).decode("utf-8")
        return img_str
    
    @staticmethod
    def blackbox(args: str) -> requests.Response:
        """
        Interact with the Blackbox AI API for generating content. 🧠

        Args:
            args (str): The input text to interact with the Blackbox AI chat API.

        Returns:
            requests.Response: The response object from the API request.

        Example usage:
        >>> from Asuraa import api
        >>> response = api.blackbox("Hello, how are you?")
        >>> print(response.text)
        {
            "response": "Generated content response",
            "status": 200
        }
        """

        url = m('aHR0cHM6Ly93d3cuYmxhY2tib3guYWkvYXBpL2NoYXQ=').decode("utf-8")
        
        payload = {
            "agentMode": {},
            "codeModelMode": True,
            "id": "XM7KpOE",
            "isMicMode": False,
            "maxTokens": None,
            "messages": [
                {
                    "id": "XM7KpOE",
                    "content": urllib.parse.unquote(args),
                    "role": "user"
                }
            ],
            "previewToken": None,
            "trendingAgentMode": {},
            "userId": "87cdaa48-cdad-4dda-bef5-6087d6fc72f6",
            "userSystemPrompt": None
        }

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'sessionId=f77a91e1-cbe1-47d0-b138-c2e23eeb5dcf; intercom-id-jlmqxicb=4cf07dd8-742e-4e3f-81de-38669816d300; intercom-device-id-jlmqxicb=1eafaacb-f18d-402a-8255-b763cf390df6; intercom-session-jlmqxicb=',
            'Origin': m('aHR0cHM6Ly93d3cuYmxhY2tib3guYWk=').decode("utf-8"),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return {"results": response.text, "join": "@AsuraaSupport", "success": True}
        except Exception as e:
            return e  
    
    @staticmethod
    def chatgpt(args:str,mode:str=False):
       
        """
        Sends a query to a specified chatgpt API endpoint to retrieve a response based on the provided question.
        

        Args:
            args (str): The question or input for the chatgpt.
            mode(str) : this  parameter is used to select different models of Chatgpt
                        available modes are "girlfriend","anime","animev2","flirt","santa","elonmusk","wormgpt"

        Returns:
            str: The response text from the chatgpt API.

        Example usage:
        >>> from Asuraa import api
        >>> response = api.chatgpt("hi babe?",mode="girlfriend")
        >>> print(response)
        """
        if not mode:
            session = requests.Session()
            response_data=payloads_response(payloads=payload8,args=args)
            url = m("aHR0cHM6Ly9hcGkuZXhoLmFpL2NoYXRib3QvdjEvZ2V0X3Jlc3BvbnNl").decode("utf-8")
            headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6ImJvdGlmeS13ZWItdjMifQ.O-w89I5aX2OE_i4k6jdHZJEDWECSUfOb1lr9UdVH4oTPMkFGUNm9BNzoQjcXOu8NEiIXq64-481hnenHdUrXfg",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
            response = session.post(url, headers=headers, data=json.dumps(response_data))
            return {"results":response.json()["response"],"join": "@AsuraaSupport", "success": True}
        else:
            try:
                result = gpt_4_mode(args, mode)
                return {"results":result,"join": "@AsuraaSupport", "success": True}
                
            except Exception as e:
                return e  

    
    @staticmethod
    def gemini(args: str) -> dict:
        """
        Generate content using the Gemini API. ✨

        Args:
            args (str): The input text to generate content.

        Returns:
            dict: A dictionary containing the generated content with metadata.

        Example usage:
        >>> from Asuraa import api
        >>> generated_content = api.gemini("Hello, how are you?")
        >>> print(generated_content)
        """
        url = m('aHR0cHM6Ly9nZW5lcmF0aXZlbGFuZ3VhZ2UuZ29vZ2xlYXBpcy5jb20vdjFiZXRhL21vZGVscy9nZW1pbmktcHJvOmdlbmVyYXRlQ29udGVudD9rZXk9QUl6YVN5QlFhb1VGLUtXalBWXzRBQnRTTjBEUTBSUGtOZUNoNHRN').decode("utf-8")
        headers = {'Content-Type': 'application/json'}
        payload = {
            'contents': [
                {'parts': [{'text': args}]}
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return {"results":generated_text,"join": "@AsuraaSupport", "success": True}
        except Exception as e:
            return e

    @staticmethod
    def bhagwatgita(chapter: int, shalok: int = 1) -> requests.Response:
        """
        Retrieve a verse from the Bhagavad Gita based on the provided chapter and shalok number.

        Args:
        chapter (int): The chapter number from which the verse will be retrieved.
        shalok (int, optional): The shalok number within the chapter. Default is 1.

        Returns:
        dict: A dictionary containing the chapter number, verse text, chapter introduction, and the specified shalok text.

        Example usage:
        >>> from Asuraa import api
        >>> verse_data = api.bhagwatgita(1, 5)
        >>> print(verse_data)
        """
        xc=base64.b64decode("aHR0cHM6Ly93d3cuaG9seS1iaGFnYXZhZC1naXRhLm9yZy9jaGFwdGVyLw==").decode(encoding="utf-8")
        url = f"{xc}{chapter}/hi"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraph = soup.find("p")
        chapter_intro = soup.find("div", class_="chapterIntro")
        co = soup.find_all("section", class_="listItem")
        output = [i.text.strip().replace("View commentary »", "").replace("Bhagavad Gita ", "").strip()  for i in co]
        data = {
            "chapter_number": chapter,
            "verse": paragraph.text,
            "chapter_intro": chapter_intro.text,
            "shalok": output[shalok],
        }

        return data

    
    @staticmethod
    def imdb(args: str) -> dict:
        """
        Retrieve information about a movie or TV show from IMDb based on the search query.

        Args:
        args (str): The movie or TV show to search for on IMDb.

        Returns:
        dict: A dictionary containing details about the movie or TV show, such as name, description, genre,
            actors, trailer link, and more.

        Example usage:
        >>> from Asuraa import api
        >>> movie_data = api.imdb("The Godfather")
        >>> print(movie_data)
        """

        session = HTMLSession()

        url = f"https://www.imdb.com/find?q={args}"
        response = session.get(url)
        results = response.html.xpath("//section[@data-testid='find-results-section-title']/div/ul/li")
        urls = [result.find("a")[0].attrs["href"] for result in results][0]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(f"https://www.imdb.com/{urls}", headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        movie_name = soup.title.text.strip()

        meta_tags = soup.find_all("meta")
        description = ""
        keywords = ""

        for tag in meta_tags:
            if tag.get("name", "") == "description":
                description = tag.get("content", "")
            elif tag.get("name", "") == "keywords":
                keywords = tag.get("content", "")

        json_data = soup.find("script", type="application/ld+json").string
        parsed_json = json.loads(json_data)

        movie_url = parsed_json["url"]
        movie_image = parsed_json["image"]
        movie_description = parsed_json["description"]
        movie_review_body = parsed_json["review"]["reviewBody"]
        movie_review_rating = parsed_json["review"]["reviewRating"]["ratingValue"]
        movie_genre = parsed_json["genre"]
        movie_actors = [actor["name"] for actor in parsed_json["actor"]]
        movie_trailer = parsed_json["trailer"]
        
        output = []
        for result in results:
            name = result.text.replace("\n", " ")
            url = result.find("a")[0].attrs["href"]
            if ("Podcast" not in name) and ("Music Video" not in name):
                try:
                    image = result.xpath("//img")[0].attrs["src"]
                    file_id = url.split("/")[2]
                    output.append({
                        "movie_name": movie_name,
                        "id": file_id,
                        "poster": image,
                        "description": description,
                        "keywords": keywords,
                        "movie_url": movie_url,
                        "movie_image": movie_image,
                        "movie_description": movie_description,
                        "movie_review_body": movie_review_body,
                        "movie_review_rating": movie_review_rating,
                        "movie_genre": movie_genre,
                        "movie_actors": movie_actors,
                        "movie_trailer": movie_trailer,
                        "join": "@AsuraaSupport",
                        "success": True,
                    })
                    return {"results": output}
                except:
                    return {"Success": False}
    
    @staticmethod
    def unsplash(args)->requests.Response:
        """
    Get image URLs related to the query using the iStockphoto API.

    Args:
        args (str): The search query for images.

    Returns:
        list: List of image URLs related to the query.
        
    Example usage:
    >>> from Asuraa import api
    >>> response = api.unsplash("boy image")
    >>> print(response)
    

    """
        url = f'https://www.istockphoto.com/search/2/image?alloweduse=availableforalluses&phrase={args}&sort=best'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://unsplash.com/'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            
        
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tags = soup.find_all('img')
            image_urls = [img['src'] for img in image_tags if img['src'].startswith('https://media.istockphoto.com')]
            
            return {"results": image_urls, "join": "@AsuraaSupport", "success": True}
        else:
            return {f"status code: {response.status_code}"}
      
    @staticmethod  
    def leetcode(username):
        """
    Retrieve user data including activity streak, profile information, and contest badges from LeetCode using GraphQL API.

    Args:
        username (str): The username of the LeetCode user.

    Returns:
        dict: A dictionary containing user data such as streak, total active days, badges, user profile information, and social media URLs.

    Example usage:
    >>> from Asuraa import api
    >>> user_data = api.leetcode("noob-mukesh")
    >>> print(user_data)"""
        url = base64.b64decode('aHR0cHM6Ly9sZWV0Y29kZS5jb20vZ3JhcGhxbC8=').decode("utf-8")

        payload = {
        'operationName': 'userProfileCalendar',
        'query': '''
        query userProfileCalendar($username: String!, $year: Int) {
        matchedUser(username: $username) {
            userCalendar(year: $year) {
            activeYears
            streak
            totalActiveDays
            dccBadges {
                timestamp
                badge {
                name
                icon
                }
            }
            submissionCalendar
            }
        }
        }
        ''',
        'variables': {'username': username, 'year': 2024}
    }

        payload_2 = {
        'operationName': 'userPublicProfile',
        'query': '''
        query userPublicProfile($username: String!) {
        matchedUser(username: $username) {
            contestBadge {
            name
            expired
            hoverText
            icon
            }
            username
            githubUrl
            twitterUrl
            linkedinUrl
            profile {
            ranking
            userAvatar
            realName
            aboutMe
            school
            websites
            countryName
            company
            jobTitle
            skillTags
            postViewCount
            postViewCountDiff
            reputation
            reputationDiff
            solutionCount
            solutionCountDiff
            categoryDiscussCount
            categoryDiscussCountDiff
            }
        }
        }
        ''',
        'variables': {'username': username}
    }

        try:
            response = requests.post(url, json=payload)
            data_1 = response.json()['data']['matchedUser']

            response = requests.post(url, json=payload_2)
            data_2 = response.json()['data']['matchedUser']

            output_dict2 = {} 
            output_dict2.update(data_1)
            output_dict2.update(data_2)
            output_dict = {}

            for key, value in output_dict2.items():
                if isinstance(value, dict):
                    output_dict[key] = {}
                    for k, v in value.items():
                        output_dict[key][k] = v
                else:
                    output_dict[key] = value
            return output_dict
        except Exception as e:
            return e
        
    @staticmethod
    def github(args):
        """
    Search GitHub information based on the username query provided.

    Args:
        args (str): The search query to find information of  GitHub User.

    Returns:
        dict: A dictionary containing search results of GitHub username .

    Example usage:
    >>> from Asuraa import api
    >>> search_results = api.github("noob-mukesh")
    >>> print(search_results)
    """

        n = base64.b64decode("aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS91c2Vycy8=").decode("utf-8")
        result = requests.get(f"{n}{args}").json()
        url = result["html_url"]
        name = result["name"]
        id = result["id"]
        company = result["company"]
        bio = result["bio"]
        pattern = "[a-zA-Z]+"
        created_at = result["created_at"]
        created = re.sub(pattern, " ", created_at)
        updated_at = result["updated_at"]
        updated = re.sub(pattern, " ", updated_at)
        avatar_url = f"https://avatars.githubusercontent.com/u/{id}"
        blog = result["blog"]
        location = result["location"]
        repositories = result["public_repos"]
        followers = result["followers"]
        following = result["following"]
        results = {
            "url": url,
            "name": name,
            "id": id,
            "company": company,
            "bio": bio,
            "created at": created,
            "updated at": updated,
            "Profile image": avatar_url,
            "blog": blog,
            "location": location,
            "repos": repositories,
            "followers": followers,
            "following": following,
        }
        return results
    
    @staticmethod
    def ai_image(prompt: str) -> bytes:
        """Generates an AI-generated image based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating the image.

        Returns:
            bytes: The generated image in bytes format.
            
        Example usage:
        >>> from Asuraa import api
        >>> generated_image= api.ai_image("boy image")
        >>> print(generated_image)
        """
        url = base64.b64decode('aHR0cHM6Ly9haS1hcGkubWFnaWNzdHVkaW8uY29tL2FwaS9haS1hcnQtZ2VuZXJhdG9y').decode("utf-8")

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

        
            
api=Asuraa()
