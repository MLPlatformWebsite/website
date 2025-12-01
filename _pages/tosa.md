---
layout: flow
title: Developer Resources
permalink: /tosa/
js-package: resources
css_bundle: resources
description: >
  Here you can find an aggregation of TOSA related presentations, videos and other resources.
jumbotron:
  title: Tensor Operator Set Architecture (TOSA)
  image: /assets/images/content/ml-banner.jpg

flow:
  - row: container_row
    sections:
      - format: image
        alt: The TOSA logo
        path: /assets/images/content/TOSA_LOGO_COLOUR_RGB.png
  - row: container_row
    sections:
      - format: block
        item_width: "6"
        style: text-center
        block_section_content:
          blocks:
            - title: Contributing
              description: |-
                  Click here to learn how to contribute to TOSA
              buttons:
                - title: Contributions
                  url: /tosa/contributing.html
            - title: Roadmap
              description: Click below to learn about the TOSA roadmap
              buttons:
                - title: Roadmap
                  url: /tosa/roadmap.html
  - row: container_row
    sections:
      - format: text
        text_content:
          text: |
            # Introduction
            Tensor Operator Set Architecture (TOSA) provides a set of whole-tensor operations commonly employed by Deep Neural Networks.
            The intent is to enable a variety of implementations running on a diverse range of processors, with the results at the TOSA level consistent across those implementations.
            Applications or frameworks which target TOSA can therefore be deployed on a wide range of different processors, including SIMD CPUs, GPUs and custom hardware such as NPUs/TPUs, with defined accuracy and compatibility constraints.
            Most operators from the common ML frameworks (TensorFlow, PyTorch, etc.) should be expressible in TOSA.
            It is expected that there will be tools to lower from ML frameworks into TOSA.

            # Goals
            A minimal and stable set of tensor-level operators to which machine learning framework operators can be reduced.
            Full support for both quantized integer and floating-point content.
            Precise functional description of the behavior of every operator, including the treatment of their numerical behavior in the case of precision, saturation, scaling, etc. as required by quantized datatypes.
            Agnostic to any single high-level framework, compiler backend stack or particular target.
            The detailed functional and numerical description enables precise code construction for a diverse range of targets – SIMD CPUs, GPUs and custom hardware such as NPUs/TPUs.

            # Specification
      - format: buttons
        style: text-center
        buttons_content:
          - title: TOSA Specification
            url: /tosa/tosa_spec.html
      - format: text
        text_content:
          text: |-
            The TOSA Specification is written as AsciiDoc mark-up and developed in its raw mark-up form, managed through a git repository here: [https://github.com/arm/tosa-specification](https://github.com/arm/tosa-specification). The specification is developed and versioned much like software is. While the mark-up is legible and can be read fairly easily in its raw form, it is recommended to build or “render” the mark-up into a PDF document, or similar. To do this, please follow the instructions in the README.md in the root of the specification repository.

            # Principles for New Operators
            TOSA defines a set of primitive operators to which higher level operators can be lowered in a consistent way.
            To remain effective and efficient to implement the set of operators must be constrained to a reasonably small set of primitive operations out of which others can be constructed.
            For a list of the principles for TOSA operators see the [TOSA specification](tosa_spec.html#_operator_selection_principles)

  - row: container_row
    sections:
      - format: text
        text_content:
          text: |-
            # TOSA videos

            Below is a video introduction to TOSA done as part of Arm's AI Tech Talk series.

      - format: youtube
        url: https://youtu.be/I-mljwralfU
        title: "Arm Tech Talk: Introducing a common operator set for Machine Learning accelerators – TOSA"
---
