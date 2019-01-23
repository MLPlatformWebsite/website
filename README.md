# MlPlatform.org Static Jekyll Website
The MlPlatform.org website is built using the Jekyll static site generator. It is based off of the jumbo-jekyll-theme used for all of the Linaro static sites. With the move from Wordpress to Static we have introduced GitHub/Community driven content that allows MlPlatform.org users to submit issues about any of the pages on MlPlatform.org through the associated Git respository.
*****
## [Looking to add a blog post?](#adding-a-blog-post)
*****
## Contributions
We happy to consider any contributions/feature requests that you may have. Please submit a PR with your changes and we will take a look. You can also use the `Github Edit` buttons available on all the website pages to help locate the file you wish to edit/raise and issue about.
*****
## Contents
- [Overview](#overview)
- [Adding a Content](#adding-a-content)
- [Adding Redirects](#adding-redirects)
- [Building the static site locally](#building-locally)
- [Contributing Guide](#contributing)
*****
# Overview
This website was developed by Linaro and utilises [Jekyll](https://jekyllrb.com), which is a static website generator, to provide a quick and responsive website. This website is part of a CI (Continuous Integration) build which happens on [bamboo.linaro.org](https://bamboo.linaro.org); so if you'd like to see the website builds take place take a look.

## Website Theme
This website uses the `jumbo-jekyll-theme` developed as an open source project by Linaro to ensure content-driven websites are as lightweight as possible. Head over to the [theme repo] to find out more. Here are a few examples of websites using the theme:
- [96Boards.org](https://www.linaro.org)
- [Linaro.org](https://www.96boards.org)
- [connect.linaro.org](https://connect.linaro.org)
- [OP-TEE.org](https://www.op-tee.org)
- [TrustedFirmware.org](https://www.trustedfirmware.org)
- [DeviceTree.org](https://www.devicetree.org)
- [96Boards.ai](https://www.96boards.ai)

## Useful basics
Jekyll used ruby to generate static websites. Jekyll uses Markdown for page content and front matter to describe the meta data of a given page. 

A typical page may look like this:
`/your-new-page.md` or `/your-new-page/README.md`
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
*******
## Adding a page

### Step 1 - Fork the repo
The first step is to fork [this repo] so that you can [submit a pull request] for your website updates.

### Step 1 - Create a file
Website pages are added as markdown files usually in a folder with a `README.md` file beneath to keep everything organised and to ensure content renders on GitHub too (e.g `/services/README.md` or `/services.md`). If your page contains HTML then use the `.html` file extension.

### Step 2 - Add Jekyll front matter to your new page
The url/permalink for your page should be added to the `front matter` of your posts/pages (the section at the top of the file between the set of 3 dashes `---`) as the `permalink` so that your page url is exactly as you intended it to be. See below for an example of the front matter to add to your page. Each theme layout may have different front matter variables that are required so if in any doubt refer to the [theme repo]'s documentation. 

#### Available front matter options
Below is a table of the most common front matter variable to add to your page.

| Front Matter Option | Value | Description  | 
| ------ | ----------- | ----- |
| layout | post | Layout to be used for the page |
| published | false | Set `published` to false if you want to add the page but not show it on the website. |
| title | My Awesome Post | The title of your page/post. Used in the `meta` tags and in layouts to display your page correctly. |
| description | This is an awesome post about MlPlatform.org... | The description of your page used as the `meta` description.|

#### Example front matter
```YAML
---
# Layout of your web page - see below for available layouts.
layout: jumbotron-container
# URL of your page
permalink: /about/
# Title of your page
title: About Us
# Description of your web page.
desc: |-
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy 
    text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has
    survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was 
    popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop
    publishing software like Aldus PageMaker including versions of Lorem Ipsum.
# Keywords that describe your page used as meta keywords.
tags: lorem, ipsum, web, page
jumbotron:
    carousel-images:
        - /assets/images/content/background-image1.jpg
        - /assets/images/content/background-image2.png
        - /assets/images/content/background-image3.jpg
---
```
### Step 2 - Add content to your page


## Adding a blog post

In order to add a blog post to MlPlatform.org copy an existing post from the [_posts folder](https://github.com/MlPlatform.org/website/tree/master/_posts). Posts are organised into by year/month so add to the correct folder based on the month you are posting it in and if the folder doesn't exist create one.

### Step 1 - Modify the post file name
The url for your title is based on the title provided in the filename e.g 2018-06-07-i2s-in-dragonboard410c.md will have a url of /blog/i2s-in-dragonboard410c/. Separate the words in your title by dashes and modify the date at the start of the filename as neccessary. 

### Step 2 - Modify the post front matter
Modify the post front matter based on your post. Values to modify are:
- author:
- date:
- image:
- tags:
- description:

#### Author
Change the author to a unique author shortname. If this is your first time posting then add your author values to the [_data/authors.yml file](https://github.com/MlPlatform.org/website/blob/master/_data/authors.yml). Make sure to add your profile image to the [/assets/images/authors folder](https://github.com/MlPlatform.org/website/tree/master/assets/images/authors). Verify that the author name is an exact match to that provided as the author: in your post.

#### Date
Modify the date to sometime before you post the blog otherwise Jekyll will see it as a __future__ post and not render it until the time on the server exceeds/equals that provided as the date in the post front matter.

#### Image
This value is used for the featured image displayed on your blog post and the image that is used when sharing the blog post on social media sites.

```YAML
image:
    featured: true
    path: /assets/images/blog/DragonBoard-UpdatedImages-front.png
    name: DragonBoard-UpdatedImages-front.png
    thumb: DragonBoard-UpdatedImages-front.png 
    
```

Make sure that the image you add in this section of front matter is placed in the [/assets/images/blog folder](https://github.com/MlPlatform.org/website/tree/master/assets/images/blog).

__Note:__ There is currently a bug with the version of `jekyll-assets` we are using which means the only acceptable image extensions are `.jpg` and `.png`. If you use `.jpeg` you image may not display as expected.


#### Tags
These should be modified based on the content of your post as they are used for Meta keywords so that people can find your post based on the [tags your provide](https://www.MlPlatform.org/blog/tag/).

#### Description
Change this value to a short description of your blog post as this is used for the meta description of your blog post.

### Step 3 - Add your post content.

Write your post content in Markdown format; specifically the [Kramdown](https://kramdown.gettalong.org/) Markdown flavour.

#### Adding images
Please use the following code snipppet to add an image to your blog post. Make sure to add the images that you include to [/assets/images/blog folder](https://github.com/MlPlatform.org/website/tree/master/assets/images/blog).

```
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

```
{% include image.html name="name-of-your-image.png"  class="medium-inline" alt="The Alt text for your image" %}
```

Using this Jekyll include will allow your images to be lazy loaded and format the image HTML correctly.


#### Adding code

We are using the rouge syntax highlighter to highlight your glorious code. 

```bash
$ bundle exec jekyll serve --port 1337
```

See the full list of languages [here](https://github.com/jneen/rouge/wiki/List-of-supported-languages-and-lexers).


#### Adding Media/YouTube videos

To add a media element / YouTube video use the following Jekyll include.

```
{% include media.html media_url="https://youtu.be/GFzJd0hXI0c" %}
```

## Adding Redirects to the Static site

We are using [Edge-rewrite](https://github.com/marksteele/edge-rewrite) which is a rewrite engine running in Lambda@Edge. The redirects are to be added to the `_data/routingrules.json` file in the webiste repository following the syntax rules [here](https://github.com/marksteele/edge-rewrite).

```
^/oldpath/(\\d*)/(.*)$ /newpath/$2/$1 [L]
!^/oldpath.*$ http://www.example.com [R=302,L,NC]
^/topsecret.*$ [F,L]
^/deadlink.*$ [G]
^/foo$ /bar [H=^baz\.com$]
```

__Note:__ These redirects are currently not respected by the link checker until built. So if trying to fix broken links by adding redirects then this may not be the best way to go about it currently. 

*****


# Building the static site

It is not 100% neccessary to build to site on your computer to submit updates but it's helpful if you want to see the updates to big changes before your submit your pull request. You can also trigger a staging build of the site by submititng a pull request to the [develop] branch of [this repo].
We are working towards creating a Docker container for building static Jekyll sites. In the mean time you can still clone the site and install bundler/jekyll gems and ruby to build the site locally or checkout the [official docker container for Jekyll](https://hub.docker.com/r/jekyll/jekyll/) if you are familiar with setting up a container driven environment.

In order to build the [MLPlatform.org] static site make sure you have Ruby and the bundler/jekyll gems installed. For instructions on how to setup a build environment for building Jekyll sites see the official Jekyll documentation [here](https://jekyllrb.com/docs/installation/).

This will install the required gems listed in the Gemfile:

```
$ bundle 
```

This will serve (s) the Jekyll static website to the http://localhost:4000 where you can view the generated static website:

```
$ bundle exec jekyll s 
```

# Contributing
## Simple Changes
<todo>
## Submit a Pull Request
<todo>
## Issues 
If you come across any bugs/issues then please let us know by opening an issue [here](https://github.com/ArmNNWebsite/website/issues/new). Please provide precise details on how to reproduce the bug/issue so that we can act on the issue as soon as possible.

### Known Issues
#### Image file names
Due to the way product images are include, images should not include spaces in the filename otherwise it may not be rendered on the website as expected.

[this repo]: https://github.com/ArmNNWebsite/website
[develop]: https://github.com/ArmNNWebsite/website
[theme repo]: https://github.com/linaro-website/jumbo-jekyll-theme
[submit a pull request]: #submit-a-pull-request
[MLPlatform.org]: https://mlplatform.org

