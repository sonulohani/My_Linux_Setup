// Bloom: a closing window sinks back into a soft glow of the theme accent
// while it fades out.
vec4 close_color(vec3 coords_geo, vec3 size_geo) {
    float v = 1.0 - niri_progress;
    float vc = clamp(v, 0.0, 1.0);

    float scale = mix(0.92, 1.0, v);
    vec2 q = (coords_geo.xy - 0.5) / scale + 0.5;
    q.y -= 0.03 * (1.0 - v);
    vec4 c = texture2D(niri_tex, (niri_geo_to_tex * vec3(q, 1.0)).st);

    // Niri has no palette uniforms, so this is Noctalia's accent_primary (#aac7ff).
    vec3 accent = vec3(0.667, 0.780, 1.0);
    vec3 light = mix(vec3(1.0), accent, 0.6);
    float glow = (1.0 - vc) * 0.45;
    c.rgb += (light * c.a - c.rgb) * glow;

    return c * smoothstep(0.0, 1.0, vc);
}
