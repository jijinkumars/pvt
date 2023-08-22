import spacy
import json

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Example paragraph
text = """
Quotation Date:
4/3/2023
Quote Reference:
BDQ 8205 EMF
Contact:
Anica Lompre
Company:
Pivot
Email Address:
alompre@pivotinteriors.com
Rep:
Edgewater Contract - Dean De Gouveia
Specifier:
Pivot
Project Name:
Disneyland INS Building - Pivot
OPTION 1 - NOTED ON CAP SPEC
Textiles Are Approved
Item No.
Quantity
Product/Image (for illustration only)
Specification
Unit List Cost
Total List Cost
Entente Booth High back 2 seater Body: Gr.3 Maharam, Manner – Parakeet
Lumbar: Gr.9 Maharam Lithe – River
ENT/2/OAK
2
Seat: Gr.4 Maharam, Metaphor – Thermosphere
$ 20,774.00
$ 41,548.00
Partition: Gr.3 Maharam, Manner – Parakeet Sofa Leg: Oak Table Top: Oak Laminate Table Base: Oak
Total List
$ 41,548.00
Estimated Net Freight (no discount applicable) to zip code:
90638
$ 3,950.00
Entente Booth High back 2 seater Body: Gr.3 Maharam, Manner – Parakeet Lumbar: Gr.9 Maharam Lithe – River
ENT/2
2
Seat: Gr.4 Maharam, Metaphor –
$ 20,774.00
$ 41,548.00
ALT OPTION- NOT APPROVED
Thermosphere Partition: Gr.3 Maharam, Manner – Parakeet Sofa Leg: Oak Table Top: White Laminate Table Base: Oak
BY CLIENT, YET ** JUST FOR
CLIENT REFERENCE ON
Total List
$ 41,548.00
PRICING ***
Estimated Net Freight (no discount applicable) to zip code:
90638
$ 3,950.00
TABLE TOP FINISHES
Natural Recon Designer White Oak (D354-60) (7996-38)
Freight Quote valid for 60 days after which subject to a 10% Increase. After 120 days must be requoted
Lead Time - 10-12 weeks from High Point NC, from receipt of clean PO.
boss design
"""

doc = nlp(text)

# Initialize variables to store extracted data
extracted_data = {
    "Options": []
}

# Define patterns for detecting section headers
section_headers = [
    "Quotation Date:",
    "Quote Reference:",
    "Contact:",
    "Company:",
    "Email Address:",
    "Rep:",
    "Specifier:",
    "Project Name:",
    "OPTION",
    "TABLE TOP FINISHES",
    "Freight Quote Validity",
    "Lead Time -",
    "boss design",
]

# Initialize variables for storing the current section name and content
current_section = None
current_content = []

# Iterate through the tokens in the processed text
for token in doc:

    if token.text in section_headers:

        if current_section and current_content:

            if isinstance(extracted_data[current_section], list):
                extracted_data[current_section].append("\n".join(current_content))
            else:
                extracted_data[current_section] = "\n".join(current_content)
            current_content = []

        current_section = token.text

    elif current_section:
        current_content.append(token.text)

if current_section and current_content:

    if isinstance(extracted_data.get(current_section), list):
        extracted_data[current_section].append("\n".join(current_content))
    else:
        extracted_data[current_section] = "\n".join(current_content)


for key, value in extracted_data.items():
    if isinstance(value, str):
        extracted_data[key] = "\n".join(line.strip() for line in value.split("\n") if line.strip())

# Print the extracted data as JSON
# print(json.dumps(extracted_data, indent=4))
input_json = json.dumps(extracted_data, indent=4)

print(input_json)
