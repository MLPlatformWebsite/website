# mlplatform.org Static Jekyll Website

This is the git repository for static Jekyll-based mlplatform.org website (<https://mlplatform.org/>).

Hosted in this repo are the markdown content files associated with the website. Feel free to [submit a PR](https://github.com/ArmNNWebsite/website/pulls) / [Issue](https://github.com/ArmNNWebsite/website/issues/new) if there is anything you would like to change.

This static Jekyll site is using the [`jumbo-jekyll-theme`](https://github.com/linaro-marketing/jumbo-jekyll-theme). Please take a moment to review the guides on the [theme's GitHub wiki](https://github.com/linaro-marketing/jumbo-jekyll-theme/wiki).

*****

## Contributing

To make it easier to contribute to the content, Linaro provides a couple of Docker containers for building and checking the site. All you need is Docker installed on your computer and enough RAM and disc space.

To build the site:

```bash
cd <git repository directory>
./build-site.sh
```

To build the site and then serve it so that you can check your contribution appears:

```bash
cd <git repository directory>
JEKYLL_ACTION="serve" ./build-site.sh
```

To check that your contribution doesn't include any broken links:

```bash
cd <built web site directory>
../check-links.sh
```

The built web site directory will be `production.mlplatform.org`.

For more information, please see the [build container wiki](https://github.com/linaro-its/jekyll-build-container/wiki) and the [link checker wiki](https://github.com/linaro-its/jekyll-link-checker/wiki).

## GitHub / AWS Authentication

A public GitHub runner is used to deploy the built website. To obtain temporary credentials, an OIDC process is used. This requires a one-off configuration process on the AWS account hosting the S3 bucket and CloudFront distribution.

### Step 1: Configure the OIDC Provider in AWS IAM

Log in to your AWS Management Console and navigate to the IAM service.

In the left-hand navigation pane, click on Identity providers.

Click the Add provider button.

For the Provider type, select OpenID Connect.

In the Provider URL field, enter:

https://token.actions.githubusercontent.com

For the Audience field, enter:

sts.amazonaws.com

Click Add provider to save it.

### Step 2: Create the IAM Role for GitHub Actions

In the IAM dashboard, click on Roles in the left-hand navigation pane.

Click the Create role button.

For Trusted entity type, select Web identity.

Under Identity provider, choose the token.actions.githubusercontent.com provider you just created.

For the Audience, select sts.amazonaws.com.

Click Next.

Attach Permissions: On the "Add permissions" page, search for and add the policies your workflow needs (e.g., AmazonS3FullAccess, AmazonEC2FullAccess). Note that AdministratorAccess is permissible but may be too broad.

Security Best Practice: Always follow the principle of least privilege. It's better to create a custom policy with only the exact permissions your workflow needs, rather than using broad "FullAccess" policies.

Click Next.

Name your role: github-actions-oidc-role.

Review and Create: Review the details and click Create role.

Get the ARN: After the role is created, click on its name in the list and copy the ARN (Amazon Resource Name) from the summary page. Update `role-to-assume` in `push.yml` with the ARN.
