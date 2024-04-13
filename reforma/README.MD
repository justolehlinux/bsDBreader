# Web Scraping Tool

This Python script is designed to scrape product data from a specific website and store it in a CSV file. It utilizes web scraping techniques with libraries like `requests`, `BeautifulSoup`, and `csv`. The script extracts information such as product names, details, SKUs, and image URLs from the website's HTML pages.

## Prerequisites
- Python 3.x
- Required Python libraries: `requests`, `BeautifulSoup`

## Usage
1. Make sure you have Python installed on your system.
2. Install the required Python libraries using pip:
```markdown
   pip install requests beautifulsoup4
   ```
3. Clone or download the script to your local machine.
4. Run the script by executing the following command in your terminal:
```markdown
   python script_name.py
   ```
5. Follow the prompts to input the necessary information.

## Features
- **get_search_results(url):** Retrieves search results from the specified URL.
- **extract_product_links(url):** Extracts product links from the HTML code of the search results page.
- **extract_product_data(url):** Extracts product data from the HTML code of the product page.
- **count_duplicates(img_urls, name, Handle):** Counts duplicate image URLs.
- **write_to_csv(products):** Writes product data to a CSV file.
- **main():** Main function to execute the script.
- **read_lines_from_file(filename):** Reads lines from a file and returns a list of strings.
- **letsgo(SPU):** Function to initiate the scraping process for a given SPU (Stock Keeping Unit).
- **write_to_csv_NotFound(SPU):** Writes SPUs for which product links are not found to a separate CSV file.

## Example
You can run the script with your desired input file containing SPUs to scrape product data. Ensure that the input file contains one SPU per line.

For detailed usage instructions and customization options, refer to the comments within the script.
