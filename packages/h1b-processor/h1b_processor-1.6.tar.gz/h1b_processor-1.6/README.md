# Data Cleaner 

Data Cleaner is a Python package for cleaning data frames that you obtain from h1bdata.info to find potential employers that can sponsor

## Installation

You can install the package using pip:

```bash
pip install cleanh1b 


usage

from clean_h1b import data_cleaner

# Load your DataFrame
keyword='data engineer'

# Create an instance of data_cleaner
processor = data_cleaner(keyword)

# Process the DataFrame
processed_df = processor.process()

# Display the processed DataFrame
print(processed_df)

