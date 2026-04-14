# Simple GitHub Pages package for one Markdown homepage

This package is intentionally minimal.

## Files you should care about

- `index.md` - the homepage content and the only file you will normally edit
- `_config.yml` - one-time site settings
- `assets/css/style.scss` - optional styling overrides

## How to publish it

1. Create a GitHub repository.
2. Upload the contents of this folder to the repository root.
3. In **Settings -> Pages**, change **Source** to **Deploy from a branch**.
4. Choose **main** and **/(root)**, then click **Save**.
5. Wait a minute and open the site URL shown by GitHub Pages.

## Important one-time check

This package assumes your repository is named:

`safety-case-core-guidelines`

If you use a different repository name, update this line in `_config.yml`:

`baseurl: "/safety-case-core-guidelines"`

For example, if your repo is named `my-guidelines`, change it to:

`baseurl: "/my-guidelines"`

If your repository is named `<your-user>.github.io`, leave `baseurl` empty:

`baseurl: ""`

## Daily editing workflow

Edit `index.md` directly on GitHub.
