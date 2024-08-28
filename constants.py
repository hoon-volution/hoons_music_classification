class Constants:
    SAMPLING_RATE = 16_000  # sampling rate
    DURATION_SEC = 10  # 데이터 당 길이

    CLIP_SEC_HEAD = 10  # 앞에 몇 초를 자를까?
    CLIP_SEC_TAIL = 10  # 뒤에 몇 초를 자를까?

    SEG_LENGTH = SAMPLING_RATE * DURATION_SEC

    NUM_SEGS_PER_SONG = 20  # 한 곡마다 몇 개의 데이터를 만들까?

    VAL_RATIO = 0.15  # 아티스트 당 validation set으로 쪼갤 곡의 비율
    TEST_RATIO = 0.15  # 아티스트 당 test set으로 쪼갤 곡의 비율
