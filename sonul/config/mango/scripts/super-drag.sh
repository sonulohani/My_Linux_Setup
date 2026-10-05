#!/bin/sh
# Super+drag that also works on maximized windows.
# mango refuses to move a maximized window, so restore it first, then start
# the interactive move while the mouse button is still held.

client=$(mmsg get focusing-client)
id=$(printf '%s' "$client" | jq '.id')

case "$client" in
*'"is_maximized":true'*)
	mmsg dispatch togglemaximizescreen client,"$id"

	case "$client" in
	*'"is_floating":true'*)
		# The restored floating geometry can be anywhere on screen; put the
		# window under the cursor so the drag grabs it near the top edge.
		width=$(mmsg get client "$id" | jq '.width')
		read -r cx cy <<EOF
$(mmsg get cursorpos | jq -r '"\(.x | floor) \(.y | floor)"')
EOF
		x=$((cx - width / 2))
		y=$((cy - 20))
		[ "$x" -lt 0 ] && x=0
		[ "$y" -lt 0 ] && y=0
		mmsg dispatch movewin,"$x","$y" client,"$id"
		;;
	esac
	;;
esac

mmsg dispatch moveresize,curmove
