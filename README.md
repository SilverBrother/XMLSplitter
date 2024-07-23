# XMLSplitter
- Python script for splitting big XML files into smaller files. It is optional to maintain potential CDATA syntax from the original XML file.
- Read the comments for clarifications. The default script is set up to output three smaller XML files based on the values from a Zip tag in the original file. 
- Both the range and number of output files can be adjusted inside the script for your convenience.
- Do not apply on XML files you're anything but 100% certain are safe. defusedxml is NOT incorporated in the script.
