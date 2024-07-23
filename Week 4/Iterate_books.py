from xml.etree.cElementTree import iterparse

def books(file):
    for event, elem in iterparse(file):
        if event == 'start' and elem.tag == 'root':
            # This will set `books` to the root element, but `books` is not used further
            # If you need to use the `books` variable, you should define it outside the loop
            pass
        elif event == 'end' and elem.tag == 'book':
            # Print book details
            print('{0}, {1}, {2}, {3}, {4}'.format(
                elem.findtext('title'),
                elem.findtext('publisher'),
                elem.findtext('numberOfChapters'),
                elem.findtext('pageCount'),
                elem.findtext('author')
            ))
            elem.clear()  # Clear the element to save memory
        elif event == 'end' and elem.tag == 'chapter':
            # Print chapter details
            print('{0}, {1}, {2}'.format(
                elem.findtext('chapterNumber'),
                elem.findtext('chapterTitle'),  # Note the corrected tag name 'chapterTitle'
                elem.findtext('pageCount')
            ))
            elem.clear()  # Clear the element to save memory

if __name__ == '__main__':
    with open("books.xml", "r") as file:
        books(file)
