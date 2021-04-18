from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Properati(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        total_pages = 1

        while True:
            if page > total_pages:
                break

            logging.info("Requesting %s" % page_link)
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break

            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='StyledCard-n9541a-1 ixiyWf')
            print(properties)
            if page == 1:
                nav_list = page_content.select('#page-wrapper > div.results-content > div.container.wide-listing > div.content > div.row.items-container > div.item-list.span6 > div > div.pagination.pagination-centered > ul > li')
                total_pages = len(nav_list) - 2

            if len(properties) == 0:
                break

            for prop in properties:
                link = prop.find('a', class_='item-url')
                title = link['title']
                price_section = prop.find('p', class_='price')
                if price_section is not None:
                    title = title + ' ' + price_section.get_text().strip()
                href = link['href']
                internal_id = prop.find('a', class_='icon-fav')['data-property_id']

                yield {
                    'title': title,
                    'url': href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                }

            page += 1
            page_link = self.provider_data['base_url'] + source + "/%s/" % page
