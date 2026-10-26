# LONGJUN website

This is the existing registered static Site. Its identity is in `.openai/hosting.json`. Preserve its project ID and current audience.

The website contains 17 independent pages: home, company, history, markets, ingredients, three application categories, seven product details, quality and contact. The primary categories are Health (`/health/`), Fragrance (`/fragrance/`) and Raw Material Derivatives (`/derivatives/`). The Origin & Craft page was removed. English is the default; Chinese, French, Japanese, Korean, Spanish and Arabic are provided. Language selection is carried across internal routes.

## Updating content

- `site/content.json`: translations for all seven languages. Add new keys to every language.
- `site/products.json`: existing products, assigned by primary application. Health includes rutin, quercetin and berberine hydrochloride; Fragrance includes Rose Otto; Derivatives includes troxerutin, rhamnose and rose hydrosol. Each product retains its own detail route. Do not publish unconfirmed products as available.
- `site/markets.json`: selected customer countries from the supplied company profile. Markers represent national markets, never exact customer addresses.
- `site/shell.html`: shared navigation and footer.
- `site/sections.json`: retained original visual sections used by the renderer.
- `site/asset-sources.json`: exact image sources, licenses, chemical identity references and use limitations.
- `scripts/render-site.py`: renders all independent HTML pages and the browser translation dictionary.
- `dist/styles.css` and `dist/app.js`: shared styling and language/menu behavior; the renderer preserves these files.

Run `python scripts/render-site.py` after changing content, products or templates. No dependency installation or framework build is required. All files under `dist` are tracked public output.

To change markets, edit `site/markets.json` and run `python scripts/generate-map.py` before rendering the pages. `site/world-polygons.json` contains rounded geometry from Natural Earth 1:110m country boundaries, obtained from the official Natural Earth repository. Natural Earth data are public domain: https://www.naturalearthdata.com/about/terms-of-use/ .

Before publishing, run `python scripts/check-site.py`, `node --check dist/app.js` and `node --check dist/translations.js`. The checks cover links and anchors, every language, unique IDs, one main heading per page, removal of the origin page and preservation of the logo. Use the Sites hosting workflow for publishing.

The contact form creates a visible, copyable draft and a mailto link. It does not automatically send, store or claim to have delivered a message. Product CTAs preselect the material; quality-document requests prefill the document field. No backend email service is configured.

## Content and imagery

Company history and the eight selected customer markets come from the company profile supplied by the user. The user confirmed that rutin, troxerutin, quercetin, rhamnose and berberine hydrochloride remain sold. Do not treat these as discontinued. The rose ingredient origin is China, selected cultivation regions. Do not invent dated milestones, customer identities, certifications, stock levels or product specifications.

The company logo was supplied by the user and remains unchanged. The original rose oil and hero still lifes are illustrative. Category imagery uses a Rosa damascena reference photograph (Виолетова, CC BY-SA 4.0), a Sophora source photograph (Fanghong, CC BY-SA 3.0), and official PubChem molecular structure references. Attribution is available in the footer on every page. Images do not represent owned farms, production batches, grade, purity or stock availability. Rhamnose uses an L-rhamnose reference; berberine hydrochloride uses an anhydrous chloride reference. Confirm the supplied form in product specifications.

The 2026-10-15 execution guide informed the enquiry sequence: application brief, specification and batch documentation, sample evaluation, supply terms and feedback. Existing extracts remain represented. Future materials such as sandalwood are described as sourcing enquiries, not current stock. No unverified testing images or clinical claims are published.
