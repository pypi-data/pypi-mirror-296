import uuid
from datetime import datetime
from importlib import metadata
from typing import Callable

import click
import gradio as gr
from gradio import Blocks, TabbedInterface

from guigaga.introspect import ArgumentSchema, CommandSchema, OptionSchema, introspect_click_app
from guigaga.logger import Logger


class InterfaceBuilder:
    def __init__(
        self,
        cli: click.Group | click.Command,
        app_name: str | None = None,
        command_name: str = "gui",
        *,
        hide_not_required: bool = True,
    ):
        self.cli = cli
        self.app_name = app_name
        self.command_name = command_name
        self.hide_not_required = hide_not_required
        self.command_schemas = introspect_click_app(cli)
        self.blocks = []
        try:
            self.version = metadata.version(self.click_app_name)
        except Exception:
            self.version = None
        # traverse the command tree and create the interface
        for command_schema in self.command_schemas.values():
            self.traverse_command_tree(command_schema)
        if len(self.blocks) == 1:
            _, self.interface = self.blocks[0]
        else:
            interface_list = [block for _, block in self.blocks]
            tab_names = [name for name, _ in self.blocks]
            self.interface = TabbedInterface(interface_list, tab_names=tab_names)

    def traverse_command_tree(self, schema: CommandSchema):
        if schema.name not in ["root", "gui"]:
            block = self.create_block(schema)
            self.blocks.append(block)
        for subcommand in schema.subcommands.values():
            self.traverse_command_tree(subcommand)

    def create_block(self, command_schema: CommandSchema):
        logger = Logger()

        with Blocks(theme=gr.themes.Soft()) as block:
            self.render_help_and_header(command_schema)
            with gr.Row():
                with gr.Column():
                    if self.hide_not_required:
                        schemas = self.render_schemas(command_schema, render_not_required=False)
                        with gr.Accordion("Advanced Options", open=False):
                            schemas.update(self.render_schemas(command_schema, render_required=False))
                    else:
                        schemas = self.render_schemas(command_schema)
                with gr.Column():
                    btn = gr.Button("Run")
                    logs = gr.Textbox(label="Logs", lines=25, max_lines=25)
                    # tell gradio to display the output
                    # not sure how I'll get it here...
                    # self.outputs(command_schema)
            # inputs = self.sort_schemas(command_schema, schemas)
            inputs = self.sort_schemas(command_schema, schemas)
            btn.click(fn=logger.intercept_stdin_stdout(command_schema.function), inputs=inputs, outputs=logs)
        return command_schema.name, block

    def render_help_and_header(self, command_schema: CommandSchema):
        gr.Markdown(
            f"""
            # {command_schema.name}
            {command_schema.docstring}
            """
            )


    def render_schemas(self, command_schema, *, render_required=True, render_not_required=True):
        inputs = {}
        schemas = command_schema.options + command_schema.arguments
        schemas = [schema for schema in schemas if (render_required and schema.required) or (render_not_required and not schema.required)]
        schemas_name_map = {schema.name if isinstance(schema.name, str) else schema.name[0].lstrip("-"): schema for schema in schemas}
        for name, schema in schemas_name_map.items():
            component = self.get_component(schema)
            inputs[name] = component
        return inputs

    def sort_schemas(self, command_schema, schemas: dict):
        order = command_schema.function.__code__.co_varnames[:command_schema.function.__code__.co_argcount]
        schemas = [schemas[name] for name in order if name in schemas]
        return schemas

    def get_component(self, schema: OptionSchema | ArgumentSchema):
        component_type = schema.type.name
        default = None
        if schema.default.values:
            default = schema.default.values[0][0]
        if isinstance(schema, OptionSchema):
            label = schema.name[0].lstrip("-")
        else:
            label = schema.name
        if schema.required:
            label += "*"

        # Handle different component types
        if component_type == "text":
            return gr.Textbox(default, label=label)

        elif component_type == "integer":
            return gr.Number(default, label=label, precision=0)

        elif component_type == "float":
            return gr.Number(default, label=label)

        elif component_type == "boolean":
            return gr.Checkbox(default == "true", label=label)

        elif component_type == "uuid":
            uuid_val = str(uuid.uuid4()) if default is None else default
            return gr.Textbox(uuid_val, label=label)

        elif component_type == "filename":
            return gr.File(label=label)

        elif component_type == "path":
            return gr.FileExplorer(label=label, file_count="single")

        elif component_type == "Choice":
            choices = option.type.choices
            return gr.Dropdown(choices, value=default, label=label)

        elif component_type == "INT_RANGE":
            min_val = option.type.min if option.type.min is not None else 0
            max_val = option.type.max if option.type.max is not None else 100
            return gr.Slider(minimum=min_val, maximum=max_val, step=1, value=default, label=label)

        elif component_type == "FLOAT_RANGE":
            min_val = option.type.min if option.type.min is not None else 0.0
            max_val = option.type.max if option.type.max is not None else 1.0
            return gr.Slider(minimum=min_val, maximum=max_val, value=default, label=label)

        elif component_type == "DATETIME":
            formats = option.type.formats if option.type.formats else ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
            datetime_val = default if default is not None else datetime.now().strftime(formats[0])
            return gr.Textbox(datetime_val, label=label)

        else:
            return gr.Textbox(default, label=label)


class GUI:
    def __init__(
        self,
        app: click.Group | click.Command,
        app_name: str | None = None,
        command_name: str = "gui",
        click_context: click.Context | None = None,
        *,
        hide_not_required: bool = True,
    ):
        self.app = app
        self.app_name = app_name
        self.command_name = command_name
        self.click_context = click_context
        self.interface = InterfaceBuilder(self.app, self.app_name, self.command_name, hide_not_required=hide_not_required).interface

    def launch(
        self,
    ) -> None:
        self.interface.queue().launch(share=True)


def gui(name: str | None = None, command: str = "gui", help: str = "Open Gradio GUI.", *, hide_not_required = True) -> Callable:
    def decorator(app: click.Group | click.Command):
        @click.pass_context
        def wrapped_gui(ctx, *args, **kwargs):  # noqa: ARG001
            GUI(app, app_name=name, command_name=command, click_context=ctx, hide_not_required=hide_not_required).launch()

        if isinstance(app, click.Group):
            app.command(name=command, help=help)(wrapped_gui)
        else:
            new_group = click.Group()
            new_group.add_command(app)
            new_group.command(name=command, help=help)(wrapped_gui)
            return new_group

        return app

    return decorator
