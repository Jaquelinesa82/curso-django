from django.shortcuts import render


def video(request, slug):
    videos = {
        'motivacao': {'titulo': 'Video Aperitivos: Motivação', 'youtube_id': 'alALqQFykNs'},
        'instalacao-windows': {'titulo': 'Instalação Windows', 'youtube_id': 'ScmQ4I5Qr5s'}
    }
    video = videos[slug]
    return render(request, 'aperitivos/video.html', context={'video': video})
