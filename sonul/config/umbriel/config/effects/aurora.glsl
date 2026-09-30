// Aurora: the focused window's ring becomes a slowly turning gradient through
// the theme palette, with a bright glint gliding around it and a soft halo
// fading out into the padding. Without a palette it uses built-in aurora hues.

const float TAU = 6.283185307179586;

vec3 fallback_hue(float t) {
    vec3 sky = vec3(0.478, 0.639, 1.000);
    vec3 lavender = vec3(0.702, 0.549, 1.000);
    vec3 rose = vec3(1.000, 0.541, 0.784);
    vec3 mint = vec3(0.369, 0.902, 0.816);
    float s = fract(t) * 4.0;
    float f = smoothstep(0.0, 1.0, fract(s));
    if (s < 1.0) return mix(sky, lavender, f);
    if (s < 2.0) return mix(lavender, rose, f);
    if (s < 3.0) return mix(rose, mint, f);
    return mix(mint, sky, f);
}

vec3 hue(float t) {
    vec3 c = umbriel_palette_count > 0 ? umbriel_palette_at(t).rgb : fallback_hue(t);
    // Material-style theme colors are pastel; lift saturation so the ring glows.
    float luma = dot(c, vec3(0.2126, 0.7152, 0.0722));
    return clamp(mix(vec3(luma), c, 1.35), 0.0, 1.0);
}

vec4 border(vec2 uv) {
    float d = max(umbriel_border_distance(uv), 0.0);
    float ring = umbriel_sample(uv).a;

    vec2 p = (uv - 0.5) * umbriel_size;
    float angle = atan(p.y, p.x);

    vec3 col = hue(angle / TAU + umbriel_time * 0.05);

    float glint = pow(0.5 + 0.5 * cos(angle - umbriel_time * 0.6), 40.0);
    col = mix(col, vec3(1.0), glint * 0.55);

    float halo = exp(-d / 7.0) * (0.22 + 0.25 * glint);
    float a = ring + halo * (1.0 - ring);
    return vec4(col * a, a);
}
