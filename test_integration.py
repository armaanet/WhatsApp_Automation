from app import app

data = {
    'From': '+1234567890',
    'Body': 'Remind me to call Mom tomorrow at 6 PM'
}

with app.test_client() as client:
    response = client.post('/webhook', data=data)
    print("Response from server:")
    print(response.data.decode('utf-8'))
