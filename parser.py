import csv
import urllib2
from bs4 import BeautifulSoup


def get_page_info(page_num):
    """
    Get html markup from the url
    :param page_num: Integer: page number that need to fetch
    :return: String: html markup
    """
    page = urllib2.urlopen('https://ocs.ca/collections/all-cannabis-products?page=%s' % page_num)
    if page.getcode() == 200:
        return page.read()
    else:
        raise Exception('Error %s' % page.getcode())


def get_products_html(page):
    """
    Get array of html markup products
    :param page: String: html markup of the page
    :return: Array: array of html markup products
    """
    soup = BeautifulSoup(page, 'html.parser')
    prods = []
    for prod in soup.find_all('article', class_='product-tile'):
        prods.append(prod)
    return prods


def get_products():
    """
    Get all html markup products from the site
    :return: Array: array of all html markup products
    """
    to_parse = True
    i = 1
    p_array = []
    while to_parse:
        products = get_products_html(get_page_info(i))
        if products:
            for prod in products:
                p_array.append(prod)
            i += 1
        else:
            to_parse = False
    return p_array


def parse_products():
    """
    Parse array of html markup products
    :return: Array: array of products
    """
    prod_arr = [['vendor', 'title', 'price', 'properties']]
    for prod in get_products():
        vendor = prod.find('h4', class_='product-tile__vendor').text.strip()
        title = prod.find('h3', class_='product-tile__title').text.strip()
        price = prod.find('p', class_='product-tile__price').text.strip()
        properties = ', '.join('%s %s' % (prop.find('h4').text.strip(), prop.find('p').text.strip()) for prop in
                               list(prod.find('ul', class_='product-tile__properties').children))
        prod_arr.append([vendor, title, price, properties])

    return prod_arr


def save_to_csv(products):
    """
    Function that saves array of products to file
    :param products: Array: array of parsed products
    """
    with open('products.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(products)


if __name__ == '__main__':
    save_to_csv(parse_products())
