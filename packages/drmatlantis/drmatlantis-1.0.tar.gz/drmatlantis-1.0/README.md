# drmatlantis

This Python class allows to run Dr. MATLANTIS on MATLANTIS server.

## Prerequisites

Before using this integration, ensure you have the following installed:

- Jupyter Notebook or JupyterLab
- Python 3.6+
- Required Python packages: `anywidget`, `traitlets`, `ipylab`

## Installation

```shell
pip install drmatlantis
   ```
## Usage

1. Import the class in your Jupyter notebook:

   ```python
   from drmatlantis import DrMatlantisServer
   ```

2. Initialize the server and run it

   ```python
   server = DrMatlantisServer()
   server.run()
   ```

## License

MIT License

Copyright (c) 2024 Hristo Todorov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.