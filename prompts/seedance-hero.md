# Cinematic hero prompt — Hermes Berserk Armor

For image-to-video / text-to-video models: **Seedance, Kling, Runway Gen-3, Luma, or your own `comfyui-h3-ondemand-gpu` (MiniMax I2V)**.

The concept: the **Berserker Armor closing over a skeletal harness**, a **glowing brain (the model)** pulsing inside the ribcage, chains and plates locking into place. Dark fantasy, Berserk manga ink aesthetic.

---

## Master prompt (text-to-video)

```
Dark fantasy cinematic, Kentaro Miura Berserk manga aesthetic, heavy cross-hatch
ink shading rendered in motion. A towering black Berserker armor assembles itself
in a ruined cathedral under a lightning storm. First we see a bare metallic
SKELETON / exo-harness standing in the dark — a machine ribcage of steel struts
and cables. Inside the ribcage, a HUMAN BRAIN made of molten amber light and
circuitry begins to pulse and glow, casting warm light through the bones.

Then the ARMOR closes over it: jagged obsidian plates, spiked pauldrons, heavy
chains and rivets slam into place around the skeleton one by one, each plate
locking with a spark. The wolf-helm lowers over the skull, its single eye
igniting deep crimson red. Ash and embers drift upward, rain streaks across the
frame, cold lightning flickers behind. Camera slowly pushes in from a low heroic
angle, then orbits around the fully-formed armored figure as it clenches its fist.

Color: near-black steel, bone grey, warm amber core glow, one crimson accent.
Mood: ominous, powerful, sacred-machine. Volumetric fog, film grain, high
contrast, dramatic rim light. Ultra-detailed, 4k, cinematic 24fps.
```

**Negative prompt:** `bright colors, cartoon, cute, low detail, blurry, watermark, text, extra limbs, deformed hands`

---

## Symbolism to keep (why each element is there)

| On screen | Means |
|---|---|
| Skeletal harness / exo-ribcage | the **infra harness** (k3s cluster, nodes) |
| Glowing brain inside the ribcage | the **model** — the will/intelligence |
| Plates locking on | the **tools** wrapping the agent (attack + defense) |
| Chains | the **guardrails** — capability without blast radius |
| Wolf-helm, crimson eye | the awakened **Hermes Berserk** agent, online |
| Three silhouettes / three bodies (optional wide shot) | the **fleet**: Azure · k3s · Local |

---

## Shot list (if the tool supports keyframes / multi-shot)

1. **0–2s** — wide: bare steel skeleton harness in the dark, rain, distant lightning.
2. **2–4s** — push in: amber brain ignites inside the ribcage, light spills through bones.
3. **4–7s** — armor plates + chains slam into place around it, sparks on each lock.
4. **7–9s** — wolf-helm lowers, crimson eye ignites, camera low-angle hero shot.
5. **9–10s** — figure clenches fist; ash rises; hard cut to title **HERMES BERSERK ARMOR**.

---

## Using your own pipeline (`comfyui-h3-ondemand-gpu`)

1. Generate the **hero still** first (SDXL / your `berserk-1997-comfyui` LoRA) using the master prompt as a single-frame prompt.
2. Feed that still as `init_image` into the MiniMax H3 image-to-video workflow.
3. Motion prompt: *"armor plates lock into place, amber brain pulses inside the ribcage, crimson eye ignites, embers rise, slow push-in."*
4. 6–10s @ 24fps, then drop the title card (`assets/fleet-architecture.png` style) on the tail.
