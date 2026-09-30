// Dusk: a gentle vignette. The center and the bar stay untouched while the far
// corners fall off softly, about 18% darker at the very corner.

vec4 screen(vec2 uv) {
    vec4 c = umbriel_sample(uv);
    vec2 p = (uv - 0.5) * vec2(umbriel_size.x / umbriel_size.y, 1.0);
    float falloff = smoothstep(0.45, 1.05, length(p));
    return vec4(c.rgb * (1.0 - 0.18 * falloff), c.a);
}
