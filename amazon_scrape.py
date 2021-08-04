def get_url(search_term):
    """Generate a url from search term"""
    template = "https://www.amazon.com/s?k={}&crid=1AU02VKAA00X0&sprefix=ultra%2Caps%2C198&ref=nb_sb_ss_ts-doa-p_1_7"
    search_term = search_term.replace(" ", "+")

    # add term query
    url = template.format(search_term)

    # add pagequery placeholder
    # url += '&page{}'
    url += '&page={}&ref=sr_pg_{}'

    return url


def extract_record(item):
    """ Extract and return record from a single record"""

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    # print(description)
    # price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:

        # rating
        rating = item.i.text

        # review count
        review_count = item.find('span', 'a-size-base').text.replace(",", "")
    except AttributeError:
        rating = ' '
        review_count = ' '

    result = (description, price, rating, review_count, url)

    return result


