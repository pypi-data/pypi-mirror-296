from datetime import datetime
import click
import json
import sys
import io

from postman_cli_transformer.junit_transformer import junit_transform
from postman_cli_transformer.processor import Processor


@click.command()
@click.argument("output", type=click.File("w"), required=True)
@click.option(
    "-junit",
    "--junit-out-file",
    required=False,
    type=click.File("w"),
    help="File location to output junit xml file from transformed CLI results.",
)
@click.option(
    "-bup",
    "--bubble-up-exit-code",
    default=True,
    required=False,
    type=click.BOOL,
    help="""Defaults to True. Since this tool is used to transform output results from the Postman CLI,
     it will exit with an error if the underlying Postman CLI output contains an error. 
    This will facilitate the failure of the task in a CI/CD pipeline. If you do not want 
     this behavior and wish the exit code to reflect the exit state of this app, set 
     this flag to False.""",
)
@click.version_option()
def cli(output, junit_out_file, bubble_up_exit_code):
    """This script will take as input the STDOUT from
    a Postman CLI collection run and transform the
    output text to a file containing the output data
    organized in a JSON format. It will also preserve
    the CLI standard out and send to STDOUT at the end
    of its execution.

    \b
    Output to file foo.json:
        postman-cli-transformer foo.json

    \b
    Output json to file foo.json and output junit xml to file bar.xml :
        postman-cli-transformer foo.json --junit-out-file bar.xml

    """

    stdin_data = sys.stdin.read()

    parsed_stdin, errored = parse(stdin_data)

    if junit_out_file:
        current_time_of_test_run = datetime.now().isoformat()

        results = junit_transform(json.loads(parsed_stdin), current_time_of_test_run)
        junit_out_file.write(results)

    output.write(parsed_stdin)
    output.flush()

    click.echo(stdin_data)

    if bubble_up_exit_code:
        if errored:
            raise click.exceptions.Exit(1)


def parse(data):
    raw_lines = []
    data_as_file = io.StringIO(data)
    for line in data_as_file:
        raw_lines.append(line)

    processor = Processor(raw_lines)
    results = processor.parsed
    errored = processor.errored

    json_str = json.dumps(results)

    return json_str, errored
