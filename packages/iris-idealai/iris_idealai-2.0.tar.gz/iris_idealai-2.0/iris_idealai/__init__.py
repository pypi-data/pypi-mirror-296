import PIL.Image
import requests
from io import BytesIO
from .script import m_set, m_build, t_gen

class Iris:
    def __init__(self, model_name=None, api_key=None):
        self.api_key = api_key
        if api_key:
            # Validate the API key using the security-codes endpoint
            validation_response = self._validate_api_key(api_key)
            
            if validation_response.get('status') == 'success':
                if validation_response.get('num_of_requests', 0) > 0:
                    t_gen().configure(api_key=validation_response.get('key'))  # Use the validated key
                    self.model = t_gen().GenerativeModel(model_name or m_set())
                    self.introduction = m_build()
                else:
                    # Raise an error if the request limit is reached
                    raise Exception("You have exceeded the limit of requests per day.")
            else:
                # Raise an error if the API key is invalid
                raise Exception("Invalid API key.")
        else:
            self.model = t_gen().GenerativeModel(model_name or m_set())
            self.introduction = m_build()

    def _validate_api_key(self, api_key):
        url = "https://practice.mchaexpress.com/iris/security-code.php"
        try:
            response = requests.post(url, json={"key": api_key})
            response_data = response.json()
            return response_data
        except Exception as e:
            raise Exception(f"Error validating API key: {e}")

    def _introduce(self):
        return self.introduction

    def generate_text(self, prompt):
        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, stream=False)
        return response

    def generate_chunk_text(self, prompt):
        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, stream=True)

        # Collect all chunks of text
        chunks = []
        for chunk in response:
            if hasattr(chunk, 'text'):
                chunks.append(chunk.text)
            else:
                chunks.append(str(chunk))
        
        return "\n".join(chunks)
    
    def generate_custom_text(self, prompt, candidate_count=1, stop_sequences=None, max_output_tokens=100, temperature=1.0):
        if stop_sequences is None:
            stop_sequences = []
        
        # Create the GenerationConfig object with the provided parameters
        generation_config = t_gen().types.GenerationConfig(
            candidate_count=candidate_count,
            stop_sequences=stop_sequences,
            max_output_tokens=max_output_tokens,
            temperature=temperature
        )

        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, generation_config=generation_config)
        return self._process_response(response)
    
    def generate_image(self, prompt):
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt} without pollination.ai mark/tag"
        
        try:
            # Fetch the image from the URL
            response = requests.get(url)
            if response.status_code == 200:
                image_blob = BytesIO(response.content)
                image = PIL.Image.open(image_blob)

                return image
            else:
                raise Exception("Failed to fetch image")

        except Exception as e:
            print(f"Error: {e}")
            return None

    def analyze_image(self, image_url, prompt="Tell me about this image"):
        try:
            response = requests.get(image_url)
            if response.status_code == 200 and 'image' in response.headers['Content-Type']:
                image = PIL.Image.open(BytesIO(response.content))
                response = self.model.generate_content([prompt, image])
                analyzed_text = self._process_response(response)
                return f"{analyzed_text}"
            else:
                return f"\n\nError: Unable to download the image or the URL is incorrect."
        except PIL.UnidentifiedImageError:
            return f"\n\nError: The image could not be identified or processed."
        
    def _process_response(self, response):
        result = []
        for chunk in response:
            if hasattr(chunk, 'text'):
                result.append(chunk.text)
            else:
                result.append(str(chunk))
        return "\n".join(result)
