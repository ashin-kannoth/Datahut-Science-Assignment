## Overview
This project scrapes product data from Puma India’s Women’s Footwear category.

## Tools Used
- Python
- Playwright (for JavaScript rendering)
- BeautifulSoup
- pandas

## Approach
The Puma website loads prices dynamically via JavaScript. Playwright was used to render the page, after which BeautifulSoup parsed the rendered HTML to extract product URLs, names, brand, Sale Price, and MRP.

## Pagination
Pagination was handled by iterating page numbers using the `?page=` parameter until no product cards were found.

## Challenges
Prices were not available in static HTML.

## How It Was Handled
Browser automation via Playwright was used to ensure accurate price extraction.

## Output
The final dataset is stored in `dataset.csv` with duplicate products removed.
