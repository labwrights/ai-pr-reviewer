Skip the export when a ticket has no id

A ticket without an id breaks the weekly import, so the export now stops and returns 0 when it finds one.
