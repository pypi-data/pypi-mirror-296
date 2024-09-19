import rbt.cli.terminal as terminal
import sys
from rbt.cli.cloud import cloud_down, cloud_up, register_cloud
from rbt.cli.dev import dev_expunge, dev_run, register_dev
from rbt.cli.export_import import (
    do_export,
    do_import,
    register_export_and_import,
)
from rbt.cli.init.init import init_run, register_init
from rbt.cli.protoc import protoc, register_protoc
from rbt.cli.rc import ArgumentParser
from rbt.cli.secret import register_secret, secret_delete, secret_write
from rbt.cli.serve import register_serve, serve
from rbt.cli.subprocesses import Subprocesses
from rbt.cli.task import register_task, task_cancel, task_list
from typing import Optional


def create_parser(
    *,
    rc_file: Optional[str] = None,
    argv: Optional[list[str]] = None,
) -> ArgumentParser:

    parser = ArgumentParser(
        program='rsm',
        filename='.rsmrc',
        subcommands=[
            'cloud down',
            'cloud up',
            'cloud secret delete',
            'cloud secret write',
            'dev expunge',
            'dev run',
            'export',
            'import',
            'init',
            'protoc',
            'serve',
            'task list',
            'task cancel',
        ],
        rc_file=rc_file,
        argv=argv,
    )

    register_dev(parser)
    register_export_and_import(parser)
    register_protoc(parser)
    register_secret(parser)
    register_cloud(parser)
    register_init(parser)
    register_serve(parser)
    register_task(parser)

    return parser


async def rsm() -> int:
    # Sets up the terminal for logging.
    verbose, argv = ArgumentParser.strip_any_arg(sys.argv, '-v', '--verbose')
    terminal.init(verbose=verbose)

    # Install signal handlers to help ensure that Subprocesses get cleaned up.
    Subprocesses.install_terminal_app_signal_handlers()

    parser = create_parser(argv=argv)

    args, argv_after_dash_dash = parser.parse_args()

    if args.subcommand == 'dev run':
        return await dev_run(
            args,
            parser=parser,
            parser_factory=lambda argv: create_parser(argv=argv),
        )
    elif args.subcommand == 'dev expunge':
        await dev_expunge(args)
        return 0
    elif args.subcommand == 'export':
        return await do_export(args)
    elif args.subcommand == 'import':
        return await do_import(args)
    elif args.subcommand == 'protoc':
        return await protoc(args, argv_after_dash_dash, parser=parser)
    elif args.subcommand == 'secret write':
        await secret_write(args)
        return 0
    elif args.subcommand == 'secret delete':
        await secret_delete(args)
        return 0
    elif args.subcommand == 'cloud up':
        await cloud_up(args)
        return 0
    elif args.subcommand == 'cloud down':
        await cloud_down(args)
        return 0
    elif args.subcommand == 'init':
        await init_run(args)
        return 0
    elif args.subcommand == 'serve':
        return await serve(
            args,
            parser=parser,
            parser_factory=lambda argv: create_parser(argv=argv),
        )
    elif args.subcommand == 'task list':
        await task_list(args)
        return 0
    elif args.subcommand == 'task cancel':
        await task_cancel(args)
        return 0

    raise NotImplementedError(
        f"Subcommand '{args.subcommand}' is not implemented"
    )
