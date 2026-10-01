// A restrained squash-and-settle while a window resizes. Both endpoints are
// unchanged, with a smooth start and finish. Outside the squash this behaves
// like niri's built-in resize: crop the next texture when growing, crossfade
// otherwise.
vec4 resize_color(vec3 coords_curr_geo, vec3 size_curr_geo) {
    float p = niri_clamped_progress;
    float pulse = 16.0 * p * p * (1.0 - p) * (1.0 - p);
    vec2 scale = vec2(1.0 - 0.02 * pulse, 1.0 - 0.045 * pulse);
    vec3 coords = vec3((coords_curr_geo.xy - 0.5) / scale + 0.5, 1.0);

    bool crop = niri_curr_geo_to_next_geo[0][0] <= 1.0
        && niri_curr_geo_to_next_geo[1][1] <= 1.0;

    if (crop) {
        if (coords.x < 0.0 || 1.0 < coords.x || coords.y < 0.0 || 1.0 < coords.y)
            return vec4(0.0);
        vec3 coords_next_geo = niri_curr_geo_to_next_geo * coords;
        return texture2D(niri_tex_next, (niri_geo_to_tex_next * coords_next_geo).st);
    }

    vec4 next = texture2D(niri_tex_next, (niri_geo_to_tex_next * coords).st);
    vec4 prev = texture2D(niri_tex_prev, (niri_geo_to_tex_prev * coords).st);
    return mix(prev, next, p);
}
