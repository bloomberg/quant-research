import pandas as pd
import numpy as np
import itertools
import math

class PrettyBreaks:
    def __init__(self, area=None):
        if area:
            self.area = True
            pd_area = pd.read_csv(area, delimiter=";", index_col=0)
            pd_area["mercator area"] = pd_area["area"] / (
                np.cos(np.pi * pd_area["Latitude (average)"] / 180) ** 2
            )
            self.areas = pd_area
        else:
            self.area = False

    @staticmethod
    def round_values_generator(a, b, n):
        level_1_units = [0, 1, 5, 2, 2.5, 4, 6, 8, 7.5, 9, 3, 7]
        level_1_values = [
            0.1,
            0.25,
            0.5,
            0.8,
            0.9,
            0.95,
            0.95,
            0.95,
            0.975,
            0.9875,
            0.9875,
            0.99375,
        ]
        dict_unit_values = dict(zip(level_1_units, level_1_values))
        dict_roundness_score = {}

        if b == 0:
            unit_b = 0
        else:
            unit_b = int(np.abs(b) // (10 ** (np.ceil(np.log10(np.abs(b)) - 1))))

        if a == 0:
            unit_a = 0
        elif b != 0 and np.ceil(np.log10(np.abs(a))) == np.ceil(np.log10(np.abs(b))):
            unit_a = int(np.abs(a) // (10 ** (np.ceil(np.log10(np.abs(a))) - 1)))
        else:
            unit_a = 0

        primary_units = [
            i
            for i in level_1_units
            if (i >= min(np.abs(a), np.abs(b)) and i <= max(np.abs(a), np.abs(b)))
            or (i >= unit_a and i <= unit_b)
        ]
        res = []
        count_primary = 0
        count_level_2 = 0
        iterations = 0
        power = -1
        products = sorted(
            list(itertools.product(level_1_units, repeat=np.abs(power) + 1)),
            key=lambda x: np.sum(
                [dict_unit_values[val_aux] + p for p, val_aux in enumerate(x)]
            ),
        )

        while len(dict_roundness_score.keys()) < n or iterations < len(
            level_1_units
        ):  # or count_level_2 != len(level_1_units)**(np.abs(power) + 1) - 1:
            if iterations < len(level_1_units):
                unit = level_1_units[iterations]
            else:
                unit_1 = primary_units[count_primary]
                unit = round(
                    np.sum(
                        [
                            products[count_level_2][i] * 10 ** (-i)
                            for i in range(np.abs(power) + 1)
                        ]
                    ),
                    np.abs(power) + 2,
                )
            # print('current unit ', unit)
            if PrettyBreaks.power_is_in_range(unit, a, b):
                aux = PrettyBreaks.power_in_range(unit, a, b)
                for val in aux:
                    if round(val, np.abs(power) + 2) not in dict_roundness_score.keys():
                        if iterations < len(level_1_units):
                            dict_roundness_score[val] = dict_unit_values[unit]
                        else:
                            dict_roundness_score[
                                round(val, np.abs(power) + 1)
                            ] = np.sum(
                                [
                                    dict_unit_values[val_aux] + p
                                    for p, val_aux in enumerate(products[count_level_2])
                                ]
                            )
            if (
                count_level_2 == len(level_1_units) ** (np.abs(power) + 1) - 1
                and count_primary == len(primary_units) - 1
            ):
                count_level_2 = 0
                count_primary = 0
                power -= 1
                products = sorted(
                    list(itertools.product(level_1_units, repeat=np.abs(power) + 1)),
                    key=lambda x: np.sum(
                        [dict_unit_values[val_aux] + p for p, val_aux in enumerate(x)]
                    ),
                )
            elif (
                count_level_2 == len(level_1_units) ** (np.abs(power) + 1) - 1
                and count_primary < len(primary_units) - 1
            ):
                count_level_2 = 0
                count_primary += 1
            elif count_level_2 < len(level_1_units) ** (np.abs(power) + 1) - 1:
                count_level_2 += 1
            iterations += 1
        return dict_roundness_score

    def area_sum(self, countries, array=True):
        if array:
            return self.areas.loc[self.areas.index.intersection(countries)].sum()[
                "mercator area"
            ]
        else:
            return self.areas.loc[
                self.areas.index.intersection(countries.index.values)
            ].sum()["mercator area"]

    @staticmethod
    def power_is_in_range(unit, a, b):
        if unit == 0:
            return a <= 0 and b >= 0
        if unit == a or unit == b:
            return True
        if (
            PrettyBreaks.boundaries(unit, a)[1] <= b
            and PrettyBreaks.boundaries(unit, b)[0] >= a
        ):
            return True

        return False

    @staticmethod
    def power_in_range(unit, a, b):

        if unit == 0:
            if a <= 0 and b >= 0:
                return [0]
            else:
                return []

        if a < 0 and b <= 0:
            return list(
                -1
                * np.array(
                    PrettyBreaks.power_in_range(unit, np.abs(b), np.abs(a))[::-1]
                )
            )
        elif a < 0 and b > 0:
            return (
                list(
                    -1
                    * np.array(
                        PrettyBreaks.power_in_range(
                            unit, min(np.abs(a), np.abs(b)), max(np.abs(a), np.abs(b))
                        )[::-1]
                    )
                )
                + list(
                    -1
                    * np.array(
                        PrettyBreaks.power_in_range(unit, 0, min(np.abs(a), np.abs(b)))[
                            ::-1
                        ]
                    )
                )
                + PrettyBreaks.power_in_range(unit, 0, min(np.abs(a), np.abs(b)))
                + PrettyBreaks.power_in_range(
                    unit, min(np.abs(a), np.abs(b)), max(np.abs(a), np.abs(b))
                )
            )

        if a != 0:
            n = int(np.log10(np.abs(a) / unit))
        else:
            n = min(0, int(np.log10(np.abs(b) / unit)) - 2)
        current_res = PrettyBreaks.power_10_unit(unit, n)
        res = []
        if current_res >= a and current_res <= b:
            res.append(current_res)
        n += 1
        current_res = PrettyBreaks.power_10_unit(unit, n)
        while current_res >= a and current_res <= b:
            res.append(current_res)
            n += 1
            current_res = PrettyBreaks.power_10_unit(unit, n)
        return res

    @staticmethod
    def compartment_score(n1, n2, ratio, area=False, n2_unique=np.inf):
        if n1 == 0 or n2 == 0 or (not area and n2_unique < int(1.0 / ratio)):
            return np.inf
        else:
            return np.abs(ratio - n1 / n2)

    @staticmethod
    def normalized_distance(qt, pretty_val):
        return np.abs(qt - pretty_val) / np.abs(qt)

    @staticmethod
    def power_boundaries(unit, value):
        if value > 0:
            return [
                math.ceil(math.log(value / unit, 10)) - 1,
                math.ceil(math.log(value / unit, 10)),
            ]
        elif value < 0:
            return [
                math.ceil(math.log(np.abs(value) / unit, 10)),
                math.ceil(math.log(np.abs(value) / unit, 10)) - 1,
            ]
        else:
            return [0, 0]

    @staticmethod
    def power_10_unit(unit, power):
        return unit * 10 ** power

    @staticmethod
    def boundaries(unit, value):
        a1, a2 = PrettyBreaks.power_boundaries(unit, value)
        if a1 == a2:
            return [-unit, unit]
        else:
            return [
                np.sign(value) * PrettyBreaks.power_10_unit(unit, a1),
                np.sign(value) * PrettyBreaks.power_10_unit(unit, a2),
            ]

    @staticmethod
    def closest_power_10_unit(unit, value):
        bnd = PrettyBreaks.boundaries(unit, value)
        return bnd[np.argmin(np.abs(np.ones(2) * value - bnd))]

    def pretty_break_quant(self, values, quantile, ratio, weights=[1, 1, 1], n_gen=40):
        qt = values.quantile(quantile)
        current_score = np.inf
        res = None
        dict_unit_val = PrettyBreaks.round_values_generator(
            min(values), max(values), n_gen
        )
        for pretty_val in dict_unit_val.keys():
            unit_score = dict_unit_val[pretty_val] * weights[0]
            n1 = (values < pretty_val).sum()
            n2 = (values >= pretty_val).sum()
            n2_unique = values[values >= pretty_val].nunique()
            unit_score += (
                PrettyBreaks.compartment_score(n1, n2, ratio, n2_unique=n2_unique)
                * weights[1]
            )
            if self.area and weights[2] > 0:
                n1_area = self.area_sum(values[values < pretty_val].index.values)
                n2_area = self.area_sum(values[values >= pretty_val].index.values)
                unit_score += (
                    PrettyBreaks.compartment_score(n1_area, n2_area, ratio, True)
                    * weights[2]
                )
            if unit_score < current_score:
                res = pretty_val
                current_score = unit_score
        if res == None:
            return self.pretty_break_quant(values, quantile, ratio, weights, 10 * n_gen)
        else:
            return res

    def breaker(self, values, n_breaks, weights=[1, 1, 1]):
        res = []
        if values.shape[0] == values[values >= 0].count():
            min_val = 0
        else:
            min_val = PrettyBreaks.boundaries(1, min(values))[0]
        res.append(min_val)
        for i in range(n_breaks + 1, 1, -1):
            vals = values[values >= res[-1]]
            quantile = 1.0 / i
            ratio = 1.0 / (i - 1)
            res.append(self.pretty_break_quant(vals, quantile, ratio, weights))
        return res

    def pretty_count(self, values, pretty_values, use_areas=True):
        s_count = values.groupby(
            pd.cut(values, pretty_values + [np.inf], right=False)
        ).count()
        df_count = pd.DataFrame(
            s_count.values, index=s_count.index.values, columns=["Count"]
        )
        if use_areas and self.area:
            areas = (
                values.groupby(pd.cut(values, pretty_values + [np.inf], right=False))
                .apply(self.area_sum, (False))
                .values
            )
            df_count["Area"] = areas
        return df_count

