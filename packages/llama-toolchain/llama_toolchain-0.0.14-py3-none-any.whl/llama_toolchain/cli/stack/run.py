# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import argparse

from pathlib import Path

import pkg_resources
import yaml

from llama_toolchain.cli.subcommand import Subcommand
from llama_toolchain.core.datatypes import *  # noqa: F403
from llama_toolchain.common.config_dirs import BUILDS_BASE_DIR


class StackRun(Subcommand):
    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self.parser = subparsers.add_parser(
            "run",
            prog="llama stack run",
            description="""start the server for a Llama Stack Distribution. You should have already built (or downloaded) and configured the distribution.""",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self.parser.set_defaults(func=self._run_stack_run_cmd)

    def _add_arguments(self):
        from llama_toolchain.core.package import ImageType

        self.parser.add_argument(
            "config",
            type=str,
            help="Path to config file to use for the run",
        )
        self.parser.add_argument(
            "--port",
            type=int,
            help="Port to run the server on. Defaults to 5000",
            default=5000,
        )
        self.parser.add_argument(
            "--disable-ipv6",
            action="store_true",
            help="Disable IPv6 support",
            default=False,
        )

    def _run_stack_run_cmd(self, args: argparse.Namespace) -> None:
        from llama_toolchain.common.exec import run_with_pty
        from llama_toolchain.core.package import ImageType

        if not args.config:
            self.parser.error("Must specify a config file to run")
            return

        path = args.config
        config_file = Path(path)

        if not config_file.exists():
            self.parser.error(
                f"File {str(config_file)} does not exist. Did you run `llama stack build`?"
            )
            return

        with open(config_file, "r") as f:
            config = PackageConfig(**yaml.safe_load(f))

        if not config.distribution_type:
            raise ValueError("Build config appears to be corrupt.")

        if config.docker_image:
            script = pkg_resources.resource_filename(
                "llama_toolchain",
                "core/start_container.sh",
            )
            run_args = [script, config.docker_image]
        else:
            script = pkg_resources.resource_filename(
                "llama_toolchain",
                "core/start_conda_env.sh",
            )
            run_args = [
                script,
                config.conda_env,
            ]

        run_args.extend([str(config_file), str(args.port)])
        if args.disable_ipv6:
            run_args.append("--disable-ipv6")

        run_with_pty(run_args)
