#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   main.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   CLI main entrance
"""

import sys

from datature.nexus.cli import batch as batch_functions
from datature.nexus.cli import functions, messages
from datature.nexus.cli.commands import Commands
from datature.nexus.error import ErrorWithCode, ForbiddenError


def main() -> None:
    """Executes the main function of cli."""
    try:
        commands = Commands()
        args = commands.parse_args()

        if args.command == "projects":
            handle_project_command(commands)
        elif args.command == "assets":
            handle_asset_command(commands)
        elif args.command == "annotations":
            handle_annotation_command(commands)
        elif args.command == "artifacts":
            handle_artifact_command(commands)
        elif args.command == "batch":
            handle_batch_command(commands)
        else:
            commands.print_help()
    except KeyboardInterrupt:
        sys.exit(0)
    except (ForbiddenError, ErrorWithCode, IOError) as error:
        handle_error(error)


def handle_project_command(commands):
    """Executes the project level function of cli."""
    args = commands.parse_args()
    if args.action == "auth":
        functions.authenticate()
    elif args.action == "select":
        functions.select_project()
    elif args.action == "list":
        functions.list_projects()
    else:
        commands.print_help(args.command)


def handle_asset_command(commands):
    """Executes the asset level function of cli."""
    args = commands.parse_args()
    if args.action == "upload":
        functions.upload_assets(args.path, args.groups)
    elif args.action == "groups":
        functions.assets_group(args.group)
    else:
        commands.print_help(args.command)


def handle_annotation_command(commands):
    """Executes the annotation level function of cli."""
    args = commands.parse_args()
    if args.action == "upload":
        functions.upload_annotations(args.path)
    elif args.action == "download":
        functions.download_annotations(args.path, args.format)
    else:
        commands.print_help(args.command)


def handle_artifact_command(commands):
    """Executes the artifact level function of cli."""
    args = commands.parse_args()
    if args.action == "download":
        functions.download_artifact(args.artifact_id, args.format)
    else:
        commands.print_help(args.command)


def handle_batch_command(commands):
    """Executes the batch level function of cli."""
    args = commands.parse_args()
    if args.entity == "jobs":
        handle_batch_jobs_command(commands, args)
    elif args.entity == "datasets":
        handle_batch_datasets_command(commands, args)
    elif args.entity == "webhooks":
        handle_batch_webhooks_command(commands, args)
    elif args.entity == "webhooksecrets":
        if args.action == "create":
            batch_functions.webhook.create_webhook_secret()
        else:
            commands.print_help(args.action)
    else:
        commands.print_help(args.command)


def handle_batch_jobs_command(commands, args):
    """Executes the batch job level function of cli."""
    if args.action == "create":
        batch_functions.job.create_job()
    elif args.action == "get":
        batch_functions.job.get_job(args.id)
    elif args.action == "list":
        batch_functions.job.list_jobs()
    elif args.action == "wait-until-done":
        batch_functions.job.wait_until_done(args.id)
    elif args.action == "cancel":
        batch_functions.job.cancel_job(args.id)
    elif args.action == "delete":
        batch_functions.job.delete_job(args.id)
    elif args.action == "logs":
        batch_functions.job.get_job_logs(
            args.id,
            args.max_entries,
            args.since,
            args.until,
            args.level,
            args.output,
        )
    else:
        commands.print_help(args.action)


def handle_batch_datasets_command(commands, args):
    """Executes the batch dataset level function of cli."""
    if args.action == "create":
        batch_functions.dataset.create_dataset()
    elif args.action == "get":
        batch_functions.dataset.get_dataset(args.id)
    elif args.action == "list":
        batch_functions.dataset.list_datasets()
    elif args.action == "delete":
        batch_functions.dataset.delete_dataset(args.id)
    else:
        commands.print_help(args.action)


def handle_batch_webhooks_command(commands, args):
    """Executes the batch webhook level function of cli."""
    if args.action == "create":
        batch_functions.webhook.create_webhook()
    elif args.action == "get":
        batch_functions.webhook.get_webhook(args.id)
    elif args.action == "list":
        batch_functions.webhook.list_webhooks()
    elif args.action == "update":
        batch_functions.webhook.update_webhook(args.id)
    elif args.action == "update-secret":
        batch_functions.webhook.update_webhook_secret(args.id)
    elif args.action == "delete":
        batch_functions.webhook.delete_webhook(args.id)
    elif args.action == "test":
        batch_functions.webhook.test_webhook(args.id)
    else:
        commands.print_help(args.action)


def handle_error(error):
    """Cli handle error functions."""
    if isinstance(error, ForbiddenError):
        print(messages.AUTHENTICATION_FAILED_MESSAGE)
    else:
        print(messages.UNKNOWN_ERROR_SUPPORT_MESSAGE)
    sys.exit(1)
