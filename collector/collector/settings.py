ROBOTSTXT_OBEY = True
USER_AGENT = "Better Informatics Crawler (we are a UoE volunteer student group trying to make DRPS accessible to more folks. To minimize load on your systems, we only crawl 1 page every 10 seconds. We also cache and do not crawl the same page twice. For any questions, please reach out to admin@betterinformatics.com)"
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "spider_cache"
HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
HTTPCACHE_GZIP = True

DOWNLOAD_DELAY = 10

BOT_NAME = "collector"
SPIDER_MODULES = ["collector.spiders"]
NEWSPIDER_MODULE = "collector.spiders"

JOBDIR = "spider_jobs"
