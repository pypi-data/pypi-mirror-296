"""
 Copyright 2024 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import yaml
from typing import Dict, Any, Set, Tuple
from jinja2 import Template, UndefinedError


class YAMLParser:
    @staticmethod
    def load_and_render_template(file_path: str, params: Dict[str, str]) -> str:
        """
        Loads and renders the .yml.j2 template using the provided parameters.

        Args:
            file_path (str): The path to the .yml.j2 file.
            params (Dict[str, str]): Parameters to use for rendering the template.

        Returns:
            str: The rendered YAML content as a string.
        """
        with open(file_path, 'r') as file:
            template_str = file.read()
        template = Template(template_str)
        try:
            return template.render(**params)
        except UndefinedError as e:
            raise ValueError(f"Missing parameters for rendering: {e}")

    @staticmethod
    def get_variables(file_path: str) -> Dict[str, str]:
        """
        Extracts the 'variables' section from the .yml.j2 template.

        Args:
            file_path (str): The path to the .yml.j2 file.
        """
        with open(file_path, 'r') as file:
            raw_yaml = file.read()
        match = re.search(r"variables:\s*(\n(?:[ \t]+.*\n?)*)", raw_yaml)
        if match:
            variables_section = match.group(1)
        else:
            print("Variables section not found.")
        return YAMLParser.parse_rendered_yaml(variables_section)

    @staticmethod
    def get_sample_values(file_path: str) -> Dict[str, str]:
        """
        Extracts sample values from the 'variables' section.

        Args:
            file_path (str): The path to the .yml.j2 file.

        Returns:
            Dict[str, str]: A dictionary of variable names and their sample values.
        """        
        variables_section = YAMLParser.get_variables(file_path)
        return {var: details['sample'] for var, details in variables_section.items() if 'sample' in details}

    @staticmethod
    def get_default_values(file_path: str) -> Dict[str, str]:
        """
        Extracts default variables from the 'variables' section.

        Args:
            variables_section (Dict[str, Dict[str, str]]): The 'variables' section of the YAML.

        Returns:
            Dict[str, str]: A dictionary of variable names and their default values.
        """
        variables_section = YAMLParser.get_variables(file_path)
        return {var: details.get('default') for var, details in variables_section.items() if 'default' in details}

    @staticmethod
    def extract_required_variables(template_str: str) -> Set[str]:
        """
        Extracts all the variables used in the Jinja2 template.
        """
        env = Environment()
        parsed_content = env.parse(template_str)
        return meta.find_undeclared_variables(parsed_content)

    @staticmethod
    def parse_rendered_yaml(rendered_yaml: str) -> Dict[str, Any]:
        """
        Parses the rendered YAML string.

        Args:
            rendered_yaml (str): The rendered YAML content.

        Returns:
            Dict[str, Any]: Parsed YAML data.
        """
        return yaml.safe_load(rendered_yaml)

    @staticmethod
    def load_config(file_path: str, params: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Loads, renders, and parses the YAML configuration from a .yml.j2 file.

        Args:
            file_path (str): The path to the .yml.j2 file.
            params (Dict[str, str]): Parameters to use for rendering the template.

        Returns:
            Dict[str, Any]: Parsed YAML data after rendering.
            Dict[str, str]: The parameters used for rendering the template.
        """
        # Get the default values for variables
        default_values = YAMLParser.get_default_values(file_path)

        # Merge provided params with default values (params override defaults)
        merged_params = {**default_values, **params}

        # Render the template with merged params
        rendered_yaml = YAMLParser.load_and_render_template(file_path, merged_params)
        parsed_yaml = YAMLParser.parse_rendered_yaml(rendered_yaml)
        return (parsed_yaml, merged_params)

    @staticmethod
    def load_config_with_sample_values(file_path: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Loads, renders, and parses the YAML configuration from a .yml.j2 file
        using the sample values provided in the variables section.

        Args:
            file_path (str): The path to the .yml.j2 file.

        Returns:
            Dict[str, Any]: Parsed YAML data after rendering with sample values.
            Dict[str, str]: The parameters used for rendering the template.
        """
        sample_config = YAMLParser.get_sample_values(file_path)
        parsed_yaml, merged_params = YAMLParser.load_config(file_path, sample_config)
        return (parsed_yaml, merged_params)

