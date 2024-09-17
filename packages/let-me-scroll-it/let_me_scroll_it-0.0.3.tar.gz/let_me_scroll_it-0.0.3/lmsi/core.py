"""
Core functions for the LMSI package, taking in
raw paths and saving out the HTML file.
"""

from pathlib import Path

from lmsi.container import Config, PlotContainer
from lmsi.webpage.html import WebpageCreator


def core(
    potential_plots: list[Path],
    config_location: Path,
    output: Path,
):
    if config_location is not None:
        config = Config.from_file(config_location)
    else:
        config = Config(sections=[])

    plot_container = PlotContainer.from_config(
        config, {x.name for x in potential_plots}
    )

    webpage_creator = WebpageCreator()
    webpage_creator.add_metadata("LMSI Webpage")
    webpage_creator.add_plots(plot_container)
    webpage_creator.render_webpage()
    webpage_creator.save_html(output)

    return
