from django.shortcuts import render

def custom_404_view(request, exception):
    print("Custom 404 view called")
    _ = exception  # Suppress unused variable warning
    return render(request, '404.html', status=404)

