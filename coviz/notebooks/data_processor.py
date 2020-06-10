# Copyright 2020 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import numpy as np
import math


class DataProcessor:
    def __init__(self, dict_data, pops, name, name_to_ID, add_world_data=False):
        self.STDT = dict_data["Cases"].index[0]
        self.ENDT = dict_data["Cases"].index[-1]
        self.dict_data = dict_data
        self.pops = pops
        self.name = name
        self.name_to_ID = name_to_ID
        self.ID_to_name = {v: k for k, v in name_to_ID.items()}
        if add_world_data:
            self.add_world()
        # normalized by pop
        self.dict_data_pop = {}
        for key in self.dict_data.keys():
            self.dict_data_pop[key] = (
                1e6
                * self.dict_data[key]
                .divide(pops["2018"])
                .loc[:, self.dict_data[key].columns.values]
            )

    def get_ts(self, country_name, data, norm, scale, data_type, ma, n):
        if country_name:
            if norm == "Per million":
                ts = self.dict_data_pop[data].loc[:, country_name]
            else:
                ts = self.dict_data[data].loc[:, country_name]
        else:
            if norm == "Per million":
                ts = self.dict_data_pop[data]
            else:
                ts = self.dict_data[data]

        if data_type == "Daily % change":
            ts = 100 * ts.pct_change()

        if data_type == "Daily change":
            ts = ts.diff()

        ts = ts.replace({np.inf: math.nan, -np.inf: math.nan})

        if ma:
            ts = ts.rolling(window=n).mean()

        if scale == "Log":
            ts = ts.where(ts > 1e-10, math.nan)

        return ts

    def get_ts_plot(
        self, country_name, data, norm, scale, data_type, ma, n, date1, date2
    ):
        return self.get_ts(country_name, data, norm, scale, data_type, ma, n).loc[
            date1:date2
        ]

    def get_columns(self, data):
        return self.dict_data[data].columns.values

    def get_value(self, country_name, data, norm, scale, data_type, ma, n, date):
        return self.get_ts(country_name, data, norm, scale, data_type, ma, n).loc[date]

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

    def get_ts_sort(self, data, norm, scale, data_type, ma, n, date, ascending, K):
        if K:
            return (
                self.get_ts(None, data, norm, scale, data_type, ma, n)
                .loc[date]
                .sort_values(ascending=ascending)[:K]
            )
        else:
            return (
                self.get_ts(None, data, norm, scale, data_type, ma, n)
                .loc[date]
                .sort_values(ascending=ascending)
            )

    def add_world(self):
        for key in self.dict_data.keys():
            self.dict_data[key]["WLD"] = self.dict_data[key].sum(axis=1)
        return
