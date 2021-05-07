from urllib import request

from django.shortcuts import render

from pypro.modulos import facade


def detalhe(requests, slug):
    modulo = facade.encontrar_modulo(slug)
    return render(request, 'modulos/modulo_detalhe.html', {'modulo': modulo})
