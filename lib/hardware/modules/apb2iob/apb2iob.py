def setup(py_params_dict):
    attributes_dict = {
        "original_name": "apb2iob",
        "name": "apb2iob",
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "apb",
                "descr": "APB interface",
                "signals": [],
            },
            {
                "name": "iob",
                "descr": "CPU native interface",
                "signals": [],
            },
        ],
        "blocks": [
            {
                "core_name": "iob_reg_e",
                "instance_name": "iob_reg_e_inst",
            },
        ],
    }

    return attributes_dict
