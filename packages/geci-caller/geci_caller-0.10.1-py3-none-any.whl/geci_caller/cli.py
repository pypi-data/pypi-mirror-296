from geci_caller import construct_entrypoint_url
import requests
import typer

cli = typer.Typer()


@cli.command()
def write_population_status(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstraps"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    entrypoint_name = "/write_population_status"
    get_eradication_progress(
        entrypoint_name,
        input_path=input_path,
        bootstrapping_number=bootstrapping_number,
        output_path=output_path,
    )


@cli.command()
def write_csv_probability(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstrap by window"),
    output_path: str = typer.Option(help="Path of csv file to write"),
    window_length: int = typer.Option(help="Number of months by window"),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/write_effort_and_captures_with_probability",
        input_path=input_path,
        bootstrapping_number=bootstrapping_number,
        output_path=output_path,
        window_length=window_length,
    )
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def write_probability_progress_figure(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/write_probability_figure",
        input_path=input_path,
        output_path=output_path,
    )
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def plot_comparative_catch_curves(
    socorro_path: str = typer.Option(help="Path of Socorro data"),
    guadalupe_path: str = typer.Option(help="Path of Guadalupe data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/plot_comparative_catch_curves",
        socorro_path=socorro_path,
        guadalupe_path=guadalupe_path,
        output_path=output_path,
    )
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def plot_custom_cpue_vs_cum_captures(
    input_path: str = typer.Option(help="Path of input data"),
    config_path: str = typer.Option(help="Path of config file"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    entrypoint_name = "/plot_custom_cpue_vs_cum_captures"
    get_eradication_progress(
        entrypoint_name, input_path=input_path, config_path=config_path, output_path=output_path
    )


def get_eradication_progress(entrypoint_name, **kwargs):
    url = construct_entrypoint_url("eradication_progress", 10000, entrypoint_name, **kwargs)
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def plot_cpue_vs_cum_captures(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/plot_cpue_vs_cum_captures",
        input_path=input_path,
        output_path=output_path,
    )
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def plot_cumulative_series_cpue_by_flight(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/plot_cumulative_series_cpue_by_flight",
        input_path=input_path,
        output_path=output_path,
    )
    response = requests.get(url)
    print(response.status_code)
