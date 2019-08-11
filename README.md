# The IPv6 Board project
This is a project inspired by the amazing IPv6 Christmas Tree
Send an ICMPv6 Echo Request to 2001:6b0:1001:105/64 to write on the board
The host-bits are mapped from their hex-vaule to the ASCII-table.
So for example a ping to 2001:6b0:1001:105:4177:6573:6f6d:6521 will print "Awesome!" to the board

## Limits
* The board will not show the same message twice in a row, if a message is the same as the previous it will be ignored to discourage flood-ping.
* The board show the message for 1s then move it upwards when a new message is received.

## Requirements
You will need a Raspberry Pi with the [Display-O-Tron HAT](https://shop.pimoroni.com/products/display-o-tron-hat) and the [Display-O-Tron Python Library](https://github.com/pimoroni/displayotron)

