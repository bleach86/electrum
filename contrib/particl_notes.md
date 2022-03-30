# Particl Notes

## Coldstaking

To setup coldstaking the wallet must be initialised in legacy mode.

When using an extaddress as the coldstaking change address the wallet will
derive new addresses to use for each change output created.

To avoid reusing addresses when using an existing extaddress keychain as the coldstaking change address.
Run `extkey list true` on your partyman (staking) node.
Set the keys derived counter to the `num_derives_external` field from that output where the extaddress matches.
