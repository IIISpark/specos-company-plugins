# Frontend Design

For apps and operational tools:

- prioritize density, scanability, predictable navigation, and repeated-use ergonomics
- use real controls, states, empty/error/loading surfaces
- avoid decorative card nests and generic gradients
- keep text within containers across viewport sizes
- use familiar icons for tool actions
- match the domain tone; operational tools should feel calm, dense, and work-focused
- design for the repeated workflow before visual novelty
- preserve existing brand and design-system rules before introducing external references

For public sites:

- make the product/person/place visible in the first viewport
- use real or generated visual assets when inspection matters
- keep the next section hinted below the hero

Do not create a landing or marketing shell when the user asked for an app, game, internal tool, or workflow surface. Build the usable experience first.

Frontend acceptance needs browser evidence. Use `ispark-browser-qa` for layout, console/network, responsive, interaction, and screenshot verification before claiming visual work is done.
