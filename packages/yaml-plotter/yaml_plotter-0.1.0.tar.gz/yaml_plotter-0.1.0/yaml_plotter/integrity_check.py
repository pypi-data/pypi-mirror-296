import logging

logger = logging.getLogger(__name__)

def integrity_check(config: dict) -> bool:
    # Check yaml config's integrity
    # 1. Check if basic information is correct
    # 2. Check if font information is correct
    # 3. Check if grid information is correct
    # 4. Check if range information is correct
    # 5. Check if legend information is correct
    # 6. Check if plot information is correct
    # 7. Check if label information is correct

    logger.info("Start checking yaml config's integrity.")
    if not integrity_basic_info_check(config):
        return False
    if not integrity_font_check(config["font"]):
        return False
    if not integrity_grid_check(config["grid"]):
        return False
    if not integrity_range_check(config["range"]):
        return False
    if not integrity_legend_check(config["legend"]):
        return False
    if not integrity_plot_check(config["plot"]):
        return False
    if not integrity_label_check(config["label"]):
        return False
    logger.info("Yaml config's integrity check passed.")
    return True


def integrity_basic_info_check(config: dict) -> bool:
    # Check yaml config's basic information
    # 1. Check if "plot_title" exists
    # 2. Check if object "font" exists
    # 3. Check if object "grid" exists
    # 4. Check if object "range" exists
    # 5. Check if object "legend" exists
    # 6. Check if object "plot" exists
    # 7. Check if "double_axis" exists, and it should be a boolean
    # 8. Check if object "label" exists
    logger.info("Start checking yaml config's basic information.")
    requirement_list = ["plot_title", "font", "grid", "legend", "plot", "double_axis", "label"]
    for requirement in requirement_list:
        if requirement not in config:
            logger.error(f"Yaml config's basic information check failed. Missing {requirement}.")
            return False
    if not isinstance(config["double_axis"], bool):
        logger.error("Yaml config's basic information check failed. double_axis should be a boolean.")
        return False
    logger.info("Yaml config's basic information check passed.")
    return True


def integrity_font_check(font_config: dict) -> bool:
    # Check yaml config's font part information
    # The input dictionary should be the "font" part of the yaml config
    # 1. Check if "title_font", "label_font", "legend_font", "tick_font" exists
    # (note that other fonts can also exist)
    # 2. Check if for each font, "family", "size", "style", "weight" exists

    requirement_list = ["title_font", "label_font", "legend_font", "tick_font"]
    for requirement in requirement_list:
        if requirement not in font_config:
            logger.error(f"Yaml config's font part check failed. Missing {requirement}.")
            return False
        font = font_config[requirement]
        if "family" not in font or "size" not in font or "style" not in font or "weight" not in font:
            logger.error(f"Yaml config's font part check failed. Missing family, size, style, or weight in {requirement}.")
            return False
    logger.info("Yaml config's font part check passed.")
    return True


def integrity_grid_check(grid_config: dict) -> bool:
    # Check yaml config's grid part information
    # The input dictionary should be the "grid" part of the yaml config
    # 1. Check if "enabled", "line_width" exists

    requirement_list = ["enabled", "line_width"]
    for requirement in requirement_list:
        if requirement not in grid_config:
            logger.error(f"Yaml config's grid part check failed. Missing {requirement}.")
            return False
    logger.info("Yaml config's grid part check passed.")
    return True


def integrity_range_check(range_config: dict) -> bool:
    # Check yaml config's object part information
    # The input dictionary should be the "object" part of the yaml config
    # 1. Check if "x_min", "x_max", "axis_1_min", "axis_1_max", "axis_2_min", "axis_2_max" exists
    # 2. Check if for each range, "auto" or a number exists

    requirement_list = ["x_min", "x_max", "axis_1_min", "axis_1_max", "axis_2_min", "axis_2_max"]
    for requirement in requirement_list:
        if requirement not in range_config:
            logger.error(f"Yaml config's range part check failed. Missing {requirement}.")
            return False
        if range_config[requirement] != "auto" and not isinstance(range_config[requirement], (int, float)):
            logger.error(f"Yaml config's range part check failed. {requirement} should be 'auto' or a number.")
            return False
    logger.info("Yaml config's range part check passed.")
    return True


def integrity_legend_check(legend_config: dict) -> bool:
    # Check yaml config's legend part information
    # The input dictionary should be the "legend" part of the yaml config
    # 1. Check if "enabled", "location" exists

    requirement_list = ["enabled", "location"]
    for requirement in requirement_list:
        if requirement not in legend_config:
            logger.error(f"Yaml config's legend part check failed. Missing {requirement}.")
            return False
    logger.info("Yaml config's legend part check passed.")
    return True


def integrity_label_check(label_config: dict) -> bool:
    # Check yaml config's label part information
    # The input dictionary should be the "label" part of the yaml config
    # 1. Check if "x_label", "axis_1_label", "axis_2_label" exists

    requirement_list = ["x_label", "axis_1_label", "axis_2_label"]
    for requirement in requirement_list:
        if requirement not in label_config:
            logger.error(f"Yaml config's label part check failed. Missing {requirement}.")
            return False
    logger.info("Yaml config's label part check passed.")
    return True


def integrity_plot_check(plot_config: dict) -> bool:
    # Check yaml config's plot part information
    # The input dictionary should be the "plot" part of the yaml config
    # 1. Check if plot_config is a list
    # 2. Check if each element in plot_config has "type"
    # (allowed type: [line])
    # 3. call each check function for each type

    if not isinstance(plot_config, list):
        logger.error("Yaml config's plot part check failed. plot should be a list.")
        return False
    for plot in plot_config:
        if "type" not in plot:
            logger.error("Yaml config's plot part check failed. Missing type in plot.")
            return False
        if plot["type"] == "line":
            if not integrity_line_plot_check(plot):
                logger.error("Yaml config's plot part check failed. Line plot check failed.")
                return False
        else:
            logger.error(f"Yaml config's plot part check failed. Unknown plot type {plot['type']}.")
            return False
    logger.info("Yaml config's plot part check passed.")
    return True


def integrity_line_plot_check(line_config: dict) -> bool:
    # check if line plot config is correct
    # The input dictionary should be an item of the "plot" part of the yaml config
    # 1. check if "axis", "x", "y", "color", "line_width", "marker", "marker_size", "label" exists
    # 2. check if "axis" is "axis_1" or "axis_2"
    # 3. check if "x" and "y" are lists

    requirement_list = ["axis", "x", "y", "color", "line_width", "marker", "marker_size", "label"]
    for requirement in requirement_list:
        if requirement not in line_config:
            logger.error(f"Yaml config's line plot part check failed. Missing {requirement}.")
            return False
    if line_config["axis"] not in ["axis_1", "axis_2"]:
        logger.error("Yaml config's line plot part check failed. axis should be 'axis_1' or 'axis_2'.")
        return False
    if not isinstance(line_config["x"], list) or not isinstance(line_config["y"], list):
        logger.error("Yaml config's line plot part check failed. x and y should be lists.")
        return False
    logger.info("Yaml config's line plot part check passed.")
    return True
