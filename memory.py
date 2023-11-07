# 딥러닝을 이용해 저화질 이미지를 고화질로

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Input, MaxPooling2D, UpSampling2D, add
from tensorflow.keras import regularizers
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

# 모델만들기

input_image = Input(shape=(128, 128, 3))

#인코더
l1 = Conv2D(64, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(input_image)
l2 = Conv2D(64, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l1)
l3 = MaxPooling2D(padding='same')(l2)
l4 = Conv2D(128, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l3)
l5 = Conv2D(128, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l4)
l6 = MaxPooling2D(padding='same')(l5)
l7 = Conv2D(256, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l6)

#디코더
l8 = UpSampling2D()(l7)
l9 = Conv2D(128, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l8)
l10 = Conv2D(128, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l9)

#잔차 연결 레이어
l11 = add([l5, l10])

l12 = UpSampling2D()(l11)
l13 = Conv2D(64, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l12)
l14 = Conv2D(64, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l13)

#잔차 연결 레이어
l15 = add([l14, l2])

decoded = Conv2D(3, 3, padding='same', activation='relu',kernel_initializer='he_normal',
            activity_regularizer=regularizers.l1(10e-10))(l15)

autoencoder = Model(input_image, decoded)
autoencoder.summary()

autoencoder.load_weights('/content/drive/MyDrive/gan/weight.hdf5')
loaded_model = autoencoder


# 데이터셋 경로
images_path = "your DataSet root"

# 전처리 함수
def preprocess_high_image(path):
    image = cv2.imread(path)
    # 크기 변경
    image = cv2.resize(image, (128, 128))
    # 정규화
    image = image.astype(np.float32) / 255.0
    return image

def preprocess_low_image(path):
    image = cv2.imread(path)
    # 크기 변경
    image = cv2.resize(image, (32, 32))
    image = cv2.resize(image, (128, 128))
    # 정규화
    image = image.astype(np.float32) / 255.0
    return image


# 파일경로 저장할 빈 리스트
image_path_list=[]

for filename in os.listdir(images_path):
    if filename.endswith('.jpg'):
        image_path = os.path.join(images_path, filename)
        image_path_list.append(image_path)
# 데이터 순서 맞추기 위해 정렬
image_path_list=sorted(image_path_list)



# train, test 나누기
train_images, test_images, _ , _ = train_test_split(image_path_list, image_path_list, train_size=0.8, random_state=42)


# train_dataset 생성
train_X_dataset = []
train_y_dataset = []

for image_path in train_images:
    # 파일 읽기
    image = cv2.imread(image_path)
    # 함수로 전처리
    low=preprocess_low_image(image_path)
    high=preprocess_high_image(image_path)
    # 리스트에 추가
    train_X_dataset.append(low)
    train_y_dataset.append(high)



# test_dataset 생성
test_X_dataset = []
test_y_dataset = []

for image_path in test_images:
    # 파일 읽기
    image = cv2.imread(image_path)
    # 함수로 전처리
    low=preprocess_low_image(image_path)
    high=preprocess_high_image(image_path)
    # 리스트에 추가
    test_X_dataset.append(low)
    test_y_dataset.append(high)



# 모델 컴파일
autoencoder.compile(optimizer='adam',
                    loss='mse',
                    metrics=['accuracy'])

# 콜백 설정
check_path_ = "upscaling_image.ckpt"
mcCB = ModelCheckpoint(check_path_,
                       save_best_only=True,
                       save_weights_only=True,
                       monitor='val_loss',
                       verbose=1)

esCB = EarlyStopping(monitor='val_loss',
                              patience=5,
                              verbose=1,
                              restore_best_weights=True)

train_X_dataset=np.array(train_X_dataset)
train_y_dataset=np.array(train_y_dataset)
test_X_dataset=np.array(test_X_dataset)
test_y_dataset=np.array(test_y_dataset)

# 모델 학습
batch_size = 128
hist = autoencoder.fit(train_X_dataset, train_y_dataset,
                       epochs=150,
                       validation_data=(test_X_dataset, test_y_dataset),
                       callbacks=[mcCB, esCB])

autoencoder.load_weights(check_path_)

autoencoder.save('model.h5')

# 모델 평가
losses = autoencoder.evaluate(test_X_dataset, test_y_dataset)
print("Losses:", losses)

autoencoder.save('model.h5')

#------------------------------------------------------------------------------------------------
model=load_model(r"D:\model.h5")

# 테스트 이미지 파일 경로
test_image_path = 'Your Test img file root'


# 이미지 로드 및 200% 확대
pred_img=cv2.imread(test_image_path)

dsize_=128,128
pred_img=cv2.resize(pred_img, dsize_)
pred_img_width, pred_img_height=dsize_
size_=int(pred_img_width * 2), int(pred_img_height * 2)
zoomed_image = cv2.resize(pred_img, size_, interpolation=cv2.INTER_CUBIC)


# 윈도우 크기 및 스텝 크기 설정
window_size = 128
step_size = 64

# 빈이미지생성
# 이미지 크기
blank_width=int(pred_img_width * 2)
blank_height=int(pred_img_height * 2)
# 흰색으로 채운 빈 이미지
blank_image=np.ones((blank_height, blank_width, 3), dtype=np.uint8) * 255  


# 윈도우를 옮기면서 학습시키기
for y in range(0, pred_img_height* 2 - window_size + 1, step_size):
    for x in range(0, pred_img_width* 2 - window_size + 1, step_size):
        result_array = zoomed_image[y:y+window_size, x:x+window_size]

        # 이미지 전처리
        result_array = result_array / 255.0

        # 모델 예측
        pred_result_array = model.predict(np.array([result_array]))[0]
        # 범위제한하기
        pred_result_array *=255

        min_val = 0
        max_val = 255
        clipped_array = np.where(pred_result_array < min_val, min_val, np.where(pred_result_array > max_val, max_val, pred_result_array))
        clipped_array = clipped_array.astype(np.ubyte)
        #print(clipped_array.shape)

        #pred_window = cv2.cvtColor(clipped_array, cv2.COLOR_GRAY2BGR)

        # # 이미지합치기
        blank_image[y:y+window_size, x:x+window_size] = pred_result_array

cv2.imwrite("re_magic.jpg",blank_image)
