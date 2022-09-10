#!/usr/bin/env python3

import aws_cdk as cdk

from project.project_stack import ProjectStack


app = cdk.App()
ProjectStack(app, "project")

app.synth()
