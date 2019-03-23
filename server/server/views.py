from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def pay_mobile(request, skin):
	data = {'value': 3};
	return render(request, 'pay_mobile.html', data);
