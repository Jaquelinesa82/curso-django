from django.shortcuts import render


def video(request, slug):
    video = {'titulo': 'Video Aperitivos: Motivação', 'youtube_id': 'alALqQFykNs'}
    return render(request, 'aperitivos/video.html', context={'video': video})
