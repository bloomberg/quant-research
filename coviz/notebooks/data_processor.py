import pandas as pd
import numpy as np
import math


class DataProcessor:
    def __init__(self, dict_data, pops, name, name_to_ID):
        self.STDT = dict_data["Cases"].index[0]
        self.ENDT = dict_data["Cases"].index[-1]
        self.dict_data = dict_data
        self.pops = pops
        self.name = name
        self.name_to_ID = name_to_ID
        self.ID_to_name = {v: k for k, v in name_to_ID.items()}
        # normalized by pop
        self.dict_data_pop = {}
        for key in self.dict_data.keys():
            self.dict_data_pop[key] = 1e6 * self.dict_data[key].divide(pops["2018"])

    def get_ts(self, country_name, data, norm, scale, data_type):
        if country_name:
            if norm == "Per 1MPop":
                ts = self.dict_data_pop[data].loc[:, country_name]
            else:
                ts = self.dict_data[data].loc[:, country_name]
        else:
            if norm == "Per 1MPop":
                ts = self.dict_data_pop[data]
            else:
                ts = self.dict_data[data]

        if data_type == "Daily % change":
            ts = 100 * ts.pct_change()

        if data_type == "Daily change":
            ts = ts.diff()

        ts = ts.replace({np.inf: math.nan, -np.inf: math.nan})

        if scale == "Log":
            ts = ts.where(ts > 0, math.nan)

        return ts

    def get_ts_plot(self, country_name, data, norm, scale, data_type, date1, date2):
        return self.get_ts(country_name, data, norm, scale, data_type).loc[date1:date2]

    def get_columns(self, data):
        return self.dict_data[data].columns.values

    def get_value(self, country_name, data, norm, scale, data_type, date):
        return self.get_ts(country_name, data, norm, scale, data_type).loc[date]

    def get_population(self, country_name):
        return self.pops.loc[country_name]["2018"]

    def get_index(self, data):
        return list(self.dict_data[data].index.values)

    def get_len(self):
        return self.dict_data["Cases"].shape[0]

    def get_ID(self, name):
        return self.name_to_ID[name]

    def get_name(self, ID):
        return self.ID_to_name[ID]

    def get_ts_sort(self, data, norm, scale, data_type, date, ascending, K):
        return (
            self.get_ts(None, data, norm, scale, data_type)
            .loc[date]
            .sort_values(ascending=ascending)[:K]
        )
