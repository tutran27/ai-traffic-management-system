"""WebSocket connection manager for real-time data broadcast."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections and broadcasts data to all clients."""

    def __init__(self):
        self._connections: list[WebSocket] = []

    @property
    def active_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def broadcast_json(self, data: dict[str, Any]) -> None:
        """Broadcast JSON data to all connected clients asynchronously.

        Protects the simulation loop from slow clients by setting a strict
        timeout on send operations. If a client stalls, it is dropped so
        it never causes backpressure that blocks the simulation tick loop.
        """
        if not self._connections:
            return

        message = json.dumps(data)
        stalled: list[WebSocket] = []

        async def _safe_send(ws: WebSocket) -> None:
            try:
                # 150ms timeout ensures backpressure cannot stall the 10Hz simulation loop
                await asyncio.wait_for(ws.send_text(message), timeout=0.15)
            except Exception:
                stalled.append(ws)

        await asyncio.gather(*[_safe_send(ws) for ws in list(self._connections)], return_exceptions=True)

        for ws in stalled:
            self.disconnect(ws)
            try:
                await ws.close()
            except Exception:
                pass


# Singleton instance
ws_manager = ConnectionManager()
