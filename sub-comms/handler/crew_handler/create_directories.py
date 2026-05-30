"""
Creates

```fish
mkdir ".subcom/crew/$(string replace -r -a '[^\d.]+' '' "$(date -Iminutes)")-$(random 1000
 9999)"
```

Adds `./.subcom/crew/<crew-id>/crew_pids.json` to store crew PIDs.

Writes crew-id inside the `.running` file.
"""