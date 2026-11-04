# KiPiZK Backend API

Flask API untuk background removal menggunakan rembg (U2-Net model).

## Endpoints

### GET /
Health check endpoint.

### POST /api/remove-bg
Remove background dari gambar.

**Request Body:**
```json
{
  "image": "data:image/png;base64,..."
}
```

**Response:**
```json
{
  "success": true,
  "image": "data:image/png;base64,..."
}
```

## Deploy to Railway

1. Push code ke GitHub repository baru
2. Login ke https://railway.app
3. New Project → Deploy from GitHub
4. Select repository: kipizk-backend
5. Add variables (optional): 
   - `PORT=8080`
6. Deploy

Railway akan auto-detect Python dan install dependencies.

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

API akan jalan di `http://localhost:8080`

## Test

```bash
curl -X POST http://localhost:8080/api/remove-bg \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,..."}'
```
