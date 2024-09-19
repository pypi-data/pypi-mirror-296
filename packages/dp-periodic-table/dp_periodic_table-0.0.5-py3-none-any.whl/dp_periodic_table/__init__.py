import os
from typing import List, Dict, Optional, Union
import streamlit.components.v1 as components


_DEVELOP_MODE = os.getenv("STREAMLIT_DP_PERIODIC_DEVELOP_MODE") == 'true'
if _DEVELOP_MODE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("sequence_editor"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "dp_periodic_table",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("dp_periodic_table", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def dp_periodic_table(selected_elements: Optional[List] = None, multiselect: bool = False, key: str = "dp_periodic_table"):
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    selected_elements = selected_elements or []
    if multiselect is False and selected_elements and len(selected_elements) > 1:
        raise ValueError("multiselect must be True when selected_elements has more than one element")

    component_value = _component_func(
        selectedElements=selected_elements,
        multiselect=multiselect,
        key=key
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value or []
