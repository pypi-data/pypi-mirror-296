"""Parser module to parse gear config.json."""

import logging
import sys
from typing import Tuple

from flywheel_gear_toolkit.context import GearToolkitContext


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[dict, dict]:
    """Parse config file.

    Extract input paths and configuration options.

    Returns:
        gear_inputs (dict): dictionary with the paths to the different inputs
        gear_config (dict): dictionary with gear options
    """
    # Gear inputs
    gear_inputs = {
        "anatomical": gear_context.get_input_path("anatomical"),
        "t1w_anatomical_2": gear_context.get_input_path("t1w_anatomical_2"),
        "t1w_anatomical_3": gear_context.get_input_path("t1w_anatomical_3"),
        "t1w_anatomical_4": gear_context.get_input_path("t1w_anatomical_4"),
        "t1w_anatomical_5": gear_context.get_input_path("t1w_anatomical_5"),
        "t2w_anatomical": gear_context.get_input_path("t2w_anatomical"),
        "freesurfer_license": gear_context.get_input_path("freesurfer_license_file"),
        "expert": gear_context.get_input_path("expert"),
    }

    if not gear_inputs.get("anatomical"):
        logging.error("Anatomical input must be specified.")
        sys.exit(1)

    # Gear configs
    gear_config = {
        "debug": gear_context.config.get("debug"),
        "subject_id": gear_context.config.get("subject_id"),
        "parallel": gear_context.config.get("parallel"),
        "n_cpus": gear_context.config.get("n_cpus"),
        "reconall_options": gear_context.config.get("reconall_options"),
        "gear-gtmseg": gear_context.config.get("gear-gtmseg"),
        "gear-hypothalamic_subunits": gear_context.config.get(
            "gear-hypothalamic_subunits"
        ),
        "gear-hippocampal_subfields": gear_context.config.get(
            "gear-hippocampal_subfields"
        ),
        "gear-brainstem_structures": gear_context.config.get(
            "gear-brainstem_structures"
        ),
        "gear-thalamic_nuclei": gear_context.config.get("gear-thalamic_nuclei"),
        "gear-register_surfaces": gear_context.config.get("gear-register_surfaces"),
        "gear-convert_surfaces": gear_context.config.get("gear-convert_surfaces"),
        "gear-convert_volumes": gear_context.config.get("gear-convert_volumes"),
        "gear-convert_stats": gear_context.config.get("gear-convert_stats"),
        "gear-log-level": gear_context.config.get("gear-log-level"),
        "gear-dry-run": gear_context.config.get("gear-dry-run"),
        "gear-FREESURFER_LICENSE": gear_context.config.get("freesurfer_license_key"),
        "gear-postprocessing-only": gear_context.config.get("gear-postprocessing-only"),
    }

    return gear_inputs, gear_config
