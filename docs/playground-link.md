# The public WordPress demo link

GitHub Pages cannot run PHP, so the live WordPress site is a WordPress Playground (WordPress running in the browser) that boots this theme from the public repository.

**Link (works once `main` has this branch merged and pushed):**
https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/chipmartens/tumbleweeds-vbc-theme/main/seed/blueprint-remote.json

## What `seed/blueprint-remote.json` does
1. Logs in as `admin` (password `password`, a throwaway site that lives in the visitor's browser), so wp-admin is explorable.
2. Installs Secure Custom Fields and Classic Editor from wordpress.org.
3. Installs the theme from `https://github.com/chipmartens/tumbleweeds-vbc-theme/archive/refs/heads/main.zip` with `targetFolderName: tumbleweeds-vbc`. GitHub's zip has a top folder called `tumbleweeds-vbc-theme-main`; the option renames it to the theme slug the seed expects. Playground fetches the zip through its own CORS proxy (verified in the live Playground with another public GitHub zip).
4. Runs the theme's own `seed/import.php`. The seed (`seed/content.json`) and the 13 placeholder photos (`seed/img/`) ship inside the theme zip, so nothing else is fetched. The import sets the front page and News page, permalinks, both menus, Club settings, coaches and posts.
5. Lands on `/` (the home page).

## What stays out of the zip
`.gitattributes` marks `v2/`, `tools/`, `.cursor/`, `package-lock.json` as `export-ignore`, so the GitHub zip is about 4 MB: the theme, its compiled CSS and JS, and the seed.

## Re-test after pushing
```
npx @wp-playground/cli@latest server --blueprint seed/blueprint-remote.json --port 9411
```
(open the URL once, the CLI auto-logs in). Or open the link above in a browser. The demo site is `noindex` (the import sets `blog_public` to 0) and nothing a visitor changes is saved anywhere except their own browser tab.
