// Halo: a small soft glow around the pointer, the theme accent at the center
// shading into the palette's third hue at the rim. It doesn't read the clock,
// so it never forces extra frames.

vec4 cursor(vec2 uv) {
    vec4 c = umbriel_sample(uv);
    // The square is clipped at output edges, so measure in logical pixels.
    float radius = max(umbriel_size.x, umbriel_size.y) * 0.5;
    float d = length((uv - umbriel_pointer) * umbriel_size) / radius;

    vec3 inner = umbriel_palette_count > 0 ? umbriel_palette_at(0.0).rgb : vec3(0.478, 0.639, 1.000);
    vec3 outer = umbriel_palette_count > 0 ? umbriel_palette_at(0.5).rgb : vec3(0.702, 0.549, 1.000);
    vec3 tint = mix(inner, outer, smoothstep(0.0, 0.8, d));

    float a = exp(-d * d * 5.0) * 0.24;
    return vec4(c.rgb * (1.0 - a) + tint * a * c.a, c.a);
}
