# TouchDesigner Public Component Building

This template repository is intended for creatives and developers who are looking for a simple and repeatable way to share components they build in [TouchDesigner](https://derivative.ca/) with others. At [SudoMagic](https://www.sudomagic.com/) we use a [CI/CD](https://docs.github.com/en/actions/get-started/continuous-integration) pipeline built around [self hosted github runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) for this process, but it's not always easy to maintain this kind of infrastructure. This repo is both an example for how you can get started, and contains a number of convenience scripts and tools to make the process of creating sharable, versionable, and repeatable between your repos.

This process is built on the assumption that you're already using github to host some of your work. If you haven't started yet, that's okay - you can use this repo as a launching point for creating your own sharable TOX files that are easy to track and version as you make updates.

## Dependencies

* [Task](https://taskfile.dev/)
* [Github CLI](https://cli.github.com/)
* [Python 3.14](https://www.python.org/downloads/release/python-3143/)

## Getting Started

### Create a Github Account

This template assumes that you'll be using Github as your platform for both managing your version history and for creating [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases). If you don't already have a github account it's important to start by creating an account that you can use.

### Install Dependencies

The automation in this repo uses all of the dependencies outlined above. Before creating a release it's important that you first install all of the tools listed above.

### Tags

This template uses [tags](https://docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop) as a mechanic versioning your work. Broadly, the idea is that you are responsible for creating tags for major and minor changes e.g. `v0.1` and `v1.1`. The automation in this project will automatically increment a patch tag that's based on the number of commits you've made to your project between releases. Before your first commit you'll want to make sure you both create and push an initial tag to your repo - a good place to start is something like `v0.1`. Currently the automation here uses the syntax `v{major}.{minor}.{patch}`. You only ever need to create major and minor tags manually, patch tags will be created automatically by the automation.

### Using the Terminal

The processes for creating a release uses the terminal - if you haven't spent much time using the terminal before you might start by going though an [interactive tutorial here](https://www.terminaltutor.com/). You'll only need to use a few commands to get around, but it's worth taking some time to get familiar with the terminal a little before you dive into creating your first release.

#### Tasks

```bash
task release-package
```

```bash
task release-bundle
```

### Typical Workflow
