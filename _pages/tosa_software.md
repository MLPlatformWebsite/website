---
title: Contributing to TOSA software
permalink: /tosa/software.html
keywords:
    - TOSA
    - Machine Learning
jumbotron:
  title: TOSA Software
  description: TOSA related software projects
  image: /assets/images/content/ml-banner.jpg
flow:
  - row: container_row
    sections:
      - format: text
        text_content:
          text: |-
            # Overview of TOSA Software

            The Tensor Operator Set Architecture (TOSA) defines a standard set of operations for machine-learning workloads. The tools below help developers create, test, and work with TOSA-based models.

            ### TOSA Tools

            TOSA Tools is the main software package for working with the TOSA specification. It brings together three key components:

            - TOSA Serialization Library
            - TOSA Reference Model
            - TOSA MLIR Translator

            Git repository: [https://gitlab.arm.com/tosa/tosa-tools](https://gitlab.arm.com/tosa/tosa-tools)

            #### TOSA Serialization Library

            The TOSA Serialization Library provides the basic building blocks for reading and writing TOSA graphs. It includes:

            - A FlatBuffers schema for the TOSA graph format
            - A C++ API for reading and writing graphs
            - A Python API for reading graphs

            This library is the foundation for other TOSA tools.

            #### TOSA Reference Model

            The Reference Model is the “golden” implementation of TOSA. Other TOSA implementations can be tested or validated against it.

            It reads a TOSA flatbuffer file (produced by the Serialization Library) along with input tensors in NumPy format. It then:

            1. Validates the graph
            2. Executes it
            3. Writes output tensors in NumPy format

            The project also includes tools for generating unit tests. These tests consist of TOSA operations serialized as flatbuffers, with NumPy-formatted inputs and expected outputs.

            #### TOSA MLIR Translator

            The MLIR Translator converts TOSA dialect MLIR into a serialized TOSA flatbuffer. It uses a set of MLIR passes to generate output compatible with the Serialization Library and Reference Model.

            ### Deprecated Tools and Repositories

            #### Deprecation of Repositories on git.mlplatform.org and review.mlplatform.org

            In November 2025, the Gerrit instance at mlplatform.org was retired.
            The older repositories remain available as read-only mirrors (listed below), but all ongoing development happens in the TOSA Tools repository: [https://gitlab.arm.com/tosa/tosa-tools](https://gitlab.arm.com/tosa/tosa-tools).

            ##### Mirrors of Deprecated Repositories

            | Repository | Deprecated URL | Mirror |
            | ----------- | -------------- | ------ |
            | Reference Model | https://git.mlplatform.org/tosa/reference_model.git/ | [https://gitlab.arm.com/tosa/tosa-reference-model](https://gitlab.arm.com/tosa/tosa-reference-model) |
            | Serialization Library | https://git.mlplatform.org/tosa/serialization_lib.git/ | [https://gitlab.arm.com/tosa/tosa-serialization](https://gitlab.arm.com/tosa/tosa-serialization) |
            | TOSA Checker | https://git.mlplatform.org/tosa/tosa_checker.git/ | [https://gitlab.arm.com/tosa/tosa-checker](https://gitlab.arm.com/tosa/tosa-checker) |
            | TOSA MLIR Translator | https://git.mlplatform.org/tosa/tosa_mlir_translator.git/ | [https://gitlab.arm.com/tosa/tosa-mlir-translator](https://gitlab.arm.com/tosa/tosa-mlir-translator) |


            #### TOSA Checker (Deprecated)

            The TOSA Checker helps verify whether a model can be represented entirely with TOSA operators. It primarily supports TensorFlow Lite models.

            - Git repository: [https://gitlab.arm.com/tosa/tosa-checker](https://gitlab.arm.com/tosa/tosa-checker)
            - PyPI package: [https://pypi.org/project/tosa-checker](https://pypi.org/project/tosa-checker)
---
