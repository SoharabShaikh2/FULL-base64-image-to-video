import base64

import imageio
import moviepy.video.fx.all as vfx
import json

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.io.AudioFileClip import AudioFileClip

from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


# for i in data["wbw"]:
# print(i)

# print(jsonData)


def convertAyatToVideo(jsonData, name, surah, ayat):
    i = 0
    mainVideo = []
    setMusicStart = 0

    clip = VideoFileClip("back.mp4", audio=False)
    mainAudio = AudioFileClip("back_mp3.mp3")

    clip_resized = clip.fx(vfx.resize, width=1080, height=1920)

    audio1 = AudioFileClip(jsonData["mp3"])
    audioTem1 = audio1.set_start(setMusicStart)
    audioMain1 = audioTem1.fx(vfx.speedx, 0.95)

    setMusicStart2 = setMusicStart + audioMain1.duration + 1
    audio2 = AudioFileClip(jsonData["english_mp3"])
    audioTem2 = audio2.set_start(setMusicStart2)
    audioMain2 = audioTem2

    setMusicStart3 = setMusicStart2 + audioMain2.duration + 1
    audio3 = AudioFileClip(jsonData["bengali_mp3"])
    audioTem3 = audio3.set_start(setMusicStart3)
    audioMain3 = audioTem3

    videoDuration = audioMain1.duration + 1 + audioMain2.duration + 1 + audioMain3.duration + 1

    clip1 = vfx.loop(clip_resized, duration=videoDuration)
    mainAudio1 = vfx.loop(mainAudio, duration=videoDuration)
    mainAudio1 = mainAudio1.fx(volumex, 0.4)

    clipArray = []
    audioArry = []
    clipArray.append(clip1)
    audioArry.append(mainAudio1)
    audioArry.append(audioMain1)
    audioArry.append(audioMain2)
    audioArry.append(audioMain3)

    mask_Clip = TextClip('Surah: ' + surah + ', Ayat: ' + str(ayat), fontsize=30, color='white')
    mask_Clip = mask_Clip.set_duration(videoDuration - 1).set_start(setMusicStart)
    mask_Clip = mask_Clip.set_position((0.07, 0.95), relative=True).set_opacity(0.6)
    # mask_Clip = mask_Clip.fx(vfx.margin, bottom=10, opacity=0)
    clipArray.append(mask_Clip)

    imgdata1 = base64.b64decode(jsonData["arabic_img"])
    img1 = imageio.imread(imgdata1)

    txt_clip = ImageClip(img1).set_position("center").set_duration(audioMain1.duration + 1).set_start(
        setMusicStart)
    txt_clip = vfx.fadein(txt_clip, 1)
    txt_clip = vfx.fadeout(txt_clip, 0.5)
    clipArray.append(txt_clip)

    imgdata2 = base64.b64decode(jsonData["english_img"])
    img2 = imageio.imread(imgdata2)

    txt_clip2 = ImageClip(img2).set_position("center").set_duration(audioMain2.duration + 1).set_start(
        setMusicStart2)
    txt_clip2 = vfx.fadein(txt_clip2, 1)
    txt_clip2 = vfx.fadeout(txt_clip2, 0.5)
    clipArray.append(txt_clip2)

    imgdata3 = base64.b64decode(jsonData["bengali_img"])
    img3 = imageio.imread(imgdata3)

    txt_clip3 = ImageClip(img3).set_position("center").set_duration(audioMain3.duration + 1).set_start(
        setMusicStart3)
    txt_clip3 = vfx.fadein(txt_clip3, 1)
    txt_clip3 = vfx.fadeout(txt_clip3, 0.5)
    clipArray.append(txt_clip3)

    audioMixed = CompositeAudioClip(audioArry)
    # Overlay the text clip on the first video clip
    video = CompositeVideoClip(clipArray)
    video = video.set_audio(audioMixed)
    mainVideo.append(video)

    mainVideoFile = CompositeVideoClip(mainVideo)
    mainVideoFile.write_videofile(name+"_"+str(ayat) + ".mp4")


'''
    if 120 < duration < 180:
        clip1 = clip.subclip(0, round(duration / 3))
        clip1.write_videofile(surah + "-part1.mp4")
        clip2 = clip.subclip(round(duration / 3) - 1, (round(duration / 3) * 2))
        clip2.write_videofile(surah + "-part2.mp4")
        clip3 = clip.subclip((round(duration / 3) * 2) - 1, round(duration) - .20)
        clip3.write_videofile(surah + "-part3.mp4")

    elif 60 < duration < 120:
        clip1 = clip.subclip(0, round(duration / 2))
        clip1.write_videofile(surah + "-part1.mp4")
        clip2 = clip.subclip(round(duration / 2) - 1, round(duration) - .20)
        clip2.write_videofile(surah + "-part2.mp4")
'''


# showing video


def makeVideo():
    surah = 1

    i = 0
    while i < 7:
        startFrom = 1 + i
        f = open("00" + str(surah) + "_00" + str(i)+".json", encoding="utf-8")
        data = json.load(f)
        #print(data)
        f.close()
        jsonData = data

        convertAyatToVideo(jsonData, '00' + str(surah), str(surah), startFrom)
        i += 1

    '''i = 0
    while i < len(jsonData):
        print(jsonData[i]["mp3"])
        name = '00' + str(surah) + '_00' + str(surah) + '00' + str(i + startFrom)

        i += 1'''


'''def loopFile():
    surah = 2
    i = 3
    while i < 1:
        url = '00' + str(surah) + '/' + 'Surah_00' + str(surah) + '00' + str(i) + '.json'
        name = '00' + str(surah) + '_00' + str(surah) + '00' + str(i) + '.mp4'
        makeVideo()
        i += 1'''

makeVideo()
