---
title: Contributing to the TOSA specification
description: How to contribute to the TOSA Specification
slug: tosa/contributing_spec/
layout: ../../layouts/Flow.astro
keywords:
  - TOSA
  - Machine Learning
hero:
  title: Contributing to TOSA specification
  description: How to contribute to the TOSA Specification
flow:
  - row: container_row
    sections:
      - component: text
        text_content:
          text: |-
            ## Specification Contributions
            The TOSA Specification is released under a different kind of licence to the software, one which enables vendors to create completely independent implementations of the TOSA specification which are not derivatives of anything on mlplatform.org.
            This license is posted at the start of the [TOSA specification](tosa_spec.html).
            To enable vendors to implement the TOSA Specification in this way, contributions need to be provided under a different license, the TOSA Specification Contributor Agreement.

            To view the TOSA Specification Contributor License Agreement, click below.
      - component: buttons
        style: text-center
        buttons_content:
          - title: TOSA Specification CLA
            url: /tosa/tosa_cla.html
            style: bg-blue-800 text-white rounded-sm hover:bg-blue-950
      - component: text
        text_content:
          text: |-
            ### How to Contribute
            Practically, contributions to the TOSA Specification are made by modifying the AsciiDoc markup of the specification.
            Those patches are then reviewed using Gerrit on [https://review.mlplatform.org/q/project:tosa%252Fspecification](https://review.mlplatform.org/q/project:tosa%252Fspecification).
            However, before uploading patches to a gerrit review, users must read and agree to the TOSA Specification Contributors License Agreement. This can be achieved by doing the following:

            - Login to Gerrit (http://review.mlplatform.org)
            - Navigate to User Settings
            - Open the "Agreements" section
            - Click the "New Contributor Agreement" link
            - Select the "TOSA" radio button
            - Open the link to the TOSA Specification and read
            - *If* you agree to these terms, type "I agree" in the text box and click "SUBMIT"
            - Note: You may get an error saying "Agreement already submitted.". This is harmless, please ignore it.
            - Start uploading patches to the specification!
            - Note: More significant contributions should be discussed on the MLPlatform.org's Discourse, under the "TOSA" Category. Decisions on accepting more significant changes will be made largely based on the principals laid out above. I.e. Adding new operators to TOSA which can be trivially decomposed into a sequence of existing TOSA operators are unlikely to be accepted! :-)
---
