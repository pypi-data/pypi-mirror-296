from typing import Callable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from oak_cli.evaluation.addons.flops.utils.stages.draw import draw_stages
from oak_cli.evaluation.addons.flops.utils.stages.main import STAGE_ID_KEY
from oak_cli.evaluation.graph_utils import adjust_xticks, get_evaluation_run_duration_label

# _DEFAULT_FONT_SIZE = 10
# DEFAULT_FONT_SIZE = 14
DEFAULT_FONT_SIZE = 20


def draw_graph(
    data: pd.DataFrame,
    title: Optional[str] = "",
    plot_functions: Optional[List[Callable]] = None,
    x_lim: Optional[Union[Tuple[float, float], float]] = None,
    y_lim: Optional[Union[Tuple[float, float], float]] = None,
    x_label: str = "",
    y_label: str = "",
    size: Tuple[int, int] = (10, 5),
    show_stages: bool = False,
    stages_color_intensity: float = 0.3,
    stages_color_height: float = 100,
    use_percentage_limits: bool = False,
    font_size_multiplier: float = 1,
    y_axis_font_size_multiplier: Optional[float] = None,
    x_axis_font_size_multiplier: Optional[float] = None,
    sort_by_stage_id: bool = False,
    use_median_stages: bool = False,
    show_legend_in_right_bottom_corner: bool = False,
    show_only_stage_legend: bool = False,
) -> None:
    if sort_by_stage_id:
        data = data.copy().sort_values(by=STAGE_ID_KEY)

    fig, ax = plt.subplots(figsize=size)
    if title:
        ax.set_title(title, fontsize=DEFAULT_FONT_SIZE * font_size_multiplier)

    if not plot_functions:
        sns.lineplot(data=data)
    else:
        for plot_function in plot_functions:
            plot_function()

    x_font_size = DEFAULT_FONT_SIZE * (x_axis_font_size_multiplier or font_size_multiplier)
    plt.xlabel(
        x_label or get_evaluation_run_duration_label(),
        fontsize=x_font_size,
    )
    plt.tick_params(axis="x", labelsize=x_font_size)
    adjust_xticks(ax)

    y_font_size = DEFAULT_FONT_SIZE * (y_axis_font_size_multiplier or font_size_multiplier)
    plt.ylabel(
        y_label,
        fontsize=y_font_size,
    )
    plt.tick_params(axis="y", labelsize=y_font_size)

    if use_percentage_limits:
        if y_lim is None:
            y_lim = (0, 100)
        if x_lim is None:
            x_lim = (0, max(data.index))

    if x_lim is not None:
        if isinstance(x_lim, tuple):
            plt.xlim([x_lim[0], x_lim[1]])
        else:
            plt.xlim(x_lim)
    if y_lim is not None:
        if isinstance(y_lim, tuple):
            plt.ylim([y_lim[0], y_lim[1]])
        else:
            plt.ylim(y_lim)

    if show_stages or show_only_stage_legend:
        draw_stages(
            data=data,
            color_intensity=stages_color_intensity,
            stages_color_height=stages_color_height,
            use_median_stages=use_median_stages,
            show_only_stage_legend=show_only_stage_legend,
        )

    if show_legend_in_right_bottom_corner:
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(
            handles,
            labels,
            bbox_to_anchor=(1, 0),
            loc="lower right",
            fontsize=DEFAULT_FONT_SIZE * font_size_multiplier,
        )

    #    plt.legend()
    # DELME
    # handles, labels = ax.get_legend_handles_labels()
    # plt.legend(
    #     # handles,
    #     # labels,
    #     # bbox_to_anchor=(1, 0),
    #     # loc="lower right",
    #     title="Evaluation Run",
    #     title_fontsize=DEFAULT_FONT_SIZE * font_size_multiplier,
    #     fontsize=DEFAULT_FONT_SIZE * font_size_multiplier,
    # )

    # Adjust the layout
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1, wspace=0.3, hspace=0.3)

    # Increase pad for extra margin
    # plt.tight_layout(pad=2.0)
    # sns.set(font_scale=2)

    import random

    random_number = random.randint(1, 100000)
    plt.savefig(f"{random_number}.pdf", dpi=300, bbox_inches="tight")

    plt.show()
