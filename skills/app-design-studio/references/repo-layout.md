# Repo layout and schemas

```
design/<app-slug>/
  DESIGN.md              locked bible (human-readable)
  tokens.json            design tokens (machine-readable)
  inventory.json         every screen/state/dialog/sheet planned
  STATUS.md              phase status, decisions, regenerations
  HANDOFF.md             how developers/agents use this repo
  flow-map.md            screen-to-screen navigation (mermaid ok)
  screens/
    entry/  auth/  home/  feature/  detail/  search/  profile/  settings/  system/
      <id>.png           portrait UI only, no frame
      <id>.spec.json     elements + behaviour
  states/                loading/empty/error variants (<screen-id>.<state>.png + spec)
  dialogs/  sheets/
  components/            component board PNG + per-component notes
  assets/                generated illustrations/photos (with prompt log), icon list
  prompts/               every prompt used (<id>.md) for reproducibility
  reports/               gates.md, rubric.md, contact-sheet.png
```
Naming: lowercase-hyphen ids, stable (`onb-02`, `home-01`, `home-01.empty`).

## tokens.json
```json
{
  "color": {
    "light": {"bg":"#FFFFFF","surface":"#F6F7F9","primary":"#2F5BFF","on-primary":"#FFFFFF","text":"#14181F","text-secondary":"#505A68","error":"#C8281E","on-error":"#FFFFFF"},
    "dark":  {"bg":"#0F1218","surface":"#181D26","primary":"#8AA4FF","on-primary":"#0B1020","text":"#F2F4F8","text-secondary":"#A9B2C0","error":"#FF8A80","on-error":"#2B0907"}
  },
  "pairs": [["text","bg"],["text","surface"],["text-secondary","bg"],["on-primary","primary"],["on-error","error"]],
  "icon_pairs": [["primary","bg"]],
  "type": {"display":32,"h1":24,"h2":20,"body":16,"secondary":14,"caption":12},
  "spacing": [4,8,12,16,24,32,48,64],
  "radius": {"sm":8,"md":12,"lg":16,"pill":999},
  "touch_target": 48
}
```
`pairs` = text pairs (4.5:1). `icon_pairs` = graphics (3:1). Both modes are checked.

## inventory.json
```json
{"app":"PDF Reader","items":[
  {"id":"splash-01","group":"entry","title":"Splash","states":["default"],"priority":"P0"},
  {"id":"home-01","group":"home","title":"Home","states":["default","loading","empty","error"],"priority":"P0"}
]}
```
Optional `"states_na": "<reason>"` exempts a data-group screen that genuinely has no loading/empty/error (e.g. a local-file reader); the reason is the audit trail. States listed here must exist as files (`states/home-01.empty.png` ...) for `state_coverage.py` to pass.

## <id>.spec.json
```json
{
  "id": "home-01", "title": "Home", "mode": "light", "size": [412, 892],
  "primary_actions": 1,
  "elements": [
    {"id":"fab-add","type":"button","interactive":true,"w":56,"h":56,"y":780,"font":0,"fg":"on-primary","bg":"primary"},
    {"id":"title","type":"text","interactive":false,"w":200,"h":32,"font":24,"fg":"text","bg":"bg"},
    {"id":"row-1","type":"row","interactive":true,"w":372,"h":64,"font":16,"fg":"text","bg":"surface"}
  ],
  "behaviour": {"fab-add":"opens sheet sheet-add","row-1":"opens detail-01"}
}
```
`fg`/`bg` are token names (preferred) or hex. `y` and `size` let the audit check the thumb zone. `interactive.w/h` are the **hit area**, not the glyph.
Keep specs honest: derive them from what you actually put in the prompt/HTML, and correct them after looking at the image.

## Web target additions
- `inventory.json`: top-level `"platform":"web"`, `"viewports":{"desktop":[1440,900],"mobile":[390,844]}`; each item `"views":["desktop","mobile"]` (and optional `"data":true` for list/dashboard pages). Image stems: `<id>@<view>`, states `<id>.<state>@<view>`.
- `<id>@<view>.spec.json`: same schema plus `"platform":"web"`, `"view":"desktop"`, `size` = viewport; hit areas in px, `font` in px. `tokens.json` may set `"platform":"web"` and `"touch_target":44`.
- Folders: `screens/{home,apps,requests,...}` by page group; long pages are one tall PNG per view.
