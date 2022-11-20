
# easytcp3 
yes, I am bored, so I created version 3 for the easytcp, the point of that package is to be able to write
tcp servers more easily

## create a server
```py
import asyncio
from easytcp.server import Server


app = Server("localhost", 27000)


@app.hook.client_connect
async def on_client_connect(user):
    await user.send("Hello there and welcom!")

@app.hook.message
async def on_message(user, message):
    print("someone:", message)


if __name__ == "__main__":
    asyncio.run(app.run())
```

## hook
in the create server example I used `client_connect` and `messages` hooks,
you can create custom hook and call them like so

```py
app = Server("localhost", 27000)


@app.hook.client_connect
async def on_client_connect(user):
    await app.hook.call("my_custom_hook", user=user)


@app.hook.my_custom_hook
async def custom_hook(user):
    print("custom_hook_called")
```


### builtin hooks
for now at the time of writing, I am still if I event want to use
hooks for some events
