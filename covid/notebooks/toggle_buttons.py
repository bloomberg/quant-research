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

import ipywidgets as ipw

button_style = """
<style>
    .{0:s} {{
        overflow: visible;
        position: relative;
    }}
    .{0:s}:hover{{
        text-decoration: none;
    }}
    .{0:s}::before {{
        height: 25px;
        background: #4caf50;
        border-radius: 6px;
        padding: 2px 6px;
        white-space: nowrap;
        color: white;
        z-index: 999;
        font-weight: bold;
        content:{1:s};
        {2:s}
    }}
    .{0:s}::before {{
        position: absolute;
        display: none;
    }}
    .{0:s}:hover::before {{
        display: block;
    }}
</style>
"""


class Toggle_Buttons(ipw.Box):
    def __init__(
        self,
        options,
        value,
        description,
        min_button_width,
        min_description_width,
        key,
        horizontal=True,
        button_width="100%",
        style="info",
        tooltips=None,
        description_tooltip="",
        tooltip_position="right",
    ):
        self.all_styles = ""
        self.key = key
        self.options = options
        self.value = value
        self.description = description
        self.min_description_width = min_description_width
        self.min_button_width = min_button_width
        self.button_width = button_width
        self.style = style
        self.tooltip_position = tooltip_position
        if tooltips:
            self.buttons = [self.create_button(d, t) for t, d in zip(tooltips, options)]
        else:
            self.buttons = [
                ipw.ToggleButton(
                    description=d,
                    value=False,
                    button_style="",
                    layout=ipw.Layout(
                        min_width=self.min_button_width,
                        width=self.button_width,
                        min_height="30px",
                    ),
                )
                for d in options
            ]
        self.index_val = options.index(value)
        self.buttons[self.index_val].value = True
        self.buttons[self.index_val].button_style = self.style
        if horizontal:
            super(ipw.Box, self).__init__(
                children=[
                    ipw.HTML(
                        "<p style='padding:0; margin:0'; title="
                        + description_tooltip
                        + ">"
                        + self.description
                        + "</p>",
                        layout=ipw.Layout(
                            min_width=self.min_description_width,
                            width="auto",
                            height="auto",
                            margin="0 0 0 0",
                        ),
                    )
                ]
                + self.buttons,
                layout=ipw.Layout(
                    align_items="stretch",
                    width="100%",
                    display="flex",
                    overflow="visible",
                    height="100%",
                ),
            )
        else:
            super(ipw.Box, self).__init__(
                children=[
                    ipw.HTML(
                        "<p style='text-align: center; padding:0; margin:0'; title="
                        + description_tooltip
                        + ">"
                        + self.description
                        + "</p>",
                        layout=ipw.Layout(
                            min_width=self.min_description_width,
                            width="auto",
                            height="30px",
                            align_items="center",
                            margin="0 0 0 0",
                        ),
                    )
                ]
                + self.buttons,
                layout=ipw.Layout(
                    align_items="stretch",
                    height="auto",
                    display="flex",
                    flex_flow="column",
                    overflow="auto",
                ),
            )
        for b in self.buttons:
            b.observe(self.update_col, "value")
        return

    def update_col(self, *args):
        if args[0]["owner"].description != self.value:
            for b in self.buttons:
                if b.description == args[0]["owner"].description:
                    b.value = True
                    b.button_style = self.style
                else:
                    b.value = False
                    b.button_style = ""
        self.value = args[0]["owner"].description
        return

    def set_value(self, val):
        if val != self.value:
            for b in self.buttons:
                if b.description == val:
                    b.value = True
                    b.button_style = self.style
                else:
                    b.value = False
                    b.button_style = ""
        self.value = val
        return

    def add_observe(self, f_observe, val):
        for b in self.buttons:
            b.observe(f_observe, val)
        return

    def del_observe(self, f_observe, val):
        for b in self.buttons:
            b.unobserve(f_observe, val)
        return

    def create_button(self, description, tooltip):
        button_ = ipw.ToggleButton(
            description=description,
            value=False,
            button_style="",
            layout=ipw.Layout(
                min_width=self.min_button_width,
                width=self.button_width,
                min_height="30px",
            ),
        )
        if self.tooltip_position == "right":
            tt_pos = """
            top: 0px;
            left: 102%"""
        elif self.tooltip_position == "left":
            tt_pos = """
            top: 0px;
            right: 102%"""
        elif self.tooltip_position == "top":
            if description == "Daily % change":
                tt_pos = """
                left: -120%;
                bottom: 105%"""
            elif len(tooltip) > 20:
                tt_pos = """
                left: -60%;
                bottom: 105%"""
            else:
                tt_pos = """
                left: 0%;
                bottom: 105%"""
        elif self.tooltip_position == "bottom":
            if description == "Daily % change":
                tt_pos = """
                left: -120%;
                top: 105%"""
            elif len(tooltip) > 20:
                tt_pos = """
                left: -60%;
                top: 105%"""
            else:
                tt_pos = """
                left: 0%;
                top: 105%"""
        style = button_style.format(
            description.replace("%", "pct").replace(" ", "") + "_" + self.key,
            tooltip,
            tt_pos,
        )
        self.all_styles += style
        button_.add_class(
            description.replace("%", "pct").replace(" ", "") + "_" + self.key
        )
        return button_
