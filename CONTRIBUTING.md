# Contributing
Also known as how can you help?

## Testing
The vast majority of BTHome properties have been incorporated into the module. But in my projects, I only use a handful of them. Which means many are untested under real-world conditions. If you're using BTHome-MicroPython in a project and something's not quite right, please fill out a bug report in the [GitLab issues](https://github.com/DavesCodeMusings/BTHome-MicroPython/issues).

## Bug Reports
Try to include the following:
* What's not working?
* What is it doing?
* What should it be doing?
* Any ideas to fix it.

For example:

Gas detection is not working. It's returning a 16-bit integer. It should be returning a boolean. I looked in bthome.py and I think the property is mapped incorrectly.
