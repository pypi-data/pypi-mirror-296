
# Asuraa Library

## Overview

The Asuraa library provides a suite of AI functionalities, including image generation, code generation, and chatbot interactions. This README provides a guide to install and use the library in a Python environment.

## Installation

To install or upgrade the Asuraa library, use the following pip command:

```bash
pip install --upgrade Asuraa
```

## Usage

### 1. AI Image Generation

Generate an AI image based on a description.

```python
from Asuraa import AsuraaAPI
ai = AsuraaAPI()

response = ai.imagine("cat image")
print(response)

```

### 2. ChatGPT AI

Interact with the ChatGPT AI for various responses. You can also specify modes for tailored interactions.

```python
from Asuraa import AsuraaAPI

ai = AsuraaAPI()
# Execute Chatgpt AI with the input text

response = ai.chatgpt("Whats the weather in San Francisco today? And what is the date?")
print(response)

```

### 3. Code Generation

Generate code using either Blackbox AI or Gemini AI.

```python
from Asuraa import AsuraaAPI
ai = AsuraaAPI()

# Execute blackbox AI with the input text
response = ai.blackbox("write flask app code")

print(response)
```

### 4. DataGpt AI

Fetch data science information using DataGPT AI.

```python
from Asuraa import AsuraaAPI
ai = AsuraaAPI()

# Execute datagpt AI with the input text
response = ai.datagpt("what is data science")

print(response)
```
### 5. Gemini AI 

```python
from AsuraaAPI import AsuraaAPI
ai = AsuraaAPI()
# Execute Gemini AI with the input text

response = ai.gemini("Who are you")
```
### 6. Bing image

```python
from AsuraaAPI import AsuraaAPI
ai = AsuraaAPI()
# Execute Bing Image AI with the input text

response = ai.bingimage("a man with car")
```
## License

© 2024-2025 Asuraa. All rights reserved.
