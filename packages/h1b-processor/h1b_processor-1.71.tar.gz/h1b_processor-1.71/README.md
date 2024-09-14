# Data Cleaner 

Data Cleaner is a Python package for cleaning data frames that you obtain from h1bdata.info to find potential employers that can sponsor

## Installation

You can install the package using pip:

```bash
pip install h1b-processor

from clean_h1b import data_cleaner

# Create an instance of data_cleaner
processor = data_cleaner(keywords = 'data')

# Process the DataFrame
processed_df = processor.process()

# Display the processed DataFrame
print(processed_df)

