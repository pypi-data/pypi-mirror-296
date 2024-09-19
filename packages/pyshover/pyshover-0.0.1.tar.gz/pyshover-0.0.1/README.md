# WIP

Forked to modernize the packaging. This is my favourite Pushover library, so I'm adopting it.

### Lineage

- <https://github.com/pix0r/pushover>
- <https://github.com/wyattjoh/pushover>
- This repo.

### Future plans
- Modernize where needed
- More quick-use features


# pushover

A simple Python3.3 client for <http://pushover.net/> API based off of <https://github.com/pix0r/pushover> by pix0r.

Install:

    pip install git+https://github.com/invisiblethreat/pyshover

Sample Python3 Usage:

```python
from pushover import Pushover

po = Pushover("My App Token")
po.user("My User Token")

msg = po.msg("Hello, World!")

msg.set("title", "Best title ever!!!")

po.send(msg)
```

Sample Shell Usage:

```bash
./pushover "Hello, World!" --token="My App Token" --user="My User Token"
```

## Python <small>v3</small>

Pushover Class:

class Pushover(builtins.object)
| Creates a Pushover handler.
|  
 | Usage:
|  
 | po = Pushover("My App Token")
| po.user("My User Token", "My User Device Name")
|  
 | msgid, msg = po.msg("Hello, World!")
|  
 | po.send(msgid)
|  
 | Methods defined here:
|  
 | **init**(self, token=None)
| Creates a Pushover object.
|  
 | msg(self, message)
| Creates a PushoverMessage object. Takes one "message" parameter (the message to be sent).
| Returns with message id (mid) and PushoverMessage object (msg).
|  
 | send(self, mid)
| Sends a specified message with id "mid".
|  
 | sendall(self)
| Sends all PushoverMessage's owned by the Pushover object.
|  
 | user(self, user_token, user_device=None)
| Sets a single user to be the recipient of all messages created with this Pushover object.

PushoverMessage Class:

     class PushoverMessage(builtins.object)
     |  Used for storing message specific data.
     |
     |  Methods defined here:
     |
     |  __init__(self, message)
     |      Creates a PushoverMessage object.
     |
     |  __str__(self)
     |
     |  get(self)
     |      Returns a dictionary with the values for the specified message.
     |
     |  set(self, key, value)
     |      Sets the value of a field "key" to the value of "value".
     |
     |  user(self, user_token, user_device=None)
     |      Sets a single user to be the recipient of this message with token "user_token" and device "user_device".

## Shell

    Usage:    pushover <message> --token=<TOKEN> --user=<USER> [options]

Options:
-h, --help show this help message and exit
--token=<TOKEN> Pushover app token (overrides environment
PUSHOVER_TOKEN)
--user=<USER> Pushover user key

Optional:
--device DEVICE Pushover device name
--title TITLE Message title
--timestamp TIMESTAMP Optional UNIX timestamp
--priority PRIORITY Optional priority setting (0=normal, 1=high)
