# 나만의 음악 데이터셋을 활용한 classification model 만들기


## 프로젝트 개요
"내 폴더의 음악 파일들을 데이터화 해서 직접 분류 모델을 만들 수 있을까?"

가 궁금해서 시작하게 된 토이 프로젝트.

클라우드 어딘가에 쟁여놨었던 음악들을 받아 시작하기로 한다.

## 데이터
### 데이터 준비
음악 폴더에 아직 남아있던 파일들 중 몇 개를 골라 데이터로 활용하기로 했다.

총 10팀의 아티스트를 자의적 기준으로 선정하였고, 아티스트당 1~2개의 앨범을 골라 총 167개의 곡을 골랐다.

선정한 아티스트들과 앨범은 다음과 같다.

- Epik High: 힙합 대표로 선정.
- Fall Out Boy: 팝 펑크 대표로 선정.
- Madeon: EDM 대표로 선정. 보컬이 없는 곡들이 많고 밴드 위주의 타 팀과 달리 런치패드 위주의 사운드가 많아 분류에 용이할 것으로 예상했다.
- Mika: 특색있는 보컬과 곡 스타일 들이 분류에 용이할 것으로 예상하여 선정.
- Mr.Big: 옛날 하드락, LA 메탈 대표로 선정.
- Muse: '뮤즈 스타일' 대표로 선정.
- Rage Against the Machine: 랩 메탈 대표로 선정.
- Red Hot Chili Peppers: Funk 락 대표로 선정.
- Suede: 브릿팝 대표로 선정. 독보적인 보컬 스타일이 분류에 용이할 것으로 예상.
- 브로콜리 너마저: 한국 인디 락 대표로 선정.

파일들을 ```music_samples/<아티스트>/<앨범>/<곡>.mp3```과 같은 경로에 넣어 데이터를 준비했다.
```bash
    music_samples
      ├─Epik High
      │  └─Pieces, Pt. 1
      │          Be.mp3
      │          Breakdown.mp3
      │          ...
      │
      ├─Fall Out Boy
      │  └─Infinity on High
      │          Bang the Doldrums.mp3
      │          Don_t You Know Who I Think I Am-.mp3
      │          ...
      │          
      ├─Madeon
      │  ├─Adventure [Deluxe Edition] Disc 1
      │          ...


``` 
### 데이터 전처리 및 가공
구현에 앞서, 음악 트랙보다는 intro/outro/intermission등과 가깝거나 러닝타임이 지나치게 짧아 학습에 지장을 줄 것으로 예상될 곡들을 미리 제외하였다.

**예시 1**: 서울, 1:13 AM, (Epik High, Pieces, Pt 1.)   

[![excl1](http://img.youtube.com/vi/jYutv0frJLA/0.jpg)](https://youtu.be/jYutv0frJLA?t=0s)

**예시 2**: Intro, (Muse, Absolution)   
[![excl2](http://img.youtube.com/vi/85R5sZynsyM/0.jpg)](https://youtu.be/85R5sZynsyM?t=0s)

**예시 3**: Hidden Track, (브로콜리 너마저, 졸업)   
[![excl3](http://img.youtube.com/vi/seXUf-sodbA/0.jpg)](https://youtu.be/seXUf-sodbA?t=3071s)
 

남은 곡들로부터 3340개의 데이터를 추출하였다. 추출방식은 다음과 같다.

1. 곡의 맨 앞/뒤의 10초를 잘라낸다. (연주가 시작되거나 끝나는 등 무의미한 구간 제거)
2. 남은 부분에서 10초 길이의 segment 20개를 등간격으로 추출한다. (167곡*20개=3340)
3. Training/Validation/Test Split은 segment마다가 아니라, 곡 별로 진행한다. (아티스트 마다 20곡이 training)
4. 파일들을 wav 확장자로 저장한다.

준비된 파일들을 Huggingface에 업로드하여 데이터셋을 만들었다.
https://huggingface.co/datasets/Hoonvolution/hoons_music_data

# DistilHuBert 모델 불러와 파인튜닝하기
오디오 분류에 주로 쓰이는 Pretrained 모델 중 HuBert보다 빠르게 학습 되면서도 성능이 크게 떨어지지 않는다고 하는 DistilHuBert 모델을 사용해 파인튜닝하기로 했다.
https://huggingface.co/ntu-spml/distilhubert

나만의 데이터셋을 통해 파인튜닝을 하여, 곡을 듣고 어떤 아티스트의 것인지 예측하는 분류 모델을 학습시켰다.
https://huggingface.co/Hoonvolution/distilhubert-finetuned-hoons_music

# 결과
Training accuracy는 84.4%로 나쁘지 않은 편이지만, 테스트 데이터에 대해서는 77.08%라는 조금은 아쉬운 성능이 관찰되었다.


4번 노트북에서 몇몇 오답들을 직접 들어보니 분류가 어려울만 했던 것들도 있었지만, 여러모로 개선의 여지가 많은 것 같다.


생각해볼만한 개선점으로는 다음이 있겠다.

- Hyperparameter 튜닝을 적극적으로 해보기
  - 이는 Tensorboard나 WANDB같은 툴에 조금 더 익숙해지면 시도해보자.
- 학습이 더 잘 될수 있도록 데이터 선정하기
  - 누가 들어도 '이 아티스트의 노래 같다!'고 느낄만한 음원들을 데이터로 더 잘 골랐으면 좋지 않았을까 하는 아쉬움이 있다. 하지만 이를 위해서는 그 아티스트에 대한 애정이 꽤나 각별해야 할 것 같다 😅
  - 몇 데이터는 하필 아티스트의 특성이 잘 드러나지 않는 구간에서 잘려서 분류가 잘 되지 않은 점들도 있는 것 같은데, 구간의 길이가 길었다면 정확도가 올라가지 않았을까 생각이 든다. 
- 데이터 증강 등으로 학습 데이터 수 늘리기
  - Gaussian noise를 더하는 등 데이터를 조금 더 확보해서 학습을 시켰다면 성능이 좋아지지 않았을까 기대한다.

