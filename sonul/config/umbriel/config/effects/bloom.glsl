// Bloom: an opening window rises a little and grows into place out of a soft
// glow of the theme accent while it fades in; a closing window sinks back into
// that glow. Progress includes spring overshoot, so the settle stays springy.

vec4 animation(vec2 uv) {
    float v = umbriel_direction > 0.0 ? umbriel_progress : 1.0 - umbriel_progress;
    float vc = clamp(v, 0.0, 1.0);

    float scale = mix(0.92, 1.0, v);
    vec2 q = (uv - 0.5) / scale + 0.5;
    q.y -= 0.03 * (1.0 - v);
    vec4 c = umbriel_sample(q);

    vec3 accent = umbriel_palette_count > 0 ? umbriel_palette_at(0.0).rgb : vec3(0.478, 0.639, 1.000);
    vec3 light = mix(vec3(1.0), accent, 0.6);
    float glow = (1.0 - vc) * 0.45;
    c.rgb += (light * c.a - c.rgb) * glow;

    return c * smoothstep(0.0, 1.0, vc);
}
