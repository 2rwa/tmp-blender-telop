# tmp-blender-telop

Temporary Blender telop / caption rendering test repository driven by GitHub Actions.

This repository reuses the rendering flow from `2rwa/tmp-blender` and is intended for rapid experiments with Blender text, captions, title cards, compositing, animation, fonts, layout, and related rendering behavior.

## Start simple

The baseline experiment is deliberately just:

> **Hello world!**

White text, black background, 1280x720. No lower third, no decoration, no animation.

Once that baseline render is confirmed, more elaborate telop experiments can be added independently under `experiments/<id>/`.

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

## GitHub Pages

https://2rwa.github.io/tmp-blender-telop/

## Storage policy

This is a temporary experiment repository, so repository growth is not treated as an optimization target. Selected .blend files and media may be committed directly when practical; full outputs are also retained as Actions artifacts.
