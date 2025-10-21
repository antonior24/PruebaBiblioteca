from django.shortcuts import render
from biblioteca.models import Libro
from django.db.models import Q
from django.views.defaults import page_not_found

# Create your views here.
def index(request):
    return render(request, 'libro/index.html')

def listar_libros(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.all()
    libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
    + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "
    + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "))

    return render(request, 'libro/lista.html', {"libros_mostrar": libros})

def dame_libro(request, id_libro):
    libro = Libro.objects.select_related("biblioteca").prefetch_related("autores").get(id=id_libro)

    libro = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
    + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "
    + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
    + " WHERE l.id = %s", [id_libro])[0])

    return render(request, 'libro/libro.html', {"libro_mostrar": libro})

def dame_libros_fecha(request, anyo_libro, mes_libro):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.all()
    libros = libros.filter(fecha_publicacion__year=anyo_libro, fecha_publicacion__month=mes_libro)
    libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
    + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
    + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "
    + " WHERE strftime('%%Y', l.fecha_publicacion) = %s "
    + " AND strftime('%%m', l.fecha_publicacion) = %s ",
    [str(anyo_libro), str(mes_libro)]))

    
    return render(request, 'libro/lista.html', {"libros_mostrar": libros})

def dame_libros_idioma(request, idioma):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(Q(idioma=idioma) | Q(idioma="ES")).order_by("fecha_publicacion")
    libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
    + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "
    + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
    + " WHERE idioma = 'ES' "
    + " OR idioma = %s "
    + " ORDER BY l.fecha_publicacion",
    [idioma]))

    return render(request, 'libro/lista.html', {"libros_mostrar": libros})

def error_404_view(request, exception=None):
    return render(request, 'errores/404.html' , None, None , 404)


