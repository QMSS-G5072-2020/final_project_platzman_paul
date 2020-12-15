# Celebrity Bucks Game Player Advantage 

![](https://github.com/paulplatzman/celebrity_bucks_game_player_advantage/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/paulplatzman/celebrity_bucks_game_player_advantage/branch/main/graph/badge.svg)](https://codecov.io/gh/paulplatzman/celebrity_bucks_game_player_advantage) ![Release](https://github.com/paulplatzman/celebrity_bucks_game_player_advantage/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/celebrity_bucks_game_player_advantage/badge/?version=latest)](https://celebrity_bucks_game_player_advantage.readthedocs.io/en/latest/?badge=latest)

Python package providing Celebrity Bucks game players with additional celebrity attribute data to inform buy/sell/hold decisions!

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ celebrity_bucks_game_player_advantage
```

## Features

- This package contains a data set of all celebrities available in the Celebrity Bucks online game. The data set presents information returned by the Celebrity Bucks API and augments it with additional celebrity features found in two other online sources. This package also contains a `create_celebrity_data_set.py` script that allows users to easily create new data sets or collect information about individual celebrities, enabling them to capture the most up to date celebrity information.  

## Dependencies

- bs4
- json
- os
- pandas
- requests
- sys
- datetime

## Usage

- Please see `./Celebrity_Bucks_GPA_Package_Tutorial.ipynb` for details about how to use this package.

## Documentation

The official documentation is hosted on Read the Docs: https://celebrity_bucks_game_player_advantage.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/paulplatzman/celebrity_bucks_game_player_advantage/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
