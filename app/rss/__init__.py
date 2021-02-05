from app.blog import BlogReader
from feedgen.feed import FeedGenerator


def generate_rss(site_domain: str,
                 rss_file_path: str,
                 blog_reader: BlogReader):
    blog_list = blog_reader._get_blog_list(n=10, full=True)
    feed_generator = FeedGenerator()

    feed_generator.id(site_domain)
    feed_generator.link(href=site_domain)
    feed_generator.title('帕秋莉的奇妙歷險')
    feed_generator.subtitle('Imaginary City')
    feed_generator.rss_str(pretty=True)

    for item in blog_list[::-1]:
        entry = feed_generator.add_entry()
        url = f'{site_domain}/blog/{item["datetime"]}/{item["filename"]}/'

        entry.id(f'{item["datetime"]}/{item["filename"]}')
        entry.title(item['title'])
        entry.description(item['full'])
        entry.link(href=url)

    feed_generator.rss_file(rss_file_path)
