# mlplatform.org Static Jekyll Website

This is the git repository for static Jekyll-based mlplatform.org website (https://mlplatform.org/).

Hosted in this repo are the markdown content files associated with the website. Feel free to [submit a
PR](https://github.com/ArmNNWebsite/website/pulls) / [Issue](https://github.com/ArmNNWebsite/website/issues/new) if there is anything you would like to change.

This static Jekyll site is using the [`jumbo-jekyll-theme`](https://github.com/linaro-marketing/jumbo-jekyll-theme). Please take a moment to review the guides on the [theme's GitHub wiki](https://github.com/linaro-marketing/jumbo-jekyll-theme/wiki).

*****

## Contributing

To make it easier to contribute to the content, Linaro provides a couple of Docker containers for building and checking the site. All you need is Docker installed on your computer and enough RAM and disc space.

To build the site:

```
cd <git repository directory>
./build-site.sh
```

To build the site and then serve it so that you can check your contribution appears:

```
cd <git repository directory>
JEKYLLACTION="serve" ./build-site.sh
```

To check that your contribution doesn't include any broken links:

```

cd <built web site directory>
../check-links.sh
```

The built web site directory will be `staging.mlplatform.org` unless you set `JEKYLLENV=production` before building the site, in which case the directory will be `production.mlplatform.org`.

For more information, please see the [build container wiki](https://github.com/linaro-its/jekyll-build-container/wiki) and the [link checker wiki](https://github.com/linaro-its/jekyll-link-checker/wiki).

*****

## Table of Contents

<!-- TOC -->

- [mlplatform.org Static Jekyll Website](#mlplatformorg-static-jekyll-website)
  - [Table of Contents](#table-of-contents)
  - [Website Theme](#website-theme)
  - [Useful basics](#useful-basics)
  - [Adding a page](#adding-a-page)
    - [Step 1 - Fork the repo](#step-1---fork-the-repo)
    - [Step 2 - Create a file](#step-2---create-a-file)
    - [Step 3 - Add Jekyll front matter to your new page](#step-3---add-jekyll-front-matter-to-your-new-page)
      - [Available front matter options](#available-front-matter-options)
      - [Example front matter](#example-front-matter)
  - [Adding a blog post](#adding-a-blog-post)
    - [Step 1 - Modify the post file name](#step-1---modify-the-post-file-name)
    - [Step 2 - Modify the post front matter](#step-2---modify-the-post-front-matter)
      - [Author](#author)
      - [Date](#date)
      - [Image](#image)
      - [Tags](#tags)
      - [Description](#description)
    - [Step 3 - Add your post content](#step-3---add-your-post-content)
      - [Adding images](#adding-images)
      - [Adding code](#adding-code)
      - [Adding Media/YouTube videos](#adding-mediayoutube-videos)
  - [Adding Redirects to the Static site](#adding-redirects-to-the-static-site)
  - [Building the static site](#building-the-static-site)
    - [Build instructions](#build-instructions)
  - [Issues](#issues)
  - [Known Issues](#known-issues)
    - [Image file names](#image-file-names)

<!-- /TOC -->

## Website Theme

This website uses the `jumbo-jekyll-theme` developed as an open source project by Linaro to ensure content-driven websites are as lightweight as possible. Head over to the [theme repo] to find out more. Here are a few examples of websites using the theme:

- [96Boards.ai](https://www.96boards.ai)
- [96Boards](https://www.96boards.org)
- [DeviceTree.org](https://www.devicetree.org)
- [Linaro Connect](https://connect.linaro.org)
- [Linaro](https://www.linaro.org)
- [OP-TEE](https://www.op-tee.org)
- [TrustedFirmware](https://www.trustedfirmware.org)

## Useful basics

Jekyll uses Markdown for page content and front matter to describe the meta data of a given page.

A typical page may look like this: `/your-new-page.md` or `/your-new-page/README.md`

```yaml
---
# The url your page will be visible at
permalink: /your-new-page/
# Meta title for your page
title: Your new page
# Meta description of your page.
description: >-
    This is your page description which will be visible in search engines and more.
# Tags are used by theme to add meta keywords to a page
tags:
  - jekyll
  - update
  - 2019
# Provides the layout used to create the page
layout: jumbotron-container
---
<YOUR MARKDOWN CONTENT GOES HERE>
```

Above is a basic example of a Jekyll page. Each layout may have different front matter that it requires to be rendered correctly. For example the `jumbo-jekyll-theme`'s `jumbotron-container` layout uses the following front matter to add a header image carousel or video/image banner to your page.

```yaml
---
jumbotron:
    # Default background image
    image: /assets/images/content/bkk19-vertical-white-sm.png
    # Banner Title
    title: Bringing the Arm ecosystem together
    # Custom include file
    include: your-custom-include.html
    # Description to display beneath the title
    description: ""
    # Adds a background video to your header
    video:
        # Video sources as mp4,ogv and webm for cross browser support.
        source:
            mp4: https://s3.amazonaws.com/static-linaro-org/connect/assets/videos/LinaroConnectPromo.mp4
            ogv: https://s3.amazonaws.com/static-linaro-org/connect/assets/videos/LinaroConnectPromo.ogv
            webm: https://s3.amazonaws.com/static-linaro-org/connect/assets/videos/LinaroConnectPromo.webm
        # Video poster displays for first frame of video is received.
        poster: /assets/images/content/bkk19-bg.jpg
    # Animation to use on the header elements
    animation: fade
---
```

The above snippet is used for the [Linaro Connect homepage](https://connect.linaro.org).

## Adding a page

### Step 1 - Fork the repo

The first step is to fork [this repo] so that you can [submit a pull request] for your website updates.

### Step 2 - Create a file

Website pages are added as markdown files usually in a folder with a `README.md` file beneath to keep everything organised and to ensure content renders on GitHub too (e.g `/services/README.md` or `/services.md`). If your page contains HTML then use the `.html` file extension.

### Step 3 - Add Jekyll front matter to your new page

The url/permalink for your page should be added to the `front matter` of your posts/pages (the section at the top of the file between the set of 3 dashes `---`) as the `permalink` so that your page url is exactly as you intended it to be. See below for an example of the front matter to add to your page. Each theme layout may have different front matter variables that are required so if in any doubt refer to the [theme repo]'s documentation.

#### Available front matter options

Below is a table of the most common front matter variable to add to your page.

| Front Matter Option | Value | Description  |
| ------ | ----------- | ----- |
| layout | post | Layout to be used for the page |
| published | false | Set `published` to false if you want to add the page but not show it on the website. |
| title | My Awesome Post | The title of your page/post. Used in the `meta` tags and in layouts to display your page correctly. |
| description | This is an awesome post about mlplatform.org... | The description of your page used as the `meta` description.|

#### Example front matter

```yaml
---
# Layout of your web page - see below for available layouts.
layout: jumbotron-container
# URL of your page
permalink: /about/
# Title of your page
title: About Us
# Description of your web page.
desc: |-
    Lorem ipsum dolor sit amet, consecteteur adipiscing elit luctus nam quam phasellus sapien.
    Natoque ut, ad ligula neque blandit turpis in ut congue. Venenatis cubilia, leo vehicula neque at lacus aenean.
    Euismod velit enim habitant hac. Fusce nam luctus montes convallis ut, fringilla. At, nascetur nisi per eget cum. Justo pellentesque venenatis semper eros condimentum.
# Keywords that describe your page used as meta keywords.
tags: lorem, ipsum, web, page
jumbotron:
    carousel-images:
        - /assets/images/content/background-image1.jpg
        - /assets/images/content/background-image2.png
        - /assets/images/content/background-image3.jpg
---
```

## Adding a blog post

In order to add a blog post to mlplatform.org, copy an existing post from the [_posts folder](https://github.com/ArmNNWebsite/website/tree/master/_posts). Posts are organised into by year/month so add to the correct folder based on the month you are posting it in and if the folder doesn't exist create one.

### Step 1 - Modify the post file name

The url for your title is based on the filename. For example, a file called `2018-06-07-i2s-in-dragonboard410c.md` will have a url of `/blog/i2s-in-dragonboard410c/`. Separate the words in your title by dashes and modify the date at the start of the filename as neccessary.

### Step 2 - Modify the post front matter

Values to modify are:

- author:
- date:
- image:
- tags:
- description:

See existing files for examples.

#### Author

Change the author to a unique author shortname. If this is your first time posting then add your author values to the [_data/authors.yml file](https://github.com/ArmNNWebsite/website/blob/master/_data/authors.yml). Make sure to add your profile image to the [/assets/images/authors folder](https://github.com/ArmNNWebsite/website/tree/master/assets/images/authors). Verify that the author name is an exact match to that provided as the author: in your post.

#### Date

Modify the date to sometime before you post the blog otherwise Jekyll will see it as a **future** post and not render it until the time on the server exceeds/equals that provided as the date in the post front matter.

#### Image

This value is used for the featured image displayed on your blog post and the image that is used when sharing the blog post on social media sites.

```yaml
image:
    featured: true
    path: /assets/images/blog/DragonBoard-UpdatedImages-front.png
    name: DragonBoard-UpdatedImages-front.png
    thumb: DragonBoard-UpdatedImages-front.png
```

Make sure that the image you add in this section of front matter is placed in the [/assets/images/blog folder](https://github.com/ArmNNWebsite/website/tree/master/assets/images/blog).

**Note:** There is currently a bug with the version of `jekyll-assets` we are using which means the only acceptable image extensions are `.jpg` and `.png`. If you use `.jpeg` your image may not display as expected.

#### Tags

These should be modified based on the content of your post as they are used for Meta keywords so that people can find your post based on the [tags you provide](https://www.mlplatform.org/blog/tag/).

#### Description

Change this value to a short description of your blog post as this is used for the meta description of your blog post.

### Step 3 - Add your post content

Write your post content in Markdown format; specifically the [Kramdown](https://kramdown.gettalong.org/) Markdown flavour.

#### Adding images

Please use the following code snipppet to add an image to your blog post. Make sure to add the images that you include to [/assets/images/blog folder](https://github.com/ArmNNWebsite/website/tree/master/assets/images/blog).

```liquid
{% include image.html name="name-of-your-image.png" alt="The Alt text for your image" %}
```

You also align/scale your image using the following css classes.

|Class|Details|
|-----|-------|
|small-inline|Small image aligned to the left|
|small-inline right| Small image aligned to the right|
|medium-inline|Medium image aligned to the left|
|medium-inline right|Medium image aligned to the right|
|large-inline|Large image aligned to the left|
|large-inline right|Large image aligned to the right|

```liquid
{% include image.html name="name-of-your-image.png"  class="medium-inline" alt="The Alt text for your image" %}
```

Using this Jekyll include will allow your images to be lazy loaded and format the image HTML correctly.

#### Adding code

We use the [Rouge](http://rouge.jneen.net/) syntax highlighter to highlight your glorious code.

```bash
bundle exec jekyll serve --port 1337
```

See the full list of languages [here](https://github.com/jneen/rouge/wiki/List-of-supported-languages-and-lexers).

#### Adding Media/YouTube videos

To add a media element / YouTube video use the following Jekyll include.

```liquid
{% include media.html media_url="https://youtu.be/$VIDEO_ID" %}
```

Replace `$VIDEO_ID` as required.

## Adding Redirects to the Static site

We are using [edge-rewrite](https://github.com/marksteele/edge-rewrite) running on Lambda@Edge for redirects. The redirects must be added to the `_data/routingrules.json` file following the syntax rules [here](https://github.com/marksteele/edge-rewrite). Some example rewrite directives:

```mod_rewrite
^/oldpath/(\\d*)/(.*)$ /newpath/$2/$1 [L]
!^/oldpath.*$ http://www.example.com [R=302,L,NC]
^/topsecret.*$ [F,L]
^/deadlink.*$ [G]
^/foo$ /bar [H=^baz\.com$]
```

**Note:** These redirects are not evaluated by the link checker until the site build process has started. For internal broken links, please update the referencing pages so that the links are no longer broken: **do not** use redirects for internal broken links.

## Known Issues

### Image file names

Due to the way product images are included, images should not include spaces in the filename otherwise it may not be rendered on the website as expected.
