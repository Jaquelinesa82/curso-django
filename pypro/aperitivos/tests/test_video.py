import pytest
from django.urls import reverse
from pypro.aperitivos.models import Video
from pypro.django_assertions import assert_contains


@pytest.fixture
def Video(db):
    v = Video(slug='motivacao', titulo='Vídeo Aperitivos: Motivação', youtube_id='alALqQFykNs')
    v.save()
    return v

@pytest.fixture
def resp(client, video):
    return client.get(reverse('aperitivos:video', args=(video.slug,)))


@pytest.fixture
def resp_video_nao_encontrado(client, video):
    return client.get(reverse('aperitivos:video', args=(video.slug+'video_não_existente',)))


def test_status_code_video_não_encontrado(resp_video_nao_encontrado):
    assert resp_video_nao_encontrado.status_code == 404


def test_status_code(resp):
    assert resp.status_code == 200


def test_titulo_video(resp, video):
    assert_contains(resp, video.titulo)


def test_conteudo_video(resp, video):
    assert_contains(resp, '<iframe src="https://www.youtube.com/embed/{video.youtube_id}"')