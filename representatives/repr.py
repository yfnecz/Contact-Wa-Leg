import pandas as pd
import os

class DistrictRepresentatives:
    def __init__(self):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, "Members-2025-06-04.csv")
        self.df = pd.read_csv(file_path)
        self.df['District'] = self.df['District'].astype(str).str.strip()

    def get_representatives(self, district_number):
        """
        Returns a list of dictionaries with representative info for the given district.
        """
        district_number = str(district_number).strip()
        reps = self.df[self.df['District'] == district_number]

        if reps.empty:
            return []

        return [
            {
                'name': row['Member Name'],
                'email': row['Email'],
                'chamber': row['Chamber'],
                'position': row['Position'],
                'party': row['Party'],
                'phone': row['Phone'],
                'la': row['Legislative Assistant'],
                'la_email': row['LA Email']
            }
            for _, row in reps.iterrows()
        ]
