import urllib
from bs4 import BeautifulSoup
import sys

# for arg in sys.argv:
#     print(arg)

input_file_name = '/home/ldeng/quark_web/quarkchain-dev/web/explorer/templates/explorer/balance.html'
# output_file_name = sys.argv[2]

# input_file = open('/home/valentin/development/cheerfy/frontend.cheerz.co/frontend/templates/index.html', 'r+')
input_file = open(input_file_name, 'r+')

html = input_file.read()
input_file.close()

html_cleaned = html.replace('{%', '<script>')
html_cleaned = html_cleaned.replace('%}', '</script>')
html_cleaned = html_cleaned.replace('{{', '<script>')
html_cleaned = html_cleaned.replace('}}', '</script>')

soup = BeautifulSoup(html_cleaned, "html5lib")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()  # rip it out

# get text
text = soup.get_text()
# print("text=" + text)
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
with_titles = soup.find_all(title=True)
# print(*with_titles)
titles = list(t.get('title') for t in with_titles)
# print("titles=" + '\n'.join(titles))
lst = list(titles)


refused_set = []
replacement_set = {}
replacement_list = []
key_set = text.split('\n') + lst
print("key_set=" + '\n'.join(key_set))
for entry in key_set:
    print("entry=" + entry)
    skip = False
    if entry in replacement_set:
        option = input(
            'Your entry:\n\t\t' + entry + '\n\tAlready stored with key: ' + replacement_set.get(entry) +
            '\n\tDo you want to keep same entry [1] or create a new one [2]? ')
        skip = True if option == '1' else False
    if not skip and entry not in refused_set:
        key_id = input('Your entry:\n\t\t' + entry + '\n\t - (d) to discard: ')
        if key_id != 'd':
            replacement_set[entry] = entry
            replacement_list.append(entry)
            replacement_text = "{% trans '" + entry + "' %}"
            print("replacement_text=" + replacement_text)
            html = html.replace(entry, replacement_text)
        else:
            refused_set.append(entry)

# translation_content = ''
# for entry in replacement_list:
#     replacement_text = "{% trans '" + entry + "' %}"
#     print("replacement_text=" + replacement_text)
#     html = html.replace(entry, replacement_text)
    # translation_content += 'msgid "' + str(replacement_set.get(entry).encode('utf-8')) + \
    #                        '"\nmsgstr "' + str(entry.encode('utf-8').strip()) + '"\n'

# 1) empty input file
# input_file = open(input_file_name, 'wb').close()

# 2) update input file with new content
input_file = open(input_file_name, 'wb')
soup = BeautifulSoup(html, "html.parser")
html = soup.prettify()
input_file.write(html.encode('utf-8'))
input_file.flush()
input_file.close()

# 3) update output file with new records
# output_file = open(output_file_name, 'a')
# output_file.write(translation_content)
# output_file.flush()
# output_file.close()
