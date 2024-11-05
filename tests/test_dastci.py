import pandas as pd
import random
from datsci import myfunctons


def test_datsci():

    fruits = [random.choice(['apple', 'pineapple', 'pear', 'melon', 'watermelon']) for _ in range(200)]
    fruit_consumption = [random.randint(1, 500) for _ in range(200)]

    df_fruits = pd.DataFrame({
        'Fruits': fruits,
        'Fruits consumption': fruit_consumption
    })

    assert myfunctons.table_count(df_fruits, ['apple', 'pineapple', 'pear', 'melon', 'watermelon'], 'Fruits consumption')

test_datsci
