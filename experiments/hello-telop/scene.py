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


def make_emission_material(name: str):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    emission.inputs["Strength"].default_value = 2.0
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


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
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0

    bpy.ops.object.text_add(location=(0.0, 0.0, 0.0))
    text = bpy.context.object
    text.name = "HelloWorld"
    text.data.body = "Hello world!"
    text.data.align_x = "CENTER"
    text.data.align_y = "CENTER"
    text.data.size = 1.15
    text.data.extrude = 0.0
    text.data.bevel_depth = 0.0
    text.data.materials.append(make_emission_material("WhiteText"))

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
