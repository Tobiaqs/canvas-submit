# canvas-submit
Python3 program that allows the user to easily upload some files to a Canvas assignment as a submission - from the command line.

## Installation
- Get Python3, Pip and Pipenv installed.
- Clone this repository and place it somewhere handy (i.e. `~/software/canvas-submit`).
- In `~/software/canvas-submit`, run `pipenv install`.
- Open up `~/software/canvas-submit/bin/canvas_submit` and change some variables according to your setup.
- Add `~/software/canvas-submit/bin` to your path (e.g. in `~/.bashrc`).

## Configuration
You need a Canvas API token. Once you have one, it's smart to create a file called `.env` in `~/software/canvas-submit` and set `CANVAS_SUBMIT_API_URL` and `CANVAS_SUBMIT_API_TOKEN` in that file, so you don't have to pass it to `canvas_submit`.

Tip: `CANVAS_SUBMIT_API_URL` is just the base URL of your Canvas installation (e.g. `https://canvas.instructure.com`).

You can also set more parameters in `.env`. Run `canvas_submit -h` for an overview.

## Usage
`canvas_submit --course 5190 --assignment 590921 File1.java File2.java File3.java`
