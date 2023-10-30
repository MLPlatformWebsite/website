---
title: Contributing
description: >-
  Contributions are welcome to Arm NN and the Compute Library. The projects are licensed under the MIT license and all accepted contributions must have the same license.
slug: contributing/
layout: ../../layouts/Flow.astro
hero:
  title: Contributing
flow:
  - row: container_row
    sections:
      - component: text
        text_content:
          text: |-
            Contributions are welcome to Arm NN and the Compute Library. The projects are licensed under the [MIT license](https://spdx.org/licenses/MIT.html) and all accepted contributions must have the same license.

            To contribute to a machine learning platform repository, please put a change request on [review.mlplatform.org](https://review.mlplatform.org/). (Please do not make pull requests on the GitHub repositories.)

            ## Developer Certificate of Origin (DCO)

            Before the machine learning platform project can accept your contribution, you must certify its origin and give us your permission.  To manage this process we use the Developer Certificate of Origin (DCO) V1.1 ([https://developercertificate.org/](https://developercertificate.org/))

            To indicate that you agree to the terms of the DCO, you "sign off" your contribution by adding a line with your name and e-mail address to every git commit message:

            Signed-off-by: John Doe <john.doe@example.org>

            You must use your real name. No pseudonyms or anonymous contributions are accepted.

            ## Development Repositories

            |Project|Repository|
            |-------|----------|
            |Arm NN	|[https://review.mlplatform.org/#/admin/projects/ml/armnn](https://review.mlplatform.org/#/admin/projects/ml/armnn)|
            |Compute Library|[https://review.mlplatform.org/#/admin/projects/ml/ComputeLibrary](https://review.mlplatform.org/#/admin/projects/ml/ComputeLibrary)|
            |Arm Android NN Driver|[https://review.mlplatform.org/#/admin/projects/ml/android-nn-driver](https://review.mlplatform.org/#/admin/projects/ml/android-nn-driver)|

            ## Code Reviews

            Contributions to the machine learning platform must go through code review. Code reviews are performed through the [mlplatform.org Gerrit server](https://review.mlplatform.org/). Contributors must sign up to this server with their GitHub account credentials.

            Only reviewed contributions can go to the master branch of any of the machine learning platform repositories.

            Build system can only be triggered by Arm employees for security reasons - please comment on review to request an Engineer to do so.

            ## Continuous Integration

            Contributions to machine learning platform codebases go through testing at the Arm CI system. All unit, integration and regression
            tests must pass before a contribution will be merged to a repository’s master branch.

            ## Release Policy

            The machine learning platform projects will be released every three months in February, May, August and November, see [Releases](/releases/) for details of the latest updates.
---
