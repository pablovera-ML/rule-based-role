import pandas as pd
from unidecode import unidecode


def load_schedules(db_name: str)->pd.DataFrame:
    """ Load DB, in this case is a CSV file."""
    return pd.read_csv(f"./db/{db_name}")

def remove_accents(text: str)->str:
    """Remove accents."""
    return unidecode(text)

def lowercase(text: str)->str:
    """Lowercase strings."""
    return text.lower()


