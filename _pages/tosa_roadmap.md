---
title: TOSA Roadmap
permalink: /tosa/roadmap.html
keywords:
    - TOSA
    - Machine Learning
jumbotron:
  title: TOSA Roadmap
  description: The TOSA roadmap
  image: /assets/images/content/ml-banner.jpg
flow:
  - row: container_row
    sections:
      - format: text
        text_content:
          text: |
            # TOSA Release summary and Roadmap
            This page describes the release history of TOSA as well as the current roadmap.
      - format: text
        text_content:
          text: |-
            {:.table}
            | Version | Date | Status | Summary of key changes |
            | ------- | ---- | ------ | ---------------------- |
            | 0.20    | 2020-10-29 | Released | Base and Main inference specification initial draft |
            | 0.22    | 2021-03-23 | [Released](https://discuss.mlplatform.org/t/tosa-specification-0-22-0-released/63) | Base inference specification improvements |
            | 0.23    | 2021-11-03 | [Released](https://discuss.mlplatform.org/t/tosa-specification-v0-23-0-released/98) | Base inference reference model released |
            | 0.30    | 2022-06-19 | [Released](https://discuss.mlplatform.org/t/tosa-v0-30-0-released/134) | Base inference profile conformance tests released <br> Main inference floating point precisions added |
            | 0.40    | 2022-08-31 | [Released](https://discuss.mlplatform.org/t/announcing-tosa-v0-40-0/146) | Move to machine readable xml specification for parameters <br> The arguments and data type sections are auto-generated |
            | 0.50    | 2022 Dec | [Released](https://discuss.mlplatform.org/t/announcing-tosa-v0-50-0/161) | Addition of level specification (parameter ranges) |
            | 0.60    | 2023 Mar | [Released](https://discuss.mlplatform.org/t/announcing-tosa-v0-60-0/178) | Main inference draft conformance specification |
            | 0.70    | 2023 Jun | [Released](https://discuss.mlplatform.org/t/announcing-tosa-v0-70-0/201) | Improved use of XML specification version, refine floating-point precision requirements |
            | 0.80    | 2023 Sep | [Released](https://discuss.mlplatform.org/t/announcing-tosa-v0-80-0/229) | ERF/ARGSORT operators, Stateful operators |
            | 0.90    | 2024 Jan | Released | Shape operators |
            | 1.0.0-rc0  | 2024 Apr | Released | Profiles and extensions, establish compatibility point <br> Define compatibility rules <br> - Major version changes may break backwards compatibility <br> - Minor version changes may add functionality in a backwards compatible way <br> - Patch versions are for bug fixes, clarifications, or trivial changes |
            | 1.0.0 | 2024 Aug | Planning | Finalize all issues in TOSA release candidates |
            | 1.x     | 2025 | Concept | Address features and operators not present in 1.0 |

      - format: text
        text_content:
          text: |
            Future release dates subject to change
---
