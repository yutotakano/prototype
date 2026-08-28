import re
from pathlib import Path

import scrapy
from scrapy.http import Response


class DRPSSpider(scrapy.Spider):
    name = "drps"

    async def start(self):
        urls = ["https://www.drps.ed.ac.uk/26-27/index.php"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response):
        # Save the response body to a file based on URL (removing .php)
        url_path = Path(response.url.split("ac.uk/")[-1].replace(".php", ""))
        url_path = Path("data") / url_path  # Prepend "data" to the path

        # Create the directory if it doesn't exist
        url_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the response body to a file
        file_path = url_path.with_suffix(".html")
        with open(file_path, "wb") as f:
            f.write(response.body)

        year = re.search(r"(\d{2}-\d{2})", response.url)
        if year:
            year = year.group(1)
        # If we are at a year's index (and not any other sub-index), follow:
        # Browse DPTs
        # Browse courses by School
        # Browse couses by Subject Area
        if re.search(r"www\.drps\.ed\.ac\.uk/\d{2}-\d{2}/index\.php$", response.url):
            yield scrapy.Request(
                url=f"http://www.drps.ed.ac.uk/{year}/dpt/drpsindex.htm",
                callback=self.parse,
            )
            yield scrapy.Request(
                url=f"http://www.drps.ed.ac.uk/{year}/dpt/cx_schindex.htm",
                callback=self.parse,
            )
            yield scrapy.Request(
                url=f"http://www.drps.ed.ac.uk/{year}/dpt/cx_subindex.htm",
                callback=self.parse,
            )
            return

        # Follow links to other pages and yield requests for them
        for link in response.css("a::attr(href)").getall():
            # Only follow links that are within the drps.ed.ac.uk domain
            # when resolved
            resolved = response.urljoin(link)
            if (
                "drps.ed.ac.uk/" in resolved
                and not "/current/" in resolved
                and (resolved.endswith((".php", "/", ".htm")))
            ):
                yield response.follow(link, callback=self.parse)
