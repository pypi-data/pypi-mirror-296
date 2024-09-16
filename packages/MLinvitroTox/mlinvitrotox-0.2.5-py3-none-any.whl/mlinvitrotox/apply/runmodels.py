from pathlib import Path

import click

import mlinvitrotox.utils.predict as predict
from mlinvitrotox.utils.model import Model


@click.command("run")
@click.option(
    "--model", "-m", required=True, help="name of the model or path to model file"
)
@click.option(
    "--input_file",
    "-i",
    help="input file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--output_folder",
    "-o",
    required=True,
    type=click.Path(path_type=Path),
    help="path to directory where the processed output should be stored. It will be created if it does not exist.",
)
def run_models(input_file, model, output_folder):
    """
    Run models on molecular fingerprints

    """
    model_instance = Model()
    model_path = Path(model)
    model_instance.load(model_path)

    # load predicted fingerprints and get chemical ids
    df_predfps = predict.load_application_data(input_file)
    df_predfps.set_index("chem_id", inplace=True)

    # Collect predictions for each aeid

    # from pyinstrument import Profiler
    # profiler = Profiler()
    # profiler.start()

    df_predictions = model_instance.predict(df_predfps)

    # profiler.stop()
    # print(profiler.output_text(unicode=True,color=True))
    # with open('tmp/prof.html', 'w') as f:
    #     f.write(profiler.output_html())

    # set file name for predictions output file
    output_predictions_file = output_folder / f"{model_path.stem}_predictions.csv"

    # Save predictions
    df_predictions = predict.sort_by_aeid_and_chem_id(df_predictions)
    df_predictions.round(5).to_csv(output_predictions_file, index=False)
    print(f"Predictions stored to {output_predictions_file}")


if __name__ == "__main__":
    run_models()
