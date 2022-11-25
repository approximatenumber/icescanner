import warnings
from typing import Dict
import pandas as pd
from icescanner.logger import Logger

logger = Logger.get_logger("dataset-recorder")


warnings.filterwarnings('ignore')

def is_dataset_valid(filepath: str, config: Dict) -> bool:
    """Input filter

    Args:
        filepath (str): path to dataset

    Returns:
        bool: is dataset valid for further processing
    """
    config = config  # now config is available
    df1 = pd.read_csv(filepath)
    df1.drop(['Time'],axis=1,inplace=True)
    if ((df1[lambda x: ((x['//X']<=4.34) & (x['//X']>=1.3))]['Inten-sity'].mean()>20) and ((df1[lambda x: ((x['//X']<=4.34) & (x['//X']>=1.3))]['Inten-sity'].mean()<60))):
        if ((df1[lambda x: ((x['//X']<=7.38) & (x['//X']>4.34))]['Inten-sity'].mean()>20) and (df1[lambda x: ((x['//X']<=7.38) & (x['//X']>4.34))]['Inten-sity'].mean()<60)):
            if ((df1[lambda x: ((x['//X']<10.42) & (x['//X']>7.38))]['Inten-sity'].mean()>15) and (df1[lambda x: ((x['//X']<10.42) & (x['//X']>7.38))]['Inten-sity'].mean()<35)):
                if df1.count()[0]>50000:
                    logger.info(f"{filepath} is good enough!")
                    return True
    logger.warning(f"{filepath} is not valid for further processing!")
    return False
