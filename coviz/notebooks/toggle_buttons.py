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


class Toggle_Buttons(ipw.Box):
    def __init__(
        self,
        options,
        value,
        description,
        min_button_width,
        min_description_width,
        horizontal=True,
        button_width="100%",
        style="info",
    ):
        self.options = options
        self.value = value
        self.description = description
        self.min_description_width = min_description_width
        self.min_button_width = min_button_width
        self.button_width = button_width
        self.style = style
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
                        self.description,
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
                    width="auto",
                    display="flex",
                    overflow="auto",
                    height="100%",
                ),
            )
        else:
            super(ipw.Box, self).__init__(
                children=[
                    ipw.HTML(
                        "<p style='text-align: center; padding:0; margin:0'>"
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

    def add_observe(self, f_observe, val):
        for b in self.buttons:
            b.observe(f_observe, val)
        return
