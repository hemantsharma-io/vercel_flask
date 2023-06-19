import openai
import requests
import json
from dataclasses import dataclass
from urllib.parse import urlparse
from nltk.tokenize import word_tokenize


access_token = "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"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

openai.api_key = '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'


@dataclass
class GitHubUser:
    giturl: str

class CustomClass:
    openai.api_key = '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'
    def process_url(self, user_id):
        # Perform custom processing with the URL
        # Replace this with your actual processing logic
        #result = f"Processing URL: {url}"
        return self.analyze_repositories(user_id)

    def validate_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme and parsed_url.netloc


    def fetch_user_repositories(self, giturl):
        # Validate the giturl parameter
        if not isinstance(giturl, str):
            raise ValueError("giturl parameter must be a string")

        # Validate the URL
        if not self.validate_url(giturl):
            raise ValueError("Invalid URL format")

        # Extract the username from the GitHub user URL
        username = giturl.split("/")[-1]

        # Fetch the user repositories using the GitHub API
        api_url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(api_url, timeout=10)

        # Check if the request was successful
        response.raise_for_status()

        # Get the repositories from the response
        repositories = response.json()

        # Return the repositories
        return repositories


    # Function to generate GPT-3.5 response using OpenAI API
    def generate_gpt_response(self, prompt):
        openai_key = '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'

        # API endpoint
        api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
        
        # Define the prompt you want to generate completion for
        # prompt = "Once upon a time"
        
        # Set the maximum number of tokens in the response
        max_tokens = 50
        
        # Set the temperature parameter (higher values make the output more random)
        temperature = 0.8
        
        # Create the payload for the API request
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        
        # Set the headers with your API key
        headers = {
            'Authorization': f'Bearer {openai_key}',
            'Content-Type': 'application/json'
        }
        
        # Make the API request
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        
        # Parse the response
        data = response.json()
        return data
        return data['choices'][0]['text'].strip()
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text.strip()


    def analyze_repositories(self, user_id):
        # Take GitHub user ID as input
        result_text = ""
        user_url = f"https://github.com/{user_id}"
        
        try:
            #user = GitHubUser(giturl=user_url)
            repositories = self.fetch_user_repositories(user_url)

            complex_repository = None
            max_complexity = float('-inf')
            
            for repo in repositories:
                # Generate GPT analysis for the repository
                prompt = f"This repository, {repo['full_name']}, is technically complex."

                # Calculate complexity score based on GPT response
                gpt_response = self.generate_gpt_response(prompt)
                return gpt_response
                complexity_score = len(word_tokenize(gpt_response))

                # Print repository analysis
                result_text = result_text + f"Repository: {repo['full_name']}\n"
                result_text = result_text + f"Complexity Score: {complexity_score}\n"
                result_text = result_text + f"Analysis: {gpt_response}\n"
                result_text = result_text + "-------------------------------------\n"

                # Update max complexity and complex repository if necessary
                if complexity_score > max_complexity:
                    max_complexity = complexity_score
                    complex_repository = repo['full_name']

            # Print the most technically complex repository
            result_text = result_text + f"The most technically complex repository is: {complex_repository}\n"

        except requests.exceptions.HTTPError as e:
            result_text = result_text + f"HTTPError occurred: {str(e)}\n"
        except ValueError as e:
            result_text = result_text + f"ValueError occurred: {str(e)}\n"

        return result_text
