# Fonts

Currently empty on purpose. The site uses the system font stack
(`'Segoe UI', system-ui, -apple-system, sans-serif`) everywhere, so there
are zero web-font network requests today — no external CDN (e.g. Google
Fonts), no render-blocking font fetch, no flash-of-unstyled-text.

If a custom brand font is added later, self-host it here rather than
pulling from a third-party CDN:

1. Drop the `.woff2` (and `.woff` fallback if you need older-browser
   support) files directly in this folder — do not add a Google
   Fonts/Adobe Fonts `<link>` to `index.html` or the blog template.
2. Declare it with `@font-face` in `index.html`'s `<style>` block:

   ```css
   @font-face {
     font-family: 'YourFont';
     src: url('assets/fonts/YourFont.woff2') format('woff2');
     font-display: swap; /* avoid invisible text while the font loads */
     font-weight: 400 700;
   }
   ```

3. Reference it with a system-font fallback so text is never blocked on
   the font request: `font-family: 'YourFont', 'Segoe UI', system-ui, sans-serif;`
4. Blog post pages (`scripts/_blog_template.html`) load their own
   `<style>` block — update it too if you want the same font there.

Self-hosting avoids the "overlay"/layout-shift a third-party font CDN can
cause (extra DNS/connection round trip, and a visible swap once the font
arrives) and keeps every asset the site depends on inside this repo.
