// Glass: a faint sheen across the top of each window, strongest at the top
// left, and a thin rim of light along its upper and left edges, like light
// catching a pane of glass.

vec4 window(vec2 uv) {
    vec4 c = umbriel_sample(uv);
    vec2 px = uv * umbriel_size;

    float sheen_height = min(0.4 * umbriel_size.y, 260.0);
    float sheen = (1.0 - smoothstep(0.0, sheen_height, px.y)) * (1.0 - 0.6 * uv.x) * 0.06;

    float rim = (1.0 - smoothstep(0.0, 2.0, px.y)) * 0.12
              + (1.0 - smoothstep(0.0, 2.0, px.x)) * 0.05;

    float s = clamp(sheen + rim, 0.0, 1.0);
    // Screen-blend toward white; colors are premultiplied, so white is c.a.
    return vec4(c.rgb + (vec3(c.a) - c.rgb) * s, c.a);
}
