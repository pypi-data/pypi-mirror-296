import matplotlib.pyplot as plt
import yaml
import logging
from . import integrity_check
from PIL import Image
import io


def plot_2d_chart(yaml_file_path: str) -> Image:
    with open(yaml_file_path, 'r') as f:
        config = yaml.safe_load(f)
    if not integrity_check.integrity_check(config):
        raise ValueError("Yaml config's integrity check failed.")

    # clear all plot information
    plt.clf()

    # get font information
    title_font = config['font']['title_font']
    tick_font = config['font']['tick_font']
    label_font = config['font']['label_font']
    legend_font = config['font']['legend_font']



    # create two axis
    fig, ax1 = plt.subplots()
    enable_ax2 = config['double_axis']
    if enable_ax2:
        ax2 = ax1.twinx()


    # create grid
    if config['grid']['enabled']:
        line_width = config['grid']['line_width']
        ax1.grid(
            axis="both",
            linewidth=line_width
        )

    # set axis range
    if config['range']['x_min'] != "auto" and config['range']['x_max'] != "auto":
        plt.xlim(config['range']['x_min'], config['range']['x_max'])
    if config['range']['axis_1_min'] != "auto" and config['range']['axis_1_max'] != "auto":
        ax1.set_ylim(config['range']['axis_1_min'], config['range']['axis_1_max'])
    if config['range']['axis_2_min'] != "auto" and config['range']['axis_2_max'] != "auto":
        if enable_ax2:
            ax2.set_ylim(config['range']['axis_2_min'], config['range']['axis_2_max'])
    plt.xticks(
        fontsize=tick_font['size'],
        fontfamily=tick_font['family'],
        fontstyle=tick_font['style'],
        fontweight=tick_font['weight']
    )
    ax1.yaxis.set_tick_params(
        size=tick_font['size'],
        labelfontfamily=tick_font['family'],
    )
    if enable_ax2:
        ax2.yaxis.set_tick_params(
            size=tick_font['size'],
            labelfontfamily=tick_font['family'],
        )



    # set axis labels
    ax1.set_xlabel(
        config['label']['x_label'],
        family=label_font['family'],
        style=label_font['style'],
        weight=label_font['weight'],
        size=label_font['size']
    )
    ax1.set_ylabel(
        config['label']['axis_1_label'],
        family=label_font['family'],
        style=label_font['style'],
        weight=label_font['weight'],
        size=label_font['size']
    )
    if enable_ax2:
        ax2.set_ylabel(
            config['label']['axis_2_label'],
            family=label_font['family'],
            style=label_font['style'],
            weight=label_font['weight'],
            size=label_font['size']
        )

    # start to plot
    line_list = []
    for plot_obj in config['plot']:
        if plot_obj['type'] == 'line':
            axis_obj = ax1 if plot_obj['axis'] == "axis_1" else ax2
            x = plot_obj['x']
            y = plot_obj['y']
            color = plot_obj['color']
            line_width = plot_obj['line_width']
            marker = plot_obj['marker']
            marker_size = plot_obj['marker_size']
            label = plot_obj['label']

            line = axis_obj.plot(
                x, y,
                color=color,
                linewidth=line_width,
                marker=marker,
                markersize=marker_size,
                label=label
            )
            line_list.append(line)
        else:
            raise ValueError("Unsupported plot type: " + plot_obj['type'])

    # merge and set legend
    if config['legend']['enabled']:
        lines = []
        for line in line_list:
            lines += line
        labels = [line.get_label() for line in lines]
        ax1.legend(
            lines, labels,
            loc=config['legend']['location']
        )

    # set plot title
    plt.title(
        config['plot_title'],
        family=title_font['family'],
        style=title_font['style'],
        weight=title_font['weight'],
        size=title_font['size']
    )

    # tight layout
    plt.tight_layout()

    # save plot to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=400)
    buf.seek(0)

    # read image from memory buffer
    image = Image.open(buf)
    return image


def plot_2d_chart_to_file(yaml_file_path: str, output_file_path: str):
    image = plot_2d_chart(yaml_file_path)
    image.save(output_file_path)
    logging.info(f"2D chart is saved to {output_file_path}.")
    return output_file_path


def plot_2d_chart_and_show(yaml_file_path: str):
    image = plot_2d_chart(yaml_file_path)
    image.show()
    logging.info("2D chart is shown.")
    return image













