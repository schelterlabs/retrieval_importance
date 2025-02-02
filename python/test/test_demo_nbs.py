import os

from importnb import Notebook

from retrieval_importance.utils import get_project_root


TOY_EXAMPLE_NB = os.path.join(str(get_project_root()), "toy_example.ipynb")
TOY_EXAMPLE_GROUPS_NB = os.path.join(str(get_project_root()), "toy_example_with_groups.ipynb")
WIKIFACT_NB = os.path.join(str(get_project_root()), "wikifact.ipynb")
WIKIFACT_GROUPS_NB = os.path.join(str(get_project_root()), "wikifact_with_groups.ipynb")
TIFU_TOY_EXAMPLE_NB = os.path.join(str(get_project_root()), "tifu_toy_example.ipynb")

def test_demo_nbs():
    """
    Tests whether the demo notebook works
    """
    # matplotlib.use("template")  # Can be used if we have matplotlib plots in the demo notebooks at some point
    for notebook in [TOY_EXAMPLE_NB, TOY_EXAMPLE_GROUPS_NB, WIKIFACT_GROUPS_NB, WIKIFACT_GROUPS_NB,
                     TIFU_TOY_EXAMPLE_NB]:
        Notebook().load(notebook)
