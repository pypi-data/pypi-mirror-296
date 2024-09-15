## Curious Varvara

Tiny package to check website availability

### Installation

```bash
pip install curious-varvara
```

### Usage

```python
from curious_varvara as cv

url = 'https://www.google.com'

cv.is_live(url) # returns True if website is available, False otherwise

cv.body_md5(url) # returns md5 hash of website body
```
