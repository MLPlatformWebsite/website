# Machine Learning Platform Website

This is the git repository for the Machine Learning Platform static website, built using [Astro](https://astro.build/).

## Project Structure

The content of the website is located in the `src/content` folder of the repo, spread across various folders, referred to as "collections".

```text

├── src/

│   └── content/

│       └── data/

│       └── pages/

│       └── rows/

│       └── sections/

```

## Content

### Pages

Pages can be edited via the relevant `.md` files in the `src/content/pages` folder. The `slug` property of the frontmatter determines the resulting url of the page.

New layouts can be built by adding rows and sections to the `flow` property of a page's frontmatter. This property defines a series of row components that contain section components that make up the page. The `row` property of `flow` and the `component` property of a `sections` item must both reference a filename (without extension) within the `row` and `section` collections respectively. These files in turn contain a path that points to the specified component.

```yaml
- flow:
    - row: container_row
      sections:
        - component: text
```

`container_row` here references `src/content/rows/container_row.md` and `text` references `src/content/sections/text.md`

If a new row or section component is required, please contact [it-support@linaro.org](mailto:it-support@linaro.org).

To render the markdown body of the page `.md` file, please use the `md_content` component as follows.

```yaml
- row: container_row
    sections:
      - component: md_content
```

### Data

The `src/content/data` folder contains various lists of one-off items used in the site, such as nav links, footer links and resources. Any items added to these lists will be reflected in the website.

## Assets

### Images

Images should be placed in the `src/assets` folder and referenced by relative file paths within content collection `.md` files. e.g. `../../assets/images/test_image.jpeg`. This ensures that the images are optimized at build time, improving website performance.

### Docs

Documents should be placed in the `public/docs` folder and referenced by relative url paths within content collection `.md` files e.g. `/docs/test_file.pdf`. This ensures that the documents are hosted on publicly accessible urls.

### Static HTML files

Static html files, such as the TOSA Specification file, should be placed in `public/{path}` where path is the url path after `https://www.mlplatform.org`. e.g. `public/tosa/tosa_spec.html`. The files must be linked to with the `.html` extension included in the `href` value.

## Developer Info

Running the site locally will require `Node.js` (>=18) and the `yarn` package manager.

First, install dependencies with `yarn install`.

The following commands can then be used to build and run the site locally:

| Command        | Description                                                                                                                                                                             |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `yarn build`   | Builds the site in the `dist` folder of the root directory.                                                                                                                             |
| `yarn dev`     | Runs the site in a development server, with hot module replacement to reflect updates to the code as soon as they are saved.                                                            |
| `yarn preview` | Runs the most recent build files in a development server. Unlike `yarn dev` this won't have live updates, but will be a closer representation of the site as it would be in deployment. |

## Questions?

If you have any questions about updating or building this website, please contact Linaro IT Support at [it-support@linaro.org](mailto:it-support@linaro.org).
