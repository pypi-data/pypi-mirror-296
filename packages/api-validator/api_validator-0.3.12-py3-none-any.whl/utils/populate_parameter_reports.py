"""
Populate the example parameter reports.
"""
from os.path import join, pardir, dirname, exists, isfile
from os import listdir, environ
from api_validator.oasdiff_v2.param_report import generate_parameter_report
from dotenv import load_dotenv
from api_validator.diff_utils.jobs import JobsContainer, read_jobs_from_yaml


load_dotenv()


def list_files(directory: str) -> list:
    """
    List all files in a directory
    """
    return [f for f in listdir(directory) if isfile(join(directory, f))]


def populate(overwrite: bool = True, app_name: str = None, include_spec_in_report: bool = False):
    examples_dir = join(dirname(__file__), pardir, "examples")
    # The app names will be the names of the files in the base directory, minus the extension
    app_names = [f.split(".")[0] for f in list_files(join(examples_dir, "base"))]
    if app_name:
        if app_name not in app_names:
            raise ValueError(f"App name {app_name} not found in the examples directory")
        app_names = [app_name]

    base_dir = join(examples_dir, "base")
    revision_dir = join(examples_dir, "revision")
    report_dir = join(examples_dir, "reports", "parameter-reports")

    # Assumption 0: The files all have the same base name as an app in the config file.
    config_file = join(dirname(__file__), pardir, "config.yml")
    jobs_container = read_jobs_from_yaml(config_file)


    # Assumption 1: the base and revision directories have files that follow the same naming convention.
    #   We copied them over from the analysis directory after running the `api-validator compare` command for every
    #   app under every language in the config.

    # Assumption 2: The files all end in .yml
    for app in app_names:
        base_file = join(base_dir, f"{app}.yml")
        revision_file = join(revision_dir, f"{app}.yml")
        output_file = join(report_dir, f"{app}.md")
        swagger_url = jobs_container.get_swagger_url(app)
        if not swagger_url:
            swagger_url = ""
        generate_parameter_report(base_file, revision_file, output_file, old_swagger_url=swagger_url, overwrite=overwrite)


if __name__ == '__main__':
    import argparse
    from api_validator.bin.logger import init_logger
    environ["LOGURU_LEVEL"] = "DEBUG"
    parser = argparse.ArgumentParser(description="Populate all the oasdiff JSON files in the examples directory")
    parser.add_argument("--keep-existing", action="store_true", help="Do not overwrite existing files")
    parser.add_argument("--app-name", help="Only populate the specified app")
    parser.add_argument("--include-spec-in-report", action="store_true", help="Include the full spec in the report")
    args = parser.parse_args()
    init_logger()
    do_overwrite = not args.keep_existing
    this_app_name = args.app_name
    populate(do_overwrite, this_app_name, args.include_spec_in_report)
