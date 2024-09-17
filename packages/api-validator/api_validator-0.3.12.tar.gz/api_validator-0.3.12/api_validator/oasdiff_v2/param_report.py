from jinja2 import Environment, FileSystemLoader
from os.path import dirname, exists, relpath
from os import remove
import yaml
from typing import Union
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.compare import get_diff_data
from loguru import logger


class ParameterReport:
    def __init__(self, report_name: str = "Parameter Report", include_spec_in_report: bool = False):
        self.diff_data: DiffData = DiffData()
        self.report_name = report_name
        self.markdown: str = ""
        self.include_spec_in_report = include_spec_in_report
        self.old_spec_file: Union[str, None] = None
        self.new_spec_file: Union[str, None] = None
        self.new_spec_content: Union[str, None] = None
        self.old_spec_content: Union[str, None] = None
        self.old_spec_component_count: Union[int, None] = None
        self.new_spec_component_count: Union[int, None] = None
        self.original_spec_url: Union[str, None] = None

    def __repr__(self):
        return f"ParameterReport(diff_data={self.diff_data})"

    def load_oasdiff_data(self, data: dict) -> None:
        """
        Load the OASDiff data into a list of Parameter objects.

        :param data: The OASDiff data.
        :return:
        """
        self.diff_data.load(data)

    def load_specs(self, old_spec_file: str, new_spec_file: str, old_spec_url: str) -> None:
        """
        Load the OpenAPI specification content from the previous files.
        """
        self.old_spec_file = old_spec_file
        self.new_spec_file = new_spec_file
        try:
            with open(new_spec_file, 'r') as file:
                self.new_spec_content = file.read()
        except FileNotFoundError:
            logger.error(f"New spec file not found: {new_spec_file}")
            return
        # Now calculate how many components are in the new spec
        new_spec_data = yaml.safe_load(self.new_spec_content)
        self.new_spec_component_count = len(new_spec_data.get("components", {}).get("schemas", {}))
        # And calculate how many components are in the old spec
        with open(old_spec_file, 'r') as file:
            self.old_spec_content = file.read()
        old_spec_data = yaml.safe_load(self.old_spec_content)
        self.old_spec_component_count = len(old_spec_data.get("components", {}).get("schemas", {}))
        self.original_spec_url = old_spec_url

    def render_markdown_report(self) -> str:
        # Prepare data
        type_changed_params = self.diff_data.parameters_with_changed_variable_types()
        required_changed_params = self.diff_data.parameters_with_changed_requirements()
        schema_changed_params = self.diff_data.parameters_with_changed_schema()
        default_changed_params = self.diff_data.parameters_with_changed_default_values()
        removed_params = self.diff_data.removed_parameters()
        removed_request_body_params = self.diff_data.removed_request_data()

        # Set up Jinja2 environment and load template
        template_path = dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("param_report.md.j2")

        # Render the template with the report data
        rendered_markdown = template.render(
            parameter_report_name=self.report_name,
            type_changed_params=type_changed_params,
            required_changed_params=required_changed_params,
            schema_changed_params=schema_changed_params,
            default_changed_params=default_changed_params,
            removed_params=removed_params,
            removed_request_body_params=removed_request_body_params,
            new_spec=self.new_spec_content if self.include_spec_in_report else None,
            original_spec_url=self.original_spec_url,
            original_component_count=self.old_spec_component_count,
            new_component_count=self.new_spec_component_count
        )
        self.markdown = rendered_markdown
        return rendered_markdown

    def write_markdown_report(self, output_path: str, overwrite: bool = True) -> None:
        """
        Renders a markdown report using a Jinja2 template and writes it to a file.

        :param output_path: Path where the rendered markdown file will be saved.
        :param overwrite: Whether to overwrite the existing file.
        :return:
        """
        rendered_markdown = self.render_markdown_report()
        if exists(output_path):
            if overwrite:
                logger.info(f"Removing existing report at {relpath(output_path)}")
                remove(output_path)
            else:
                logger.info(f"Report already exists at {relpath(output_path)}. Not overwriting.")
                return
        # Write the rendered markdown to a file
        with open(output_path, 'w') as file:
            file.write(rendered_markdown)
        logger.info(f"Markdown report generated: {output_path}")


def generate_parameter_report(
        old_file: str, new_file: str, report_file: str,
        old_swagger_url: str, overwrite: bool = True, include_spec_in_report: bool = False
) -> None:
    data = get_diff_data(old_file, new_file)
    parameter_report = ParameterReport(include_spec_in_report=include_spec_in_report)
    parameter_report.load_oasdiff_data(data)
    parameter_report.load_specs(old_spec_file=old_file, new_spec_file=new_file, old_spec_url=old_swagger_url)
    parameter_report.write_markdown_report(report_file, overwrite)


if __name__ == '__main__':
    import argparse
    from os.path import exists
    from os import remove
    from api_validator.bin.logger import init_logger
    init_logger()

    parser = argparse.ArgumentParser(description="Run OASDiff to compare two OpenAPI specifications")
    parser.add_argument("old_file", help="The base OpenAPI specification file")
    parser.add_argument("new_file", help="The new OpenAPI specification file")
    parser.add_argument("report_file", help="The report file to generate")
    args = parser.parse_args()
    diff_data = get_diff_data(args.old_file, args.new_file)
    generate_parameter_report(args.old_file, args.new_file, args.report_file, old_swagger_url="")
