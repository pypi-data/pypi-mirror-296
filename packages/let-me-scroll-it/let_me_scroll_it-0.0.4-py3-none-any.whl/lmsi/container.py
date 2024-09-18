"""
The plot container!
"""

import json
import re

from pydantic import BaseModel


class PlotConfig(BaseModel):
    source: str
    title: str
    caption: str
    regex: bool = False

    def match(self, filename: str) -> bool:
        if self.regex:
            return bool(re.match(self.source, filename))
        else:
            return self.source == filename


class SectionConfig(BaseModel):
    name: str
    plots: list[PlotConfig]


class Config(BaseModel):
    sections: list[SectionConfig]

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as handle:
            base = json.load(handle)

        return cls(
            sections=[
                SectionConfig(
                    name=key,
                    plots=[PlotConfig(source=k, **v) for k, v in value.items()],
                )
                for key, value in base.items()
            ]
        )


class Plot(BaseModel):
    filename: str
    title: str = ""
    caption: str = ""
    hash: str = ""

    def model_post_init(self, __context):
        self.hash = str(abs(hash(self.title + self.caption + self.filename)))


class Section(BaseModel):
    name: str
    plots: list[Plot]
    hash: str = ""

    def model_post_init(self, __context):
        self.hash = str(abs(hash(self.name)))


class PlotContainer(BaseModel):
    sections: list[Section]

    @classmethod
    def from_config(cls, config: Config, files: set[str]):
        sections = []
        matched_files = set()
        for section_config in config.sections:
            section_plots = []
            for plot_config in section_config.plots:
                for filename in files:
                    if plot_config.match(filename):
                        section_plots.append(
                            Plot(
                                filename=filename,
                                title=plot_config.title,
                                caption=plot_config.caption,
                            )
                        )
                        matched_files.add(filename)

            if len(section_plots) > 0:
                sections.append(Section(name=section_config.name, plots=section_plots))

        # If there are leftover files, add them to the uncategorised section
        left_over_files = matched_files ^ files

        if len(left_over_files) > 0:
            sections.append(
                Section(
                    name="Uncategorised",
                    plots=[
                        Plot(
                            filename=filename,
                        )
                        for filename in left_over_files
                    ],
                )
            )

        return PlotContainer(sections=sections)
