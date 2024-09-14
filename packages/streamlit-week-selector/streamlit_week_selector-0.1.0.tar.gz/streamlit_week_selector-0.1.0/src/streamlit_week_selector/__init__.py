from pathlib import Path
from typing import Optional
import datetime 

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_week_selector,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"streamlit_week_selector", path=str(frontend_dir)
)

def st_keyup(
    label: str,
    value: Optional[str] = "",
    key: Optional[str] = None,
):
    """
    Create a Streamlit text input that returns the value whenever a key is pressed.
    """
    component_value = _component_func(
        label=label,
        value=value,
        key=key,
        default=value
    )

    return component_value

# Create the python function that will be called
def streamlit_week_selector(
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        key=key,
    )

    return component_value


def main():
    st.write("## Example")
    value = st_keyup("This is a label!", '2024-W35')
    st.write(value)
    #value = streamlit_week_selector()

    #st.write(value)


if __name__ == "__main__":
    main()
