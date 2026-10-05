# Second Look

Paste a suspicious message, get a scam verdict. (ForgeHacks AI + Cybersecurity)

TODO: setup and usage.

## Debug switch (dev only)
Set `SECOND_LOOK_DEBUG=1` to print the first 300 characters of a model reply that failed
to parse to the terminal (stderr). Off by default. Never enable it in a deployment:
replies can echo the user's message. Nothing is written to a file or log.
