import re
import html2text

def convert_html_to_markdown(html_content):
    # Create an html2text object
    h = html2text.HTML2Text()
    
    # Ignore links in the conversion if needed
    h.ignore_links = False
    
    # Remove image data from HTML content
    html_content = re.sub(r'<img[^>]*>', '', html_content)
    
    # Remove base64 image data from HTML content
    html_content = re.sub(r'data:image/png;base64,[^"]*', '', html_content)
    
    # Convert HTML content to markdown
    markdown_content = h.handle(html_content)
    return markdown_content