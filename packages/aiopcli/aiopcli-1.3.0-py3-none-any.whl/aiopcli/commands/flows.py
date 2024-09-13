import logging

import click

from aiopcli import utils

def parse_flow(ctx, param, s: str) -> tuple[str, str]:
    try:
        domain, endpoint = s.split("/")
    except ValueError:
        raise click.BadParameter(f"invalid flow: {s}: must be of the form '<domain>/<endpoint>'")
    return domain, endpoint


@click.group("flows")
def cli():
    pass

@cli.command
@click.argument('flow', callback=parse_flow)
@click.option('-F', '--form', 'fields', multiple=True)
@click.option('-d', '--data')
@click.pass_obj
def run(ctx, flow, fields, data):
    domain, endpoint = flow
    path = f"/api/v1/domains/{domain}/endpoints/{endpoint}"
    with utils.prepare_fields(fields, data) as (json, files, data):
        logging.debug(f"POST {path} {files=} {data=}")
        response = ctx.client.post(path, json=json, files=files, data=data)
    utils.handle_response(response)
