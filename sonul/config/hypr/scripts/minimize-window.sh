#!/usr/bin/env bash

set -euo pipefail

readonly minimized_workspace="special:minimized"
readonly state_dir="${XDG_RUNTIME_DIR:-/tmp}/hypr-minimize-${UID}"
readonly state_file="${state_dir}/stack.json"
readonly lock_file="${state_dir}/lock"

mkdir -p "${state_dir}"
[[ -s "${state_file}" ]] || printf '[]\n' > "${state_file}"

exec 9>"${lock_file}"
flock 9

read_state() {
	if ! jq -e 'type == "array"' "${state_file}" >/dev/null 2>&1; then
		printf '[]\n' > "${state_file}"
	fi
	cat "${state_file}"
}

write_state() {
	local temporary_file
	temporary_file="$(mktemp "${state_dir}/stack.XXXXXX")"
	cat > "${temporary_file}"
	mv "${temporary_file}" "${state_file}"
}

minimize_window() {
	local active_window address workspace state

	active_window="$(hyprctl -j activewindow)"
	address="$(jq -r '.address // empty' <<< "${active_window}")"
	workspace="$(jq -r '.workspace.name // empty' <<< "${active_window}")"
	[[ -n "${address}" && -n "${workspace}" ]] || exit 0
	[[ "${workspace}" != "${minimized_workspace}" ]] || exit 0

	hyprctl --quiet dispatch \
		"hl.dsp.window.move({ workspace = \"${minimized_workspace}\", follow = false, window = \"address:${address}\" })"

	state="$(read_state)"
	jq --arg address "${address}" --arg workspace "${workspace}" \
		'map(select(.address != $address)) + [{address: $address, workspace: $workspace}]' \
		<<< "${state}" | write_state
}

restore_window() {
	local clients state valid_state entry address workspace target

	clients="$(hyprctl -j clients)"
	state="$(read_state)"
	valid_state="$(
		jq --argjson clients "${clients}" --arg minimized "${minimized_workspace}" '
			[
				.[] |
				.address as $address |
				select(any($clients[]; .address == $address and .workspace.name == $minimized))
			]
		' <<< "${state}"
	)"
	entry="$(jq -c 'last // empty' <<< "${valid_state}")"

	if [[ -z "${entry}" ]]; then
		printf '[]\n' | write_state
		exit 0
	fi

	address="$(jq -r '.address' <<< "${entry}")"
	workspace="$(jq -r '.workspace' <<< "${entry}")"
	if [[ "${workspace}" =~ ^[0-9]+$ ]]; then
		target="${workspace}"
	else
		target="name:${workspace}"
	fi

	hyprctl --quiet dispatch \
		"hl.dsp.window.move({ workspace = \"${target}\", follow = false, window = \"address:${address}\" })"
	hyprctl --quiet dispatch \
		"hl.dsp.focus({ window = \"address:${address}\" })"

	jq --arg address "${address}" \
		'map(select(.address != $address))' <<< "${valid_state}" | write_state
}

case "${1:-}" in
	minimize)
		minimize_window
		;;
	restore)
		restore_window
		;;
	*)
		printf 'Usage: %s {minimize|restore}\n' "$0" >&2
		exit 2
		;;
esac
