import asyncio
import json
import websockets

class LiveMarketStreamer:
    def __init__(self, symbol='btcusdt'):
        self.url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
        self.prev_price = None

    async def start_stream(self):
        async with websockets.connect(self.url) as websocket:
            print(f"--- Connected to Live {self.url.split('/')[-1]} Stream ---")
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                current_price = float(data['c'])
                
                if self.prev_price:
                    diff = current_price - self.prev_price
                    icon = "🟢 UP" if diff > 0 else "🔴 DOWN"
                    print(f"PRICE: ${current_price:,.2f} | {icon} ({diff:+.2f})")
                else:
                    print(f"INITIAL PRICE: ${current_price:,.2f}")
                
                self.prev_price = current_price

if __name__ == "__main__":
    streamer = LiveMarketStreamer()
    try:
        asyncio.run(streamer.start_stream())
    except KeyboardInterrupt:
        print("\nStream stopped by user.")