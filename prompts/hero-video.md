# Hero video prompt

A cinematic prompt for image-to-video / text-to-video models (Seedance, Kling,
Runway Gen-3, Luma). The concept: a heavy suit of dark armor assembling itself
over a bare mechanical skeleton, with a glowing brain — the model — pulsing
inside the ribcage. This is the visual metaphor for HBA: the harness (skeleton),
the model (brain), and the tools (armor plates) closing around it.

---

## Master prompt (text-to-video)

```
Dark fantasy cinematic, heavy ink and cross-hatch shading rendered in motion.
A towering black suit of armor assembles itself in a ruined cathedral under a
lightning storm. First we see a bare metallic SKELETON / exo-harness standing
in the dark — a machine ribcage of steel struts and cables. Inside the ribcage,
a glowing BRAIN made of molten amber light and fine circuitry begins to pulse,
casting warm light through the bones.

Then the ARMOR closes over it: jagged obsidian plates, spiked pauldrons, heavy
chains and rivets slam into place around the skeleton one by one, each plate
locking with a spark. A helm lowers over the skull, its single eye igniting deep
crimson. Ash and embers drift upward, rain streaks across the frame, cold
lightning flickers behind. Camera slowly pushes in from a low heroic angle, then
orbits the fully-formed armored figure as it clenches its fist.

Color: near-black steel, bone grey, warm amber core glow, one crimson accent.
Mood: ominous, powerful, sacred-machine. Volumetric fog, film grain, high
contrast, dramatic rim light. Ultra-detailed, 4k, cinematic 24fps.
```

Negative prompt: `bright colors, cartoon, cute, low detail, blurry, watermark, text, extra limbs, deformed hands`

---

## What each element represents

| On screen | Meaning |
|-----------|---------|
| Skeletal harness / exo-ribcage | the infrastructure harness (k3s cluster, nodes) |
| Glowing brain inside the ribcage | the model — the intelligence |
| Plates locking on | the tools wrapping the agent (reach + defense) |
| Chains | the controls — capability without blast radius |
| Helm, crimson eye | the agent, online and active |
| Three silhouettes (optional wide shot) | the fleet: Azure, k3s, local |

---

## Shot list (for tools that support keyframes)

1. 0-2s — wide: bare steel skeleton harness in the dark, rain, distant lightning.
2. 2-4s — push in: amber brain ignites inside the ribcage, light through bones.
3. 4-7s — armor plates and chains slam into place, sparks on each lock.
4. 7-9s — helm lowers, crimson eye ignites, low-angle hero shot.
5. 9-10s — figure clenches fist, ash rises, cut to title card.

---

## Using your own pipeline (comfyui-h3-ondemand-gpu)

1. Generate the hero still first (SDXL) using the master prompt as a single-frame prompt.
2. Feed that still as `init_image` into the MiniMax H3 image-to-video workflow.
3. Motion prompt: "armor plates lock into place, amber brain pulses inside the
   ribcage, crimson eye ignites, embers rise, slow push-in."
4. 6-10s at 24fps, then append the title card on the tail.
