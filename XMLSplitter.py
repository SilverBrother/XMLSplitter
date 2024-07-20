import xml.etree.ElementTree as ET
from lxml import etree
import os
import shutil


# Function to create an XML tree with a root element
def create_xml_tree(root_tag):
    root = ET.Element(root_tag)
    return ET.ElementTree(root), root


# Function to create an XML tree with a root element using lxml
def create_xml_etree(root_tag):
    root = etree.Element(root_tag)
    tree = etree.ElementTree(root)
    return tree, root


def split_options(input_filepath, output_dir, option):
    """
    Splits the input XML file into separate files based on zip code ranges and saves them to the specified output directory.

    Parameters:
    - input_filepath: Path to the input XML file.
    - output_dir: Directory where the output files will be saved.
    - option: Determines whether to preserve CDATA sections (0) or not (1).

    XML file structure:
    <Main>
        <Head>
            <Etc>
            </Etc>
        </Head>
        <Data>
            <Register>
                <Generic1>Value</Generic1>
                <Generic2>Value</Generic2>
                <Generic3>Value</Generic3>
                    <Adr>
                        <MoreGeneric1>Value</MoreGeneric1>
                        <Zip>Value</Zip>
                    </Adr>
                <Generic4>Value</Generic4>
            </Register>
        </Data>
    </Main>
    """

    if option == 0:
        # Parse the input XML file while preserving CDATA sections
        # Uses lxml
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(input_filepath, parser)
        root = tree.getroot()
        create_tree_func = create_xml_etree
        # This lambda function takes an XML tree and a file path as arguments and writes the XML tree to the file.
        write_func = lambda tree, path: tree.write(path, encoding='utf-8', xml_declaration=True, pretty_print=True)

    elif option == 1:
        # Parse the input XML file regularly
        # Uses xml.etree
        tree = ET.parse(input_filepath)
        root = tree.getroot()
        create_tree_func = create_xml_tree
        # This lambda function also takes an XML tree and a file path as arguments and writes the XML tree to the file.
        write_func = lambda tree, path: tree.write(path, encoding='utf-8', xml_declaration=True)

    else:
        print("Option must be 0 or 1.")
        return

    # Define zip code ranges and corresponding filenames in this dictionary
    zip_ranges = {
        (0, 3000): 'zips_0_3000.xml',
        (3001, 6000): 'zips_3001_6000.xml',
        (6001, 9999): 'zips_6001_9999.xml'
    }

    # Create new XML trees for each zip code range
    # Apply the tag that "Head" and "Data" is an element off
    trees = {range_key: create_tree_func("Main") for range_key in zip_ranges.keys()}

    # Iterate over each Register element
    for register in root.findall('.//Register'):
        # Find the Zip element
        zip_element = register.find('.//Adr/Zip')
        if zip_element is not None:
            try:
                zip_value = int(zip_element.text)
                # Iterate over each zip code range and its corresponding tree
                # trees.items(): Returns an iterator of the dictionary's key-value pairs.
                for range_key, (tree, tree_root) in trees.items():
                    if range_key[0] <= zip_value <= range_key[1]:
                        if option == 0:
                            zip_element.text = f"<![CDATA[{zip_element.text}]]>"
                        tree_root.append(register)
                        break
            except ValueError:
                print(f"ValueError encountered with zip value: {zip_element.text.strip()}")
        else:
            print("element is None")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each zip code range and corresponding filename
    for range_key, filename in zip_ranges.items():
        # Retrieve the XML tree and root for the current zip code range
        tree, tree_root = trees[range_key]
        if option == 1:
            # Only xml.etree offers this option for indentation
            ET.indent(tree, '  ')
        # Write the XML tree to the specified output file using the write function
        write_func(tree, os.path.join(output_dir, filename))


def main():
    input_filepath = r'Name and/or path to the input XML file'
    # Remove 'r' if you are not a Windows user
    output_dir = r'C:\Path\to\output_folder\Output'

    option = input("Do you want to split the XML with CDATA intact (0) or not (1)?:").strip().lower()
    if option not in ['0', '1']:
        print("Invalid option. Please enter 0 or 1.")
        return

    option = int(option)

    # Check if the output directory exists
    if os.path.exists(output_dir):
        # Prompt the user for overwrite permission
        response = input(
            f"The directory '{output_dir}' already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Exiting without overwriting the directory.")
            return
        else:
            # Clear the existing directory
            shutil.rmtree(output_dir)

    split_options(input_filepath, output_dir, option)


if __name__ == '__main__':
    main()
