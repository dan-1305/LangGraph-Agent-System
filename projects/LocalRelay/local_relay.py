import uuid
import asyncio
from fastapi import FastAPI, WebSocket, Request, status
from fastapi.responses import StreamingResponse
from typing import Dict

app = FastAPI(title="Local Gemini WS Relay")

# Lưu trữ các kết nối từ con app AI Studio (Browser)
# Key: code (ví dụ: danh01), Value: WebSocket connection
proxy_connections: Dict[str, WebSocket] = {}

# Lưu trữ các request đang chờ phản hồi từ Browser
# Key: bridge_id, Value: asyncio.Queue
pending_requests: Dict[str, asyncio.Queue] = {}

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket, code: str = "danh01", role: str = "proxy"):
    """Endpoint dành cho con App AI Studio trên trình duyệt kết nối vào"""
    await websocket.accept()
    if role == "proxy":
        proxy_connections[code] = websocket
        print(f"🔌 AI Studio App ({code}) đã kết nối thành công qua WebSocket Local!")
        
        try:
            while True:
                # Lắng nghe dữ liệu/phản hồi trả về từ Browser
                data = await websocket.receive_json()
                bridge_id = data.get("bridge_id")
                
                # Đẩy data vào Queue của HTTP request tương ứng đang đợi
                if bridge_id in pending_requests:
                    await pending_requests[bridge_id].put(data)
                    
        except Exception as e:
            print(f"❌ Mất kết nối với AI Studio App: {e}")
        finally:
            if code in proxy_connections:
                del proxy_connections[code]

@app.post("/v1beta/models/{model_name}:{action}")
async def handle_cline_request(model_name: str, action: str, request: Request, code: str = "danh01"):
    """Endpoint hứng request HTTP từ Cline gửi qua"""
    if code not in proxy_connections:
        return {"error": "AI Studio App chưa kết nối hoặc offline!"}, status.HTTP_503_SERVICE_UNAVAILABLE

    payload = await request.json()
    bridge_id = f"bridge-{int(asyncio.get_event_loop().time()*1000)}-{uuid.uuid4().hex[:6]}"
    print(f"📥 Nhận request {bridge_id} cho model {model_name}")

    # Tạo Queue để hứng dữ liệu trả về cho request này
    response_queue = asyncio.Queue()
    pending_requests[bridge_id] = response_queue

    # Gửi lệnh qua WebSocket bắt con App AI Studio dưới trình duyệt fetch Gemini
    await proxy_connections[code].send_json({
        "bridge_id": bridge_id,
        "action": action,
        "model": model_name,
        "payload": payload
    })

    # Thu thập dữ liệu stream trả về cho Cline
    async def stream_generator():
        try:
            while True:
                # Đợi dữ liệu từ WebSocket đẩy vào Queue
                chunk = await response_queue.get()
                if chunk.get("type") == "done":
                    break
                yield chunk.get("data", "")
        finally:
            if bridge_id in pending_requests:
                del pending_requests[bridge_id]

    # Trả về dạng Stream đúng chuẩn format của Cline yêu cầu
    return StreamingResponse(stream_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=11451)