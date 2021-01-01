import d6tflow
from d6tflow.tasks import TaskCSVPandas, TaskJson
import pandas as pd
from pandas.io.json import json_normalize


class Task_Dual(TaskJson):
    '''
    illustration of adding status information
    '''
    def run(self):
        D = pd.DataFrame({'Test': [1, 2, 3]})

        out = {'dataframe': D.to_json(), 'status': True}

        self.save(out)


if __name__ == "__main__":

    print(d6tflow.preview(Task_Dual()))
    d6tflow.run(Task_Dual())

    out_json = Task_Dual().output().load()['dataframe']
    out = pd.read_json(out_json)

    print(out)