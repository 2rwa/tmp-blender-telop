# tmp-blender-telop

Temporary Blender telop / caption rendering test repository driven by GitHub Actions.

This repository reuses the rendering flow from `2rwa/tmp-blender` and is intended for rapid experiments with Blender text, lower thirds, captions, title cards, compositing, animation, fonts, layout, and related rendering behavior.

## Rendering flow

```text
experiments/<id>/
  experiment.json
  scene.py
  validate.py
        |
        v
GitHub Actions
  discover
  -> Blender runtime/cache
  -> render scene
  -> validate real output
  -> upload full artifact
  -> commit selected results/.blend/media
  -> rebuild Pages gallery
  -> deploy GitHub Pages
```

## Layout

```text
experiments/
  <experiment-id>/
tools/
  experiment.py
  build_pages.py
results/
docs/
output/              # ignored local/Actions work directory
.github/workflows/
  blender-experiment.yml
```

## Baseline experiment

`hello-telop` renders a 1280x720 lower-third style telop containing **Hello world!**, saves the Blender scene, renders a PNG, and validates that the expected bright telop region is actually present.

## GitHub Pages

https://2rwa.github.io/tmp-blender-telop/

## Storage policy

This is a temporary experiment repository, so repository growth is not treated as an optimization target.

- full outputs are retained as short-lived Actions artifacts
- selected `.blend` files are committed under `results/<experiment>/`
- media may also be committed when below the practical 95 MiB per-file guardrail
- GitHub's hard per-file limits remain the final safety boundary

Cleanup/history rewriting can be handled separately when this repository is retired.
