---
name: html-to-beefree
description: Use when the user wants to convert an HTML email into a BeeFree visual template in Treasure Engage, import HTML into the visual editor, push HTML as a drag-and-drop template, or says "create a visual template from this HTML". Converts raw HTML emails into BeeFree's proprietary JSON format and pushes via the Engage API so the template opens with fully editable blocks in the visual editor.
---

# HTML to BeeFree Visual Template

Convert raw HTML emails into BeeFree Visual Editor templates in Treasure Engage. This skill takes an HTML email file and pushes it as a fully editable drag-and-drop template — not a blank canvas or a single HTML blob.

## Why This Skill Exists

Pushing HTML to Engage with `--editor-type beefree` via `tdx engage template create` results in a **blank canvas**. BeeFree requires its proprietary JSON format (`beefreeJson`) to render editable blocks. This skill builds that JSON manually and pushes via the Engage API directly.

## Workflow

### Step 1: Save the HTML

Save the user's HTML to a local file in the working directory (e.g., `template.html`). Clean up tracking pixels and encrypted click-tracking URLs if present — replace with clean placeholder URLs.

### Step 2: Get Workspace

```bash
tdx engage workspaces
```

Ask the user which workspace to push to. Then get the workspace UUID:

```bash
API_KEY=$(env | grep TDX_API_KEY | head -1 | cut -d= -f2-)
curl -s "https://engage-api.treasuredata.com/api/workspaces" \
  -H "Authorization: TD1 $API_KEY" -H "Accept: application/vnd.api+json" \
  | python3 -c "import json,sys; [print(f'{w[\"id\"]}  {w[\"attributes\"][\"name\"]}') for w in json.load(sys.stdin)['data']]"
```

### Step 3: Analyze the HTML and Build BeeFree JSON

Do NOT rely on the automated `html_to_beefree_json.py` converter — it fails on deeply nested table structures (which most real-world email templates use). Instead, **manually analyze the HTML** and build the BeeFree JSON with a Python script.

Read through the HTML and identify every visual section:
- Headers (logo, navigation, account links)
- Hero images / banners
- Headings and body text
- CTA buttons
- Product cards / promo blocks
- Social media icon rows
- Footer navigation links
- Legal links (terms, privacy, unsubscribe)
- Company info (logo, address, copyright)

### Step 4: Write a Python Build Script

Write a Python script to `/tmp/build_beefree.py` that constructs the BeeFree JSON. **Maximize native modules** — every section should use a native BeeFree module whenever possible. Only fall back to `make_html` for truly irreducible complex layouts.

#### Available Native Modules

| Module | Use For | BeeFree Editor |
|--------|---------|----------------|
| `heading` | h1/h2/h3 headings | Click to edit text |
| `paragraph` | Text blocks, descriptions, inline links | Click to edit text |
| `image` | Images, hero banners, logos | Click to swap image |
| `button` | CTA buttons | Click to edit label/link |
| `divider` | Horizontal rules / separators | Drag to resize |
| `social` | Social media icon rows (Facebook, Instagram, X, TikTok, LinkedIn, etc.) | Add/remove/reorder icons in sidebar |
| `menu` | Navigation link rows (footer links, legal links) | Add/remove/edit menu items in sidebar |

#### Module Mapping Guide

| HTML Pattern | Native Module |
|-------------|---------------|
| Standalone `<h1>`/`<h2>`/`<h3>` | `make_heading` |
| `<p>` text blocks | `make_paragraph` |
| `<img>` standalone images | `make_image` |
| `<table>...<a>` button pattern | `make_button` |
| `<hr>` or border-top dividers | `make_divider` |
| Multiple `<a><img>` social icons side-by-side | `make_social` (NOT html block) |
| Navigation link rows/grids | `make_menu` (NOT html block) |
| Logo + text side-by-side | Multi-column row: `make_image` + `make_paragraph` |
| Logo + nav + account link | Three-column row with native modules |

#### When to Use HTML Blocks (rare)

Only use `make_html` when a section genuinely cannot be represented by any combination of native modules and multi-column rows. This should be uncommon — most email sections can be decomposed into native modules.

#### Builder Functions Reference

```python
import json, uuid

def _uuid():
    return str(uuid.uuid4())

def make_row(columns, bg_color="transparent", content_bg="transparent", row_type="one-column-empty"):
    # row_type: "one-column-empty", "two-columns-empty", "three-columns-empty"
    return {
        "columns": columns,
        "container": {"style": {"background-color": bg_color, "background-image": "none", "background-position": "top left", "background-repeat": "no-repeat"}},
        "content": {
            "computedStyle": {"hideContentOnDesktop": False, "hideContentOnMobile": False, "rowColStackOnMobile": True, "rowReverseColStackOnMobile": False, "verticalAlign": "top"},
            "style": {"background-color": content_bg, "background-image": "none", "background-position": "top left", "background-repeat": "no-repeat", "color": "#000000", "width": "600px"}
        },
        "empty": False, "locked": False, "synced": False, "type": row_type, "uuid": _uuid()
    }

def make_column(modules, grid_cols=12, bg_color="transparent", padding=None):
    # grid_cols: 12=full, 6=half, 4=third, 3=quarter. Columns in a row must sum to 12.
    if padding is None:
        padding = {"padding-top": "0px", "padding-bottom": "0px", "padding-left": "0px", "padding-right": "0px"}
    return {
        "grid-columns": grid_cols, "modules": modules,
        "style": {"background-color": bg_color, "border-bottom": "0px solid transparent", "border-left": "0px solid transparent", "border-right": "0px solid transparent", "border-top": "0px solid transparent", **padding},
        "uuid": _uuid()
    }

def make_heading(text, level="h1", color="#333333", font_size="24px", align="center", font_family="Arial, Helvetica, sans-serif", font_weight="bold", padding=None):
    if padding is None:
        padding = {"padding-top": "10px", "padding-bottom": "10px", "padding-left": "30px", "padding-right": "30px", "text-align": align, "width": "100%"}
    return {
        "align": align,
        "descriptor": {
            "computedStyle": {"height": 42, "width": 52},
            "heading": {"style": {"color": color, "direction": "ltr", "font-family": font_family, "font-size": font_size, "font-weight": font_weight, "letter-spacing": "0px", "line-height": "120%", "link-color": "#0068A5", "text-align": align}, "text": text, "title": level},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-heading", "uuid": _uuid()
    }

def make_paragraph(html, color="#333333", font_size="16px", align="center", font_family="Arial, Helvetica, sans-serif", padding=None, link_color="#0068A5"):
    if padding is None:
        padding = {"padding-top": "5px", "padding-bottom": "5px", "padding-left": "30px", "padding-right": "30px"}
    return {
        "descriptor": {
            "computedStyle": {"hideContentOnAmp": False, "hideContentOnDesktop": False, "hideContentOnHtml": False, "hideContentOnMobile": False},
            "paragraph": {"computedStyle": {"linkColor": link_color}, "html": html, "style": {"color": color, "font-family": font_family, "font-size": font_size, "line-height": "160%", "text-align": align}},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-paragraph", "uuid": _uuid()
    }

def make_image(src, alt, width="600", href="", padding=None):
    if padding is None:
        padding = {"padding-top": "0px", "padding-bottom": "0px", "padding-left": "0px", "padding-right": "0px", "width": "100%"}
    return {
        "align": "center",
        "descriptor": {
            "computedStyle": {"class": "center fixedwidth", "width": f"{width}px"},
            "image": {"alt": alt, "height": "auto", "href": href, "percWidth": 100, "prefix": "", "src": src, "target": "_self", "width": f"{width}px"},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-image", "uuid": _uuid()
    }

def make_button(label, href="#", bg_color="#c22032", text_color="#ffffff", font_size="18px", align="center", border_radius="4px", padding=None):
    if padding is None:
        padding = {"padding-top": "10px", "padding-bottom": "10px", "padding-left": "10px", "padding-right": "10px", "text-align": align}
    return {
        "align": align,
        "descriptor": {
            "button": {"href": href, "label": f'<div class="txtTinyMce-wrapper"><p style="word-break:break-word;">{label}</p></div>', "style": {"background-color": bg_color, "border-bottom": "0px solid transparent", "border-left": "0px solid transparent", "border-radius": border_radius, "border-right": "0px solid transparent", "border-top": "0px solid transparent", "color": text_color, "direction": "ltr", "font-family": "Arial, Helvetica, sans-serif", "font-size": font_size, "font-weight": "700", "letter-spacing": "0.02em", "line-height": "200%", "max-width": "100%", "padding-bottom": "5px", "padding-left": "25px", "padding-right": "25px", "padding-top": "5px", "width": "auto"}, "target": "_blank"},
            "computedStyle": {"height": 46, "hideContentOnMobile": False, "width": 250},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-button", "uuid": _uuid()
    }

def make_divider(color="#cccccc", height="1px", padding=None):
    if padding is None:
        padding = {"padding-top": "0px", "padding-bottom": "0px", "padding-left": "0px", "padding-right": "0px"}
    return {
        "descriptor": {
            "computedStyle": {"align": "center", "hideContentOnMobile": False},
            "divider": {"style": {"border-top": f"{height} solid {color}", "height": "0px", "width": "100%"}},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-divider", "uuid": _uuid()
    }

def make_social(icons, icon_set="t-circle-white", icon_width=32, padding=None):
    """Native social media icon module.
    icons: [{"id": "facebook", "name": "Facebook", "href": "https://..."}]
    Available ids: facebook, instagram, x, tiktok, linkedin, youtube, pinterest, twitter
    Icon sets: t-circle-white, t-circle-dark, t-outline, t-only, etc.
    """
    if padding is None:
        padding = {"padding-top": "10px", "padding-bottom": "10px", "padding-left": "10px", "padding-right": "10px", "text-align": "center"}
    icon_list = []
    for icon in icons:
        icon_list.append({
            "id": icon["id"],
            "image": {
                "alt": icon["name"], "href": icon["href"], "prefix": icon["href"],
                "src": f"https://app-rsrc.getbee.io/public/resources/social-networks-icon-sets/{icon_set}/{icon['id']}@2x.png",
                "target": "_blank", "title": icon["name"]
            },
            "name": icon["name"], "text": "", "type": "follow"
        })
    return {
        "descriptor": {
            "computedStyle": {"height": icon_width + 25, "hideContentOnMobile": False, "iconsDefaultWidth": icon_width, "padding": "0 10px 0 10px", "width": len(icons) * (icon_width + 20)},
            "iconsList": {"icons": icon_list},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-social", "uuid": _uuid()
    }

def make_menu(items, font_size="14px", color="#ffffff", link_color="#ffffff", letter_spacing="0px", font_weight="400", padding=None):
    """Native menu/navigation module.
    items: [{"text": "Find a Store", "href": "https://..."}]
    Renders as a horizontal row of links. Collapses to hamburger on mobile.
    """
    if padding is None:
        padding = {"padding-top": "0px", "padding-bottom": "0px", "padding-left": "0px", "padding-right": "0px"}
    menu_items = []
    for item in items:
        menu_items.append({"id": _uuid(), "link": {"href": item["href"], "target": "_blank", "title": ""}, "text": item["text"]})
    return {
        "descriptor": {
            "computedStyle": {
                "hamburger": {"backgroundColor": "#333333", "foregroundColor": "#ffffff", "iconSize": "36px", "iconType": "normal", "mobile": True},
                "hideContentOnDesktop": False, "hideContentOnMobile": False,
                "layout": "horizontal", "linkColor": link_color,
                "menuItemsSpacing": {"padding-bottom": "10px", "padding-left": "15px", "padding-right": "15px", "padding-top": "10px"}
            },
            "menuItemsList": {"items": menu_items},
            "style": {"color": color, "font-family": "Arial, Helvetica, sans-serif", "font-size": font_size, "font-weight": font_weight, "letter-spacing": letter_spacing, **padding, "text-align": "center"}
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-menu", "uuid": _uuid()
    }

def make_html(html_content, padding=None):
    """Raw HTML block — use only as a last resort for irreducibly complex layouts."""
    if padding is None:
        padding = {"padding-top": "0px", "padding-bottom": "0px", "padding-left": "0px", "padding-right": "0px"}
    return {
        "descriptor": {
            "computedStyle": {"hideContentOnAmp": False, "hideContentOnDesktop": False, "hideContentOnHtml": False, "hideContentOnMobile": False},
            "html": {"html": html_content},
            "style": padding
        },
        "locked": False, "type": "mailup-bee-newsletter-modules-html", "uuid": _uuid()
    }
```

#### Multi-Column Rows

Use multi-column rows for side-by-side layouts (headers, company info sections):

```python
# Two-column: logo left + text right
make_row([
    make_column([make_image(...)], grid_cols=6),
    make_column([make_paragraph(...)], grid_cols=6)
], row_type="two-columns-empty")

# Three-column: logo + points + account link
make_row([
    make_column([make_image(...)], grid_cols=3),
    make_column([make_paragraph(...)], grid_cols=5),
    make_column([make_paragraph(...)], grid_cols=4)
], row_type="three-columns-empty")
```

Column `grid_cols` must sum to 12 within a row.

#### Page Wrapper

After building all rows, wrap them in the page structure:

```python
beefree_json = {
    "page": {
        "body": {
            "container": {"style": {"background-color": "<page_bg_color>"}},
            "content": {
                "computedStyle": {"linkColor": "<link_color>", "messageBackgroundColor": "transparent", "messageWidth": "600px"},
                "style": {"color": "<text_color>", "font-family": "Arial, Helvetica, sans-serif"}
            },
            "type": "mailup-bee-page-properties",
            "webFonts": []
        },
        "description": "",
        "rows": rows,
        "template": {"name": "template-base", "type": "basic", "version": "2.0.0"},
        "title": "<template_name>"
    },
    "comments": {}
}
```

Run the script to produce `/tmp/beefree_output.json`:

```bash
python3 /tmp/build_beefree.py
```

### Step 5: Push via Engage API

Push with both `htmlTemplate` and `beefreeJson` via the API:

```python
import json, subprocess, os

html = open('<html_file_path>').read()
beefree = json.load(open('/tmp/beefree_output.json'))

payload = {
    "data": {
        "type": "emailTemplates",
        "attributes": {
            "name": "<template_name>",
            "subjectTemplate": "<subject_line>",
            "htmlTemplate": html,
            "editorType": "beefree",
            "workspaceId": "<workspace_uuid>",
            "beefreeJson": beefree  # MUST be a dict, NOT json.dumps()
        }
    }
}

API_KEY = next((v for k, v in os.environ.items() if k.startswith("TDX_API_KEY") and v), "")
result = subprocess.run(
    ["curl", "-s", "-X", "POST",
     "https://engage-api.treasuredata.com/api/email_templates",
     "-H", f"Authorization: TD1 {API_KEY}",
     "-H", "Content-Type: application/vnd.api+json",
     "-H", "Accept: application/vnd.api+json",
     "-d", json.dumps(payload, ensure_ascii=False)],
    capture_output=True, text=True, timeout=30
)
resp = json.loads(result.stdout)
```

To **update** an existing template, use `PATCH` instead of `POST` and include `"id"` in the `data` object:

```python
payload["data"]["id"] = "<template_id>"
# Use PATCH to: https://engage-api.treasuredata.com/api/email_templates/<template_id>
```

**Region URLs:**
- US01: `https://engage-api.treasuredata.com`
- AP01: `https://engage-api.treasuredata.co.jp`
- EU01: `https://engage-api.eu01.treasuredata.com`

### Step 6: Report Success

Print the template ID and the Engage Studio URL:

```
Template ID: <uuid>
Studio URL: https://console-next.us01.treasuredata.com/app/es/<workspace_id>/em/<template_id>/ce
```

## Critical Rules

1. **beefreeJson must be a dict (object), NOT a JSON string.** The API returns `ENGAGE_API_SHOULD_BE_AN_OBJECT` if you pass `json.dumps()` instead of a raw dict.
2. **Use `htmlTemplate`, not `html`.** The API returns `"html is not allowed"` if you use the wrong key.
3. **Use `emailTemplates` (camelCase)** as the JSON:API type, not `email_templates`.
4. **Do NOT use `tdx engage template create --editor-type beefree`** — it does not send `beefreeJson` and results in a blank canvas.
5. **Every text paragraph must wrap content in** `<p style="word-break:break-word;">...</p>`.
6. **Maximize native modules.** Use `make_social` for social icons, `make_menu` for nav/footer links, and multi-column rows for side-by-side layouts. Only use `make_html` for truly irreducible layouts. Native modules are fully editable in the visual editor; HTML blocks require raw HTML editing.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Blank canvas in BeeFree editor | `beefreeJson` is missing or was stringified. Re-push with `beefreeJson` as a dict. |
| Only header/footer visible, content missing | The HTML parser couldn't traverse nested tables. Build BeeFree JSON manually (Step 3-4). |
| `ENGAGE_API_SHOULD_BE_AN_OBJECT` | You passed `json.dumps(beefree)` — pass the dict directly. |
| `"html is not allowed"` | Use `htmlTemplate` not `html` as the attribute key. |
| `"has already been taken"` | A template with the same name exists. Delete first: `tdx engage template delete "Name" --workspace "Workspace" --yes` |
| Social icons not editable | You used `make_html` for social icons — use `make_social` instead for native drag-and-drop editing. |
| Footer links not editable | You used `make_html` for nav links — use `make_menu` instead for native menu editing. |

## Example

**Input:** User provides an HTML email file for a Sheetz soda promotion.

**Process:**
1. Save HTML, ask for workspace
2. Analyze HTML: identify header (logo + points + My Account), hero image, promo heading, body text, disclaimer, product image, CTA card with button, social icons, footer links, legal links, company info
3. Build Python script with 12 rows — **all native modules (0 HTML blocks)**:
   - Row 1: Three-column row — `image` (logo) + `paragraph` (points) + `paragraph` (My Account link)
   - Row 2: `image` (hero banner)
   - Row 3: `heading` (promo title)
   - Row 4: `paragraph` (body text)
   - Row 5: `paragraph` (disclaimer)
   - Row 6: `image` (product image)
   - Row 7: `heading` + `paragraph` + `button` + `paragraph` (CTA card with white column bg)
   - Row 8: `social` (Facebook, Instagram, X, TikTok)
   - Row 9: `menu` (Find a Sheetz, Sheetz.com, My Savingz, My Rewardz, Order Now, Get the app)
   - Row 10: `divider`
   - Row 11: `menu` (Terms, View in browser, Privacy, Preferences, Unsubscribe)
   - Row 12: Two-column row — `image` (Sheetz logo) + `paragraph` (address)
4. Push via API with both htmlTemplate and beefreeJson
5. User opens in BeeFree and can drag-and-drop edit **every single element** — including social icons and footer links