from django.shortcuts import render, redirect, get_object_or_404
from .models import Gasto, Salario
from .forms import GastoForm, SalarioForm
from django.db.models import Sum


def lista_gastos(request):
    salario_obj = Salario.objects.first()

    for gasto in Gasto.objects.all():
        categoria_limpa = (gasto.categoria or "").strip().title()

        if gasto.categoria != categoria_limpa:
            gasto.categoria = categoria_limpa
            gasto.save()

    form = GastoForm()
    salario_form = SalarioForm(instance=salario_obj)

    if request.method == 'POST':
        if 'salvar_salario' in request.POST:
            salario_form = SalarioForm(request.POST, instance=salario_obj)
            if salario_form.is_valid():
                salario_form.save()
                return redirect('lista_gastos')
        else:
            form = GastoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('lista_gastos')

    mes = request.GET.get('mes')

    if mes:
        gastos = Gasto.objects.filter(data__month=int(mes)).order_by('-data')
    else:
        gastos = Gasto.objects.all().order_by('-data')

    total_gastos = sum(gasto.valor for gasto in gastos)
    salario = salario_obj.valor if salario_obj else 0
    saldo = salario - total_gastos

    categorias = gastos.values('categoria').annotate(total=Sum('valor'))

    labels = [item['categoria'] for item in categorias]
    valores = [float(item['total']) for item in categorias]

    return render(request, 'gastos/lista.html', {
        'gastos': gastos,
        'form': form,
        'salario_form': salario_form,
        'salario': salario,
        'total_gastos': total_gastos,
        'saldo': saldo,
        'labels': labels,
        'valores': valores,
        'mes_selecionado': mes
    })


def excluir_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    gasto.delete()
    return redirect('lista_gastos')


def editar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)

    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm(instance=gasto)

    salario_obj = Salario.objects.first()
    salario_form = SalarioForm(instance=salario_obj)

    gastos = Gasto.objects.all().order_by('-data')

    total_gastos = sum(g.valor for g in gastos)
    salario = salario_obj.valor if salario_obj else 0
    saldo = salario - total_gastos

    categorias = gastos.values('categoria').annotate(total=Sum('valor'))

    labels = [item['categoria'] for item in categorias]
    valores = [float(item['total']) for item in categorias]

    return render(request, 'gastos/lista.html', {
        'gastos': gastos,
        'form': form,
        'salario_form': salario_form,
        'salario': salario,
        'total_gastos': total_gastos,
        'saldo': saldo,
        'labels': labels,
        'valores': valores,
        'mes_selecionado': None
    })

