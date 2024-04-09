import requests
from bs4 import BeautifulSoup
import pdfkit
from openai import OpenAI
from dotenv import load_dotenv
import os
#import htmlmin

load_dotenv()

chatgpt_key = os.getenv('CHATGPT_KEY')

class WebsiteCrawler:
    def __init__(self, api_key=chatgpt_key, max_chars=2000):
        self.api_key = api_key
        self.max_chars = max_chars

    def crawl(self, ai_command, url, output_file):
        print('Initializing...')
        content_found = self.fetch_content(url)
        if content_found:
            processed_content = self.process_content(url, content_found)
            if processed_content:
                analyzed_content = self.analyze_content(ai_command, processed_content)
                self.save_data(output_file, analyzed_content)
        print('Finished!!!')

    def fetch_content(self, url):
        print('Fetching...')
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def process_content(self, url, content):
        print('Processing...')
        try:
            # Detect content type and process accordingly
            # For simplicity, let's assume the content type based on URL suffix
            content_type = os.path.splitext(url)[-1].lower()
            if content_type in ['.html', '.htm']:
                return self.process_html_content(content)
            elif content_type in ['.pdf']:
                return self.process_pdf_content(content)
            elif content_type in ['.jpg', '.jpeg', '.png', '.gif']:
                return self.process_image_content(content)
            elif content_type in ['.mp4', '.avi', '.mov']:
                return self.process_video_content(content)
            elif content_type in ['.mp3', '.wav']:
                return self.process_audio_content(content)
            else:
                return None
        except Exception as e:
            print(f"Error processing content: {str(e)}")
            return None

    def process_html_content(self, content):
        print('Processing HTML...')
        try:
            # Minimize HTML
            minified_html = htmlmin.minify(content.decode('utf-8'))  # type: ignore # noqa: F821

            soup = BeautifulSoup(minified_html, 'html.parser')
            main_tag = soup.find('main')
            if main_tag is None:
                main_tag = soup
            text = main_tag.get_text(separator='\n', strip=True)
            
            # Limitar o tamanho do texto
            if len(text) > self.max_chars:
                text = text[:self.max_chars]
            return text
        except Exception as e:
            print(f"Error processing HTML content: {str(e)}")
            return None

    def process_pdf_content(self, content):
        # Implement PDF content processing logic
        # For now, return None
        return None

    def process_image_content(self, content):
        # Implement image content processing logic
        # For now, return None
        return None

    def process_video_content(self, content):
        # Implement video content processing logic
        # For now, return None
        return None

    def process_audio_content(self, content):
        # Implement audio content processing logic
        # For now, return None
        return None

    def analyze_content(self, ai_command, content):
        print('Analyzing...')
        try:
            # Sentiment analysis
            # sentiment = TextBlob(content).sentiment
            # sentiment_str = f"Sentiment: {'Positive' if sentiment.polarity > 0 else 'Negative' if sentiment.polarity < 0 else 'Neutral'}"

            # Automatic summarization
            # summarized_content = summarize(content)

            # GPT-3 analysis
            client = OpenAI(api_key=self.api_key)
            client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": ai_command},
                    {"role": "user", "content": content}
                ])
            # gpt_result = completion.choices[0]

            # Combine results
            # analyzed_content = f"{sentiment_str}\n\nSummarized Content:\n{summarized_content}\n\nGPT-3 Analysis:\n{gpt_result['message']}"

            # return analyzed_content
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return None

    def save_data(self, output_file, result_content):
        print('Saving...')
        try:
            # Implement saving logic based on the type of content
            # For simplicity, let's assume we only save text content to PDF
            if not os.path.exists('pdf'):
                os.makedirs('pdf')

            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update this path accordingly
            options = {
                'encoding': 'UTF-8',
                'enable-local-file-access': True
            }
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(result_content, f'pdf/{output_file}', configuration=config, options=options)

            print("Data saved successfully!!!")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

crawler = WebsiteCrawler()
crawler.crawl("AI command", "https://example.com", "output.pdf")