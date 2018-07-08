from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import blog
from django.urls import reverse_lazy
from io import BytesIO
# from .lib import predict
from PIL import Image
import numpy as np
import base64

def Index(request):
    return render(request, 'index.html')

class List(ListView):
    model = blog
    paginate_by = 3

    def get_queryset(self):
        # 作成日順に並び替え
        return super().get_queryset().order_by('-created_at')

class Detail(DetailView):
    model = blog

class Create(CreateView):
    model = blog
    fields = ['content','created_at']
    success_url = reverse_lazy('list')

    # def get_success_url(self):
    #     return reverse_lazy('list')

class Update(UpdateView):
    model = blog
    fields = ['content', 'created_at']

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs["pk"]})


class Delete(DeleteView):
    model = blog
    success_url = reverse_lazy('list')

class Mnist(TemplateView):
    template_name = 'ramen_blog/paint.html'

    def post(self, request):
        base_64_string = request.POST['img-src'].replace(
            'data:image/png;base64,', '')
        file = BytesIO(base64.b64decode(base_64_string))

        # ファイルを、28*28にリサイズし、グレースケール(モノクロ画像)
        img = Image.open(file).resize((28, 28)).convert('L')

        # 学習時と同じ形に画像データを変換する
        img_array = np.asarray(img) / 255
        img_array = img_array.reshape(1, 784)

        # 推論した結果を、テンプレートへ渡して表示
        # context = {
        #     'result': predict(img_array),
        # }
        context = {
            'result': 'GitHub_sample',
        }
        return render(self.request, 'ramen_blog/result.html', context)
