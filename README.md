# GTU Satellite Image Segmantation Service


### Mermory Kullanımının Tespiti

 İlgili script için kullanım datasını oluşturulması için

``
mprof run --include-children python kmeans_seg.py
``

İlgili kullanım datasından profil oluşturmak için

``
mprof plot --output memory-profile.png
``