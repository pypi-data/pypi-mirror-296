# Copyright (c) 2024 Zhendong Peng (pzd17@tsinghua.org.cn)
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

import os
from functools import partial
from IPython.display import Audio, display, HTML
from pathlib import Path

import soundfile as sf
from jinja2 import Environment, FileSystemLoader


class WaveSurfer:
    def __init__(self):
        self.idx = 0
        dirname = os.path.dirname(__file__)
        wavesurfer_script = open(f"{dirname}/js/wavesurfer.min.js", encoding="utf-8")
        hover_script = open(f"{dirname}/js/hover.min.js", encoding="utf-8")
        minimap_script = open(f"{dirname}/js/minimap.min.js", encoding="utf-8")
        regions_script = open(f"{dirname}/js/regions.min.js", encoding="utf-8")
        spectrogram_script = open(f"{dirname}/js/spectrogram.min.js", encoding="utf-8")
        timeline_script = open(f"{dirname}/js/timeline.min.js", encoding="utf-8")
        zoom_script = open(f"{dirname}/js/zoom.min.js", encoding="utf-8")
        plugins_script = open(f"{dirname}/js/plugins.js", encoding="utf-8")

        loader = FileSystemLoader(f"{dirname}/templates")
        template = Environment(loader=loader).get_template("wavesurfer.txt")
        self.template_render = partial(
            template.render,
            wavesurfer_script=wavesurfer_script.read(),
            hover_script=hover_script.read(),
            minimap_script=minimap_script.read(),
            regions_script=regions_script.read(),
            spectrogram_script=spectrogram_script.read(),
            timeline_script=timeline_script.read(),
            zoom_script=zoom_script.read(),
            plugins_script=plugins_script.read(),
        )

    def display_audio(
        self,
        audio,
        sr=None,
        width=1200,
        enable_hover=True,
        enable_timeline=True,
        enable_minimap=False,
        enable_spectrogram=False,
        enable_zoom=False,
        enable_regions=False,
    ):
        """
        Render audio data and return the rendered result.

        :param audio: Audio data to be rendered.
        :param sr: Sample rate of the audio data.
        :param width: Width of the rendered output.
        :param enable_hover: Enable hover plugin.
        :param enable_timeline: Enable timeline plugin.
        :param enable_minimap: Enable minimap plugin.
        :param enable_spectrogram: Enable spectrogram plugin.
        :param enable_zoom: Enable zoom plugin.
        :param enable_regions: Enable regions plugin.
        :return: Rendered output html code.
        """
        if isinstance(audio, (str, Path)) and sr is None:
            sr = sf.info(audio).samplerate

        self.idx += 1
        html_code = self.template_render(
            idx=self.idx,
            audio=Audio(audio, rate=sr),
            sr=sr,
            width=width,
            enable_hover=enable_hover,
            enable_timeline=enable_timeline,
            enable_minimap=enable_minimap,
            enable_spectrogram=enable_spectrogram,
            enable_zoom=enable_zoom,
            enable_regions=enable_regions,
        )
        display(HTML(html_code))


wavesurfer = WaveSurfer()
