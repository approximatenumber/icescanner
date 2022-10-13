import os
import warnings

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from icescanner.logger import Logger

logger = Logger.get_logger("dataset-recorder")


warnings.filterwarnings('ignore')

def is_dataset_valid(filepath: str) -> bool:
    """_summary_

    Args:
        filepath (str): _description_

    Returns:
        _type_: _description_
    """
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
