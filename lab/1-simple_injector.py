# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Simple Injector Examples
# This example provides injecting way with non-nested some classes and some variables.
# The class following a protocol

# ## load packages

# + jupyter={"outputs_hidden": false}
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from injector import Binder, Injector, Module, inject, provider

# -
# ## Setting up Classes


# + jupyter={"outputs_hidden": false}
class Transportation(Protocol):
    """Protocol to be followed transportation
    """
    def transport(self) -> None:
        ...

    def __repr__(self) -> str:
        ...


class Ship:
    """A kind of transporation
    """
    def __init__(self, name: str = 'titanic') -> None:
        self.name = name

    def transport(self) -> None:
        print(f'{self.name} goes on the sea')

    def __repr__(self) -> str:
        return self.name


@inject
@dataclass
class Route:
    """Represents a route by ship
    """
    departure_time: datetime
    ship: Transportation

    def __repr__(self) -> str:
        return f"""
            {self.departure_time=}
            {self.ship=}
        """

# -
# ## Injection


# ### With Fixed Configuration
# This module provides a route with current departure


# + jupyter={"outputs_hidden": false}
class CurrentRouteModule(Module):
    """Creates `Routes` from current time
    """
    def configure(self, binder: Binder) -> None:
        binder.bind(Transportation, to=Ship)
        binder.bind(datetime, to=datetime.now())


injector1 = Injector(CurrentRouteModule)
route1 = injector1.get(Route)
print(route1)
# -

# ### With Variable Configuration
# This module provides a route with departure time set by outer scope.


# +
@dataclass
class DepartureConfig:
    departure_time: datetime


class RouteModule(Module):
    """Common Route Module
    """

    def configure(self, binder: Binder) -> None:
        binder.bind(Transportation, to=Ship)

    @provider
    def provide_departure(self, config: DepartureConfig) -> datetime:
        return config.departure_time


def configure_departure_for_2020_new_year(binder: Binder) -> None:
    binder.bind(
        DepartureConfig,
        to=DepartureConfig(
            departure_time=datetime(
                year=2020, month=1, day=1,
            )
        ),
    )


def departure_config_for_2021_new_year(binder: Binder) -> None:
    binder.bind(
        DepartureConfig,
        to=DepartureConfig(
            departure_time=datetime(
                year=2020, month=1, day=1,
            )
        ),
    )


# -

# create route by `configure_departure_for_2020_new_year`
injector2 = Injector([configure_departure_for_2020_new_year, RouteModule()])
route2 = injector2.get(Route)
print(route2)

# create route by `configure_departure_for_2021_new_year`
injector3 = Injector([departure_config_for_2021_new_year, RouteModule()])
route3 = injector3.get(Route)
print(route3)

# Now, we can get two routes from common `RouteModule`
