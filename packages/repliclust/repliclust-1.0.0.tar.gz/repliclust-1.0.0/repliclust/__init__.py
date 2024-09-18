"""
repliclust
==========

`repliclust` is a Python package for generating synthetic data sets 
with clusters. 

The package is based on data set archetypes, high-level geometric 
blueprints that allow you to sample many data sets with the same overall
geometric structure. The following modules and subpackages are available.

**Modules**:
    `repliclust.base`
        Provides the core framework of `repliclust`.
    `repliclust.distributions`
        Implements probability distributions and related functionality.
    `repliclust.viz`
        Implements probability distributions and related functionality.
    `repliclust.distort`
        Implements post-processing functions for turning convex clusters
        into more irregularly shaped, non-convex ones.

**Subpackages**:
    `repliclust.maxmin`
        Implements a data set archetype based on max-min ratios.
    `repliclust.overlap`
        Helps locate cluster centers with the desired overlap.
"""

import numpy as np

from dotenv import load_dotenv
from repliclust import config
from repliclust.base import set_seed, SUPPORTED_DISTRIBUTIONS
from repliclust import base, overlap, maxmin, distributions
from repliclust.base import DataGenerator, get_supported_distributions
from repliclust.maxmin import MaxMinArchetype as Archetype
from repliclust.viz import plot
from repliclust.distortion import distort, wrap_around_sphere

load_dotenv()
import repliclust.natural_language as nl
from openai import OpenAI

config.init_rng()
config._seed = None


def generate(
        archetype_descriptions=["two oblong clusters in 2D with a little overlap"], 
        quiet=True,
        openai_api_key=None
    ):
    """
    Generate synthetic datasets based on verbal descriptions of dataset archetypes.

    This function generates synthetic data by converting natural language descriptions
    of dataset archetypes into data. It leverages OpenAI's language models to interpret
    the descriptions and synthesize corresponding datasets.

    Parameters
    ----------
    archetype_descriptions : str or list of str, optional
        Descriptions of the dataset archetypes to generate. Can be a single description
        string or a list of description strings. Defaults to
        ``["two oblong clusters in 2D with a little overlap"]``.
    quiet : bool, optional
        If ``True``, suppresses verbose output during data synthesis. Defaults to ``True``.
    openai_api_key : str, optional
        API key for OpenAI. If not provided, the function will attempt to use the API key
        from the environment variable ``OPENAI_API_KEY``.

    Returns
    -------
    data : Dataset or list of Datasets
        The synthesized dataset(s) generated from the provided archetype descriptions.
        If a single description is provided, returns a single ``Dataset``; otherwise,
        returns a list of ``Dataset`` objects.

    Raises
    ------
    Exception
        If the OpenAI client cannot be initialized and no API key is provided.

    Examples
    --------
    Generate a single synthetic dataset:

    >>> data = generate("two oblong clusters in 2D with a little overlap")

    Generate multiple synthetic datasets:

    >>> descriptions = [
    ...     "two oblong clusters in 2D with a little overlap",
    ...     "three spherical clusters in 3D with significant overlap"
    ... ]
    >>> data_list = generate(descriptions)
    """
    if (nl.OPENAI_CLIENT is None) and (openai_api_key is None):
        raise Exception(
            "Failed to initialize OpenAI client." +
            " Either put OPENAI_API_KEY=<...> into the .env file" +
            " or pass openai_api_key=<...> as an argument in a function call."
        )
    elif (nl.OPENAI_CLIENT is None) and (openai_api_key is not None):
        nl.load_openai_client(api_key=openai_api_key)

    # record whether to return single data set or list of data sets
    return_simple = False

    # convert simple string input to list
    if isinstance(archetype_descriptions, str):
        return_simple = True
        archetype_descriptions=[archetype_descriptions]

    # turn descriptions into archetypes
    archetypes = [
        Archetype.from_verbal_description(descr, openai_api_key=openai_api_key) 
            for descr in archetype_descriptions
    ]

    # turn archetypes into a data generator
    data_generator = DataGenerator(archetypes, n_datasets=len(archetypes), quiet=True)

    # make the data
    data = [ (*archetype.synthesize(quiet=quiet), archetype) for archetype in archetypes ]

    if return_simple:
        return data[0]
    else:
        return data

# Indicate which components to import with "from repliclust import *"
__all__ = [
    'base',
    'overlap'
    'maxmin',
    'distributions',
    'distortion'
    'viz',
]