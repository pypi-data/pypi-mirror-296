import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from tqdm import tqdm  # Importing tqdm for the progress bar

class data_cleaner:
    def __init__(self, *, keywords=None):
        self.keywords = keywords
        self.progress_bar = tqdm(total=100, desc="Processing", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} {percentage:3.0f}%")

    def process(self):
        # Step 1: Preparing the URL
        self.progress_bar.update(10)  # Update progress by 10%
        keyword = '+'.join(self.keywords.split())
        url = 'https://h1bdata.info/index.php?em=&job={}&city=&year=All+Years'.format(keyword)

        # Step 2: Sending request
        self.progress_bar.update(20)  # Update progress by 20%
        data = requests.get(url)

        if data.status_code == 200:
            # Step 3: Parsing HTML
            self.progress_bar.update(20)  # Update progress by 20%
            soup = BeautifulSoup(data.content, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(StringIO(str(table)))[0]

            # Step 4: Data Cleaning
            self.progress_bar.update(20)  # Update progress by 20%
            try:
                df.pop('Unnamed: 6')
            except KeyError:
                pass

            df['year'] = df['START DATE'].str.strip().str[-4:]
            df['state'] = df['LOCATION'].str.strip().str[-2:]
            df = df.dropna()

            # Step 5: Removing Ads
            self.progress_bar.update(20)  # Update progress by 20%
            try:
                df = self._remove_adsbygoogle(df)
            except Exception:
                pass

            # Step 6: Final Cleaning and Return
            df['BASE SALARY'] = pd.to_numeric(df['BASE SALARY'])
            df['year'] = pd.to_numeric(df['year'])

            self.progress_bar.update(10)  # Final progress update
            self.progress_bar.close()

            if len(df) > 0:
                return df
            else:
                return f'this keyword returned 0 rows of data, try the link manually <{url}>'
        else:
            print(f'Keyword is not valid, try this link manually <{url}>')
            self.progress_bar.close()

    def _remove_adsbygoogle(self, df):
        pattern_clean = ".adsbygoogle."
        filter = df['EMPLOYER'].str.contains(pattern_clean)
        df = df[~filter]
        return df