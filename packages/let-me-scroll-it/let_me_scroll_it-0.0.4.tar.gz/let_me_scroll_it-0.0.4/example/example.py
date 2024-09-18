"""
An example use of lmsi. Puts three plots into a html webpage.
"""

import matplotlib.pyplot as plt

COLORS_USED = 0


def make_figure(title: str, filename: str):
    global COLORS_USED
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3], color=f"C{COLORS_USED}")
    COLORS_USED += 1
    ax.set_title(title)
    fig.savefig(filename)
    plt.close(fig)


make_figure("Find me with regex", "12341_plot.png")
make_figure("Find me based on a filename", "no_regex_required.png")
make_figure("Find me without a caption", "no_caption.png")

# Run the script!
print("You need to run:")
print("lmsi --files *.png --output index.html --config example.json")
