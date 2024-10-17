import requests
from bs4 import BeautifulSoup

def fetch_google_doc_html(url):
    """
    Fetch the Google Doc content as HTML.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the document: {response.status_code}")
    
    return response.text

def parse_html_data(html_content):
    """
    Parse the HTML content and extract the grid data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    data = []
    rows = soup.find_all('tr')
    
    for row in rows[1:]:  # Skip header row
        columns = row.find_all('td')
        if len(columns) == 3:
            try:
                x = int(columns[0].text.strip())
                char = columns[1].text.strip()
                y = int(columns[2].text.strip())
                data.append((char, x, y))
            except ValueError:
                continue
    
    return data

def create_and_print_grid(data):
    if not data:
        return
    
    max_x = max([item[1] for item in data])
    max_y = max([item[2] for item in data])
    
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    for char, x, y in data:
        grid[y][x] = char
    
    # Print the grid row by row
    for row in grid:
        print(''.join(row))

def decode_secret_message(url):
    # Step 1: Fetch the HTML content from the Google Doc
    html_content = fetch_google_doc_html(url)
    
    # Step 2: Parse the HTML for character and coordinate data
    data = parse_html_data(html_content)
    
    # Step 3: Create and save the grid
    create_and_print_grid(data)

url = input("Enter URL: ")
decode_secret_message(url)