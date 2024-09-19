# encryption/views.py
from django.shortcuts import render
from django.core.signing import Signer

# Create an instance of Signer
signer = Signer()

def encrypted_hello_view(request):
    # Sign/encrypt the "Hello" message
    value = signer.sign('Hello')
    
    port = request.get_port()
    # Pass the signed value to the template
    return render(request, 'encrypted_hello.html', {'encrypted_value': value, 'port': port})
