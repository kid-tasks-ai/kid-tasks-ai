import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from Exceptions import TasksDBException

class TasksBank:
    def __init__(self, file_path, sheets_names) -> None:
        self.age_keys = []
        self.vect_db_list = []
        self.texts_dict = {}
        self.vectorizer = TfidfVectorizer(max_features=2000)
        self.__init(file_path, sheets_names)

    def get_task_subst(self, age_group: int, game_theme: str) -> str:
        # Transform sentence using the already fitted vectorizer
        msg_vec = self.vectorizer.transform([game_theme])

        # Get relevant to age vectorized array
        age_str = str(age_group)
        idx = 0
        for i in range(len(self.age_keys)-1, -1, -1):
            if age_str in self.age_keys[i]:
                idx = i
                break

        # Compute most fit index
        similarities = cosine_similarity(msg_vec, self.vect_db_list[idx])
        most_relevant_index = np.argmax(similarities)

        # Return the most relevant paragraph
        return self.texts_dict[self.age_keys[idx]][most_relevant_index]

    def __init(self, tasks_filename, sheet_names_str) -> None:
        if not tasks_filename or not sheet_names_str:
            raise TasksDBException(f"Invalid environment variables 'TASKS_FILE' or 'TASKS_LISTS_NAMES'")

        self.age_keys = self.__split_sheets_name(sheet_names_str)
        self.texts_dict = self.__read_texts_from_excel(tasks_filename, self.age_keys)
        
        # Collect all texts to fit the vectorizer
        all_texts = [text for sublist in self.texts_dict.values() for text in sublist]
        self.vectorizer.fit(all_texts)  # Fit the vectorizer once with all texts
        
        self.vect_db_list = self.__build_vect_db(self.texts_dict)


    def __build_vect_db(self, texts_dict: dict) -> list:
        vectorized = []
        for key in texts_dict.keys():
            vectorized.append(self.vectorizer.transform(texts_dict[key]))  # Use transform
        return vectorized

    def __split_sheets_name(self, sheets_names: str) -> list[str]:
        return sheets_names.split(';')

    def __read_texts_from_excel(self, file_path: str, sheet_names: list[str]) -> dict:
        try:
            texts = {}
            for sheet_name in sheet_names:
                # Attempt to read the first column of the Excel file
                data = pd.read_excel(file_path, index_col=0, sheet_name=sheet_name)
                # Convert the dataframe column to a list
                texts[sheet_name] = data.index.to_list()
            return texts
        except FileNotFoundError:
            # raise TasksDBException("Error: The file does not exist. Check the file path.")
            print("Error: The file does not exist. Check the file path.")
        except ValueError as e:
            # raise TasksDBException(f"Error: There was an issue with the file format or reading the file: {e}")
            print(f"Error: There was an issue with the file format or reading the file: {e}")
        except Exception as e:
            # raise TasksDBException(f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")
        