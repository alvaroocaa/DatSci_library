import pandas as pd
import random
import datsci as dt


def test_datsci():

    fruits = [random.choice(['apple', 'pineapple', 'pear', 'melon', 'watermelon']) for _ in range(200)]
    fruit_consumption = [random.randint(1, 500) for _ in range(200)]

    df_fruits = pd.DataFrame({
        'Fruits': fruits,
        'Fruits consumption': fruit_consumption
    })
    a=['apple', 'pineapple', 'pear', 'melon', 'watermelon']
    df = dt.table_count(df_fruits, a, 'Fruits consumption')
    return df

test_datsci()
