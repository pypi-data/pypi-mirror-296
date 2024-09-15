# Strategizer

`Strategizer` is a Python-based framework for executing various financial trading strategies. This package provides a simple interface to apply multiple strategies, evaluate their performance, and integrate them with machine learning models for more advanced use cases.


## Features
- Pre-built trading strategies: Random, Buy Close Sell Open, SMA Crossover, and more.
- Flexible architecture to add your own custom strategies.
- Data handling using pandas and numpy.
- Integration with popular technical analysis libraries like `ta` and machine learning libraries like `sklearn`.


## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nathanschmidt89/strategizer.git
   cd strategizer


## Usage/Examples

### Example: Running a Strategy

```python
import pandas as pd
import numpy as np
from strategizer.main import StrategyExecutor, random_strategy

# Create sample data
data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Close': np.random.randn(100).cumsum()
})
data.set_index('Date', inplace=True)

# Initialize the executor
executor = StrategyExecutor(data)

# Run a strategy
result = executor.execute_strategy(random_strategy)
print(result)
```


## Authors

Nathan Schmidt is a  programmer with years of experience in software development. Specializing in innovative programming solutions, Nathan has a commitment to open-source development and community collaboration. Known for his passion for clean code and efficiency, Nathan continues to contribute to the field of software engineering with a focus on impactful, real-world applications.


## Support

For support, email nathan.schmidt.ns89@gmail.com or raise a Github issue.

