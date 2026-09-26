from __future__ import annotations

from pathlib import Path

import bpy


ROOT = Path.cwd()
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RENDER_PATH = OUTPUT_DIR / "render.png"
BLEND_PATH = OUTPUT_DIR / "scene.blend"


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def material(name: str, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.55
    return mat


def add_rect(name: str, location, scale, mat) -> None:
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)


def add_text(name: str, body: str, location, size: float, mat) -> None:
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.body = body
    obj.data.align_x = "LEFT"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.012
    obj.data.bevel_depth = 0.004
    obj.data.materials.append(mat)


def build_scene() -> None:
    clear_scene()
    scene = bpy.context.scene

    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = str(RENDER_PATH)
    scene.render.film_transparent = False

    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.006, 0.010, 0.020, 1.0)
    bg.inputs["Strength"].default_value = 0.3

    dark = material("Background", (0.012, 0.020, 0.042))
    panel = material("Panel", (0.030, 0.055, 0.095))
    accent = material("Accent", (0.05, 0.55, 1.0))
    white = material("TextWhite", (0.96, 0.98, 1.0))
    muted = material("TextMuted", (0.48, 0.68, 0.86))

    add_rect("Backdrop", (0.0, 0.0, 0.0), (6.4, 3.6, 0.05), dark)
    add_rect("LowerThird", (0.0, -2.25, 0.12), (5.65, 0.78, 0.05), panel)
    add_rect("Accent", (-5.48, -2.25, 0.20), (0.07, 0.78, 0.025), accent)

    add_text("Headline", "Hello world!", (-5.15, -2.08, 0.22), 0.58, white)
    add_text("Subline", "tmp-blender-telop / baseline render", (-5.12, -2.68, 0.22), 0.24, muted)

    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 10.0)
    camera.rotation_euler = (0.0, 0.0, 0.0)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 7.2
    scene.camera = camera

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)

    print(f"BLEND_PATH={BLEND_PATH}")
    print(f"RENDER_PATH={RENDER_PATH}")


if __name__ == "__main__":
    build_scene()
