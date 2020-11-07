from lxml import html

input_filename = "names.html"
output_filename = "names.txt"
xpath = "/html/body/div[1]/div/div/main/article/section/ol[1]/li"
names = []


def parse():
    root = html.parse(input_filename).getroot()
    for li in root.xpath(xpath):  # li[index]/a
        names.append(li.xpath('a')[0].text_content())
    print('parse(): ok')


def print_to_file():
    file = open(output_filename, 'w+')
    file.write('\n'.join(names))
    print('print(): ok')


if __name__ == '__main__':
    parse()
    print_to_file()
