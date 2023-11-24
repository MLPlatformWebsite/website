---
title: Arm ML Inference Advisor
description: The Arm ML Inference Advisor (Arm MLIA) helps AI developers design and optimize neural network models for efficient inference on Arm targets.
permalink: /mlia/
keywords:
  - Arm MLIA
layout: flow
jumbotron:
  title: Overview
  image: /assets/images/content/ml-banner.jpg
flow:
  - row: container_row
    sections:
      - format: text
        text_content:
          text: >-
            ## Overview


            The Arm ML Inference Advisor (Arm MLIA) helps AI developers design and optimize neural network models for efficient inference on Arm targets. MLIA enables insights into how the ML model will perform on Arm early in the model development cycle. By passing a model file and specifying an Arm hardware target, users get an overview of possible areas of improvement and an actionable advice on how to address each of them. The advice can cover *operator compatibility*, *performance analysis* and *model optimization* (e.g. pruning and clustering). With the Arm ML Inference Advisor, we aim to make the Arm ML IP accessible to developers at all levels of abstraction, with differing knowledge on hardware optimization and machine learning. 

            The figure below gives an overview of the data flow.

      - format: image
        alt: MLIA data flow overview
        size: "10"
        path: /assets/images/content/mlia-overview.png
      - format: text
        text_content:
          text: >-
            For further technical information, refer to the documentation on the [pypi.org homepage for Arm MLIA](https://pypi.org/project/mlia/). For a quick introduction to the tool, check out this [blog post](https://community.arm.com/arm-community-blogs/b/ai-and-ml-blog/posts/arm-machine-learning-inference-advisor).
---
