from django.shortcuts import redirect


def unauthenticated_user(view_func):
	def wrapper_func(request, *args , **kwargs ):
		if request.user.is_authenticated:
			if request.user.is_superuser:
				return redirect('owner:home')
			else:
				return redirect('menu:menu')
		else:
			return view_func(request, *args , **kwargs )

	return wrapper_func


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		
		if request.user.is_superuser:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('menu:menu')

		
	return wrapper_function


def chef(view_func):
	def wrapper_function(request, *args, **kwargs):
		
		if request.user.is_chef or request.user.is_superuser:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('menu:menu')

		
	return wrapper_function