async def websocket_view(socket):
    await socket.accept()
    await socket.send_text("hello")
    await socket.close()
