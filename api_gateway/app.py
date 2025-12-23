from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Core Services (Single Instance)
CORE_URL = 'http://localhost:5002'
SERVICES = {
    'auth': f'{CORE_URL}/auth',
    'admin': f'{CORE_URL}/admin',
    'hotel': f'{CORE_URL}/hotel',
}

# Transaction Services (Round Robin Load Balancing)
TRANS_NODES = [
    'http://localhost:5003', 
    'http://localhost:5004', 
    'http://localhost:5005'
]
# Pointer for Round Robin
trans_idx = 0

def get_next_trans_node():
    global trans_idx
    node = TRANS_NODES[trans_idx]
    # Update pointer: (0 -> 1 -> 2 -> 0 ...)
    trans_idx = (trans_idx + 1) % len(TRANS_NODES)
    return node

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    
    # 1. Determine Target URL
    if service in ['order', 'payment', 'notification']:
        # Apply Load Balancer Logic
        base_url = get_next_trans_node()
        url = f"{base_url}/{service}/{path}"
        print(f"LB: Routing '{service}' request to {base_url} (Index: {(trans_idx - 1) % len(TRANS_NODES)})")
        
    elif service in SERVICES:
        # Static Routing for Core
        url = f"{SERVICES[service]}/{path}"
        
    else:
        return jsonify({"error": "Service not found"}), 404
    
    # 2. Forward Request
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        
        # Add a custom header to show which server handled it (debug info)
        headers.append(('X-Handled-By', url))
        
        return resp.content, resp.status_code, headers
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == '__main__':
    print("Gateway running on port 5000 with Round Robin LB")
    app.run(port=5000, debug=True)
