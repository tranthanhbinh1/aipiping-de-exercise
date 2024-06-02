import pandas as pd
import numpy as np
import logging
from typing import Optional
from utils.logging_config import setup_logging

setup_logging()


class FieldsAnalytics:
    def __init__(self) -> None:
        self.df: pd.DataFrame = pd.DataFrame()

    def load_data_from_csv(self, url: str) -> None:
        """
        Loads the data from a CSV file.

        Args:
            url (str): The URL of the CSV file.

        Returns:
            None
        """
        try:
            self.df = pd.read_csv(url)
            logging.info("Data loaded successfully!")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")

    def write_data_to_csv(self, url: str) -> None:
        """
        Writes the data to a CSV file.

        Args:
            url (str): The URL of the CSV file.

        Returns:
            None
        """
        if not self.df.empty:
            try:
                self.df.to_csv(url, index=False)
                logging.info("Data written to CSV successfully!")
            except Exception as e:
                logging.error(f"Failed to write data to CSV: {e}")

    def get_data_info(self) -> None:
        """
        Gets information about the data.

        Returns:
            None
        """
        if not self.df.empty:
            logging.info(self.df.info())
        else:
            logging.error("No data available!")

    def transform_data(self) -> None:
        """
        Transforms the data.

        Returns:
            None
        """
        if not self.df.empty:
            # Map Associate degree to Level and Level name
            self.df["level"] = np.where(
                self.df["field_of_study"].str.contains(
                    "^Associate", na=False, case=False
                ),
                "associate",
                self.df["level"],
            )
            # Fill level_name with level where level exist

            self.df["level_name"] = self.df["level_name"].fillna(self.df["level"])

            # Remove tuples that have nan in level and level_name
            # Number of records before dropna
            before_dropna = len(self.df)

            self.df = self.df.dropna(subset=["level", "level_name"]).reset_index(
                drop=True
            )

            # After dropna
            after_dropna = len(self.df)

            # Difference after dropna
            dif = before_dropna - after_dropna
            logging.info(
                f"After cleaning process, {dif} records were removed. A difference of {round(dif/before_dropna, 4)*100} percent."
            )

            # Mapping ratio - ratio of the records that have academic_field filled, compared to total records
            mapping_ratio = round(self.df["academic_field"].count() / len(self.df),4)*100
            logging.info(f"Mapping ratio: {mapping_ratio} percent.")

        else:
            logging.error("No data available!")


if __name__ == "__main__":
    fields_analytics = FieldsAnalytics()
    fields_analytics.load_data_from_csv("test_data/field_of_study_exercise.csv")
    fields_analytics.get_data_info()
    fields_analytics.transform_data()
    fields_analytics.write_data_to_csv("test_data/fields_data_transformed.csv")
    logging.info("Fields data transformation completed!")
