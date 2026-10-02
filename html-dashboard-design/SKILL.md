---
name: HTML Dashboard Design
description: Apply the Treasure Data brand design system to every HTML file (.html) created in this folder — reports, dashboards, visualizations, tables, and all other HTML deliverables.
---

Whenever you generate any HTML file (`.html`), apply the Treasure Data brand
design system below. This is mandatory for all `.html` deliverables — reports,
dashboards, visualizations, tables, pages, and any other output — no exceptions.

### CSS custom properties (declare at the top of every `<style>` block)

```css
:root {
  --td-primary:      #494FFF;
  --td-secondary-1:  #8753FF;
  --td-secondary-2:  #C466D4;
  --td-accent-lime:  #9DCC4C;
  --td-accent-salmon:#F69068;
  --td-accent-red:   #EE2328;
  --td-gradient:     linear-gradient(135deg, #494FFF, #8753FF, #C466D4);
  --bg:              #F4F4FA;
  --card-bg:         #FFFFFF;
  --text:            #1a1a2e;
  --text-muted:      #64648C;
  --border:          #E2E2EE;
  --radius:          12px;
}
```

### Layout

- Max width: **1200px**, centered
- Body background: `var(--bg)` (`#F4F4FA`)
- Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Monospace (IDs, code, SQL): `'SF Mono', 'Fira Code', monospace`

### Header

- `background: var(--td-gradient)`, white text
- Contains entity/page name + subtitle + optional KPI strip

### KPI / headline values

Render with gradient text:
```css
background: var(--td-gradient);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

### Cards

```css
background: var(--card-bg);
border: 1px solid var(--border);
border-radius: var(--radius);
box-shadow: 0 2px 8px rgba(0,0,0,0.04);
padding: 20px;
```

### Semantic status colors

| State    | Text color | Background  |
|----------|------------|-------------|
| Critical | `#EE2328`  | `#fef2f2`   |
| Warning  | `#f59e0b`  | `#fffbeb`   |
| OK/Good  | `#10b981`  | `#f0fdf4`   |
| Info     | `var(--td-primary)` | — |

### Insight / callout cards (left-border style)

- Info: `border-left: 4px solid var(--td-primary)`
- Positive: `border-left: 4px solid #10b981`
- Caution: `border-left: 4px solid #f59e0b`

### Tab switching — CSS-only (no JavaScript)

Studio's iframe sandbox blocks scripts. Use CSS radio-button tabs:

1. Place `<input type="radio" name="tabs" id="t1" checked>` … `<input id="tN">` as
   direct children of a `.tabs` wrapper.
2. Place `<label for="t1">Tab Name</label>` … `<label for="tN">` as direct children
   of the same `.tabs` wrapper.
3. Place a single `<div class="wrap-c">` containing `<div class="tc c1">` …
   `<div class="tc cN">` panels — also a direct child of `.tabs`.
4. All panels start `display: none`. The checked selector reveals the active one:

```css
.tc { display: none; }
#t1:checked ~ .wrap-c .c1,
#t2:checked ~ .wrap-c .c2,
/* … one line per tab … */
#tN:checked ~ .wrap-c .cN { display: block; }
```

5. Active tab label style:
```css
input[type="radio"]:checked + label {
  background: var(--td-primary);
  color: white;
}
```

6. Use **numeric IDs only**: `t1`/`c1` through `tN`/`cN`. Never descriptive IDs.
7. Default tab is always Tab 1 — add `checked` to `#t1`.

### Segment / entity accent colors

- Consumer dashboards: `var(--td-primary)` (#494FFF)
- Trade firm dashboards: `var(--td-secondary-1)` (#8753FF)
- Designer / trade pro dashboards: `var(--td-secondary-2)` (#C466D4)

### Null / missing data

Always render **"None on file"** or **"N/A"** for null fields. Never omit a section
because data is missing — consistency across reports matters.

### Verification before opening

After writing any tabbed HTML file, verify that every tab has a matching CSS selector
and panel class before calling `mcp__tas__open_file`.
