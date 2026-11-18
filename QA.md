# Browser edition QA

Date: 2026-11-09. Preparation only; not published.

## Actual execution

- macOS, Python 3.14.5, Node.js 26.0.0, Playwright 1.62.1, installed Chrome 156.0.8078.80.
- Used existing local dependencies and CHROMIUM_PATH. A clean npm install and Playwright-managed browser download were not exercised.
- Four Python tests passed: HTML escaping, optional fields/six palettes, invalid data, fresh output directory.
- Two Node test cases passed: scale validation and actual browser integration (PNG output, no PDF, no empty input, overwrite refusal, height limit, overflow refusal).
- Three introduction pages were generated from updated JSON and directly screenshotted in Chrome. No PDF was used.
- The render report records font readiness and empty overflow lists. Glyph coverage was separately visually checked.

## Visual review

All three final PNGs opened and read. Titles, paragraphs, diagram labels, source footers, page numbers and attribution are complete; no observed clipping, overlap or missing Chinese glyphs.

- Page 1: 2400 × 3838; spacing and browser-only delivery wording checked.
- Page 2: 2400 × 3824; source-checking and QA wording checked.
- Page 3: 2400 × 3764; HTML → browser PNG wording, noncommercial license and no-publication boundary checked.

The earlier browser page 1 was 2400 × 3578; this revision adds 260 physical pixels in total. The earlier PDF-rendered page was 2400 × 3922. This is a modest breathing-room adjustment, not pixel matching: renderer/font differences and updated wording also affect size.
Body text is intended to be opened at readable size, not read entirely in a feed thumbnail.

## Packaging and caveats

Old PDF sources and exports are preserved separately. This package contains no PDF renderer or PDF output, no WeasyPrint/PyMuPDF dependency, no dependency cache and no bundled fonts. Public attribution retained.

The approved PolyForm Noncommercial 1.0.0 / CC BY-NC 4.0 split is applied; official full texts and a file scope inventory are included. Check browser/font/source licenses before release. Only the above macOS/Chrome environment was actually exercised; other supported runtimes still need testing.

License revision: all six tests re-run and passed. Page 3 regenerated and visually checked after replacing the obsolete license-pending text. Pages 1 and 2 are byte-identical to the previously reviewed exports. License source texts are retained verbatim and SHA-256 recorded in LICENSES/SOURCES.json. No publication occurred.

## README and workflow media revision

Date: 2026-11-09. Prepared locally on macOS; no remote repository was created or changed.

- README reorganized around purpose, example images, a copyable first request, workflow, local commands, boundaries and licensing. The quick-start output now uses a fresh directory rather than the already bundled output/intro.
- Relative Markdown/HTML file links checked: none missing. The GitHub public repositories API returned doublesq97-ui/su-mit-index with MIT license; the local repository remote and LICENSE agree. Linked project licenses do not apply to su-zine.
- Workflow GIF and MP4 rendered with the user-specified local su-black-purple-gif workflow: 1280 × 720, 8 seconds, 18 fps, 144 frames; 5 stages, 7 nodes, 6 directed edges. GIF metadata independently confirms duration and frame count.
- Poster and extracted opening, convergence, late-stage, final-hold and loop-end frames visually reviewed. Labels, directed relationships, attribution and safe areas are readable without clipping. Small subtitles are intended for full-size viewing.
- Renderer is not bundled. Original graph labels/data and the rendered visual design have explicit scope entries in LICENSE-SCOPE.md.
- Code, templates and all three introduction images remain byte-identical to the license-reviewed source package. No additional runtime feature was introduced. The six-test result above applies to those unchanged files; README-specific link checks and media checks were performed for this revision.
- README was not published or tested on a live GitHub repository. A clean dependency installation was not exercised.

## Public release validation

2026-11-09: The public release updates README installation links and removes the obsolete unpublished status from the introduction example. All four Python tests and both Node tests passed again using the environment above. Page 3 was regenerated and visually checked at full readable resolution; all three pages have empty overflow lists. Original license texts and attribution remain unchanged. Public files were checked for personal filesystem paths, credentials and private account identifiers; none were found. Git author uses the GitHub no-reply address.

## Optional dark theme — 2026-11-18

- Baseline commit: a877f7f76adb64278d22716f31e28138bfc6724c. Original light CSS and default HTML remain byte-identical.
- Added root JSON `theme` and CLI `--theme`, default light. Invalid themes are rejected. New CSS overrides only colors.
- GitHub Actions run 44355883669 passed for implementation commit 665095cfd541e3fa087e6c2ef3baa9000e549842: six Python tests and three Node tests; existing browser safety guards remain covered.
- Browser regression includes flow/stack/tags/papers, six palette colors, optional panel rows and long Chinese paragraphs. Light/dark DOM geometry is exactly equal. Right-side card and row text is white in dark mode.
- Original neutral example: light/dark each 2400 × 3596; prior/default light PNG byte comparison passed. Both neutral update images: 2400 × 2898. All reports show no overflow and loaded fonts.
- Chromium 151.0.7922.34 / Playwright 1.62.1 on the Actions runner with Noto CJK fonts. Local execution was blocked by the task sandbox's socket restriction; the unmodified browser renderer was tested on Actions instead.
- Downloaded Actions artifacts and visually checked light, dark, and both update pages: CJK text, contrast, spacing and footer pass. Public PNGs are browser exports; no PDF intermediates or private renderer were added.
- Original license files and private material boundary preserved. Theme/example/test/workflow license scope recorded in LICENSE-SCOPE.md.

Verification: https://github.com/doublesq97-ui/su-zine/actions/runs/44355883669
