import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Create an XML structure
root = ET.Element("root")
book = ET.SubElement(root, "book")
name = ET.SubElement(book, "name")
name.text = "Book1"

# Convert the XML tree to a string
xml_str = ET.tostring(root, encoding='utf-8')

# Parse the XML string with minidom and prettify the output
parsed_xml = minidom.parseString(xml_str)
pretty_xml = parsed_xml.toprettyxml(indent="    ")

print(pretty_xml)
