#5.2 小さなデータセットでCNNを学習する

#===========================================================================================

#dog vs catデータセット
#4000データ(2000枚で訓練、検証に1000枚、1000枚でテスト)
#このデータセットはkerasではパッケージ化されていない
#KaggleのWebページからダウンロード

#os:ディレクトリ操作、shutil:ファイルのコピーや削除
import os,shutil

#元のデータセットがある場所(ダウンロードファイル)へのパス
original_data_dir='/Users/nakatanitota/Downloads/kaggle_original_data'

#より小さなデータセットを格納するディレクトリへのパス
base_dir='/Users/nakatanitota/Downloads/cats_and_dogs_small'
#os.mkdir
#作成したpath(base_dirの場所に最後のディレクトリ名のファイルを作成)
os.mkdir(base_dir)

#訓練データセット、検証データセット、テストデータセットを配置するディレクトリ 
train_dir=os.path.join(base_dir,'train')
os.mkdir(train_dir)
validation_dir=os.path.join(base_dir,'validation')
os.mkdir(validation_dir)
test_dir=os.path.join(base_dir,'test')
os.mkdir(test_dir)

#訓練用の'cat'の画像を保存するディレクトリ 
train_cats_dir=os.path.join(train_dir,'cats')
os.mkdir(train_cats_dir)
#訓練用の'dog'の画像を保存するディレクトリ 
train_dogs_dir=os.path.join(train_dir,'dogs')
os.mkdir(train_dogs_dir)

#検証用の'cat'の画像を保存するディレクトリ 
validation_cats_dir=os.path.join(validation_dir,'cats')
os.mkdir(validation_cats_dir)
#検証用の'dog'の画像を保存するディレクトリ 
validation_dogs_dir=os.path.join(validation_dir,'dogs')
os.mkdir(validation_dogs_dir)

#テスト用にも同様のディレクトリ
test_cats_dir=os.path.join(test_dir,'cats')
os.mkdir(test_cats_dir)
test_dogs_dir=os.path.join(test_dir,'dogs')
os.mkdir(test_dogs_dir)


#catのデータの一部を移す!
#最初の1000個のcat画像をtrain_cats_dirにコピー
#format関数 : 任意の文字列{}任意の文字列'.format(変数)
#framesはリスト型の配列
frames=['cat.{}.jpg'.format(i) for i in range(1000)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(train_cats_dir,fname)
    shutil.copyfile(src,dst)

#次の500個のcat画像をvalidation_cats_dirにコピー
frames=['cat.{}.jpg'.format(i) for i in range(1000,1500)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(validation_cats_dir,fname)
    shutil.copyfile(src,dst)

#次の500個のcat画像をtest_cats_validationにコピー
frames=['cat.{}.jpg'.format(i) for i in range(1500,2000)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(test_cats_dir,fname)
    shutil.copyfile(src,dst)

#dogのデータの一部を移す!
#最初の1000個のdog画像をtrain_dog_dirにコピー
frames=['dog.{}.jpg'.format(i) for i in range(1000)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(train_dogs_dir,fname)
    shutil.copyfile(src,dst)

#次の500個のdog画像をvalidation_dogs_dirにコピー
frames=['dog.{}.jpg'.format(i) for i in range(1000,1500)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(validation_dogs_dir,fname)
    shutil.copyfile(src,dst)

#次の500個のdog画像をtest_dogs_validationにコピー
frames=['dog.{}.jpg'.format(i) for i in range(1500,2000)]
for fname in frames:
    src=os.path.join(original_data_dir,fname)
    dst=os.path.join(test_dogs_dir,fname)
    shutil.copyfile(src,dst)

#dog vs cat の割合は1:1であるため完全な２値分類

#ネットワークの構築
from keras import layers
from keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.summary()

#モデルのコンパイル
from keras import optimizers
model.compile(loss='binary_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4),metrics=['acc'])

#データの前処理
#現時点ではデータはJPGファイルとしてハードに記録されている
#1.画像ファイルを読み込む
#2.JPGファイルの内容をRGBのピクセルグリッドにデコードする
#3.浮動小数点型のテンソルに変更する
#4.(0,1)の範囲にスケール化する
#ImageDataGenerator:画像の前処理を行うkerasのパッケージ

from keras.preprocessing.image import ImageDataGenerator

#すべての画像を1/255でスケール
#インスタンスを生成
train_datagen=ImageDataGenerator(rescale=1./255)
test_datagen=ImageDataGenerator(rescale=1./255)

#インスタンスからメソッドを呼び出し
train_generator=train_datagen.flow_from_directory(train_dir,target_size=(150,150),batch_size=20,class_mode='binary')
validation_generator=test_datagen.flow_from_directory(validation_dir,target_size=(150,150),batch_size=20,class_mode='binary')

#shapeを表示してみる
for data_batch,labels_batch in train_generator:
    print('data batch shape:',data_batch.shape)
    print('label batch_shape:',labels_batch.shape)
    break

#batch generaterを用いてモデルを適合
history=model.fit_generator(train_generator,steps_per_epoch=100,epochs=30,validation_data=validation_generator,validation_steps=50)

#訓練の後はモデルを保存する
model.save('cats_and_dogs_small_1.h5')

#訓練データと検証データセットで正解率をプロット
import matplotlib.pyplot as plt

acc=history.history['acc']
val_acc=history.history['val_acc']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(1,len(acc)+1)

#正解率をプロット
plt.plot(epochs,acc,'bo',label='Training acc')
plt.plot(epochs,val_acc,'b',label='Valiation acc')
plt.title('Training and Validation accuracy')
plt.legend()

plt.figure()

#損失をプロット
plt.plot(epochs,loss,'bo',label='Train loss')
plt.plot(epochs,val_loss,'b',label='Validation loss')
plt.title('Tarining and Validation loss')
plt.legend()

plt.show()

#過学習が確認できる
#データの水増しを行い改善を図る

#データ拡張
#ImageDataGeneratorで訓練するデータを生成する
datagen=ImageDataGenerator(rotation_range=40,width_shift_range=0.2,height_shift_range=0.2,shear_range=0.2,horizontal_flip=True,fill_mode='nearest')
#rotation_range:画像をランダムに回転(0~180)
#width_shift:平行移動
#shear_range:等積変形をランダムに変形
#zoom_range:図形の内側にズーム
#horizotal_flip:画像の半分を水平方向にランダムに反転
#fill_mode:新たに作成されたピクセルを埋めるための戦略

#ランダムに水増しされた画像の表示
#画像処理モジュールのimageのimport 
from keras.preprocessing import image
#lsitdir:パスないのすべてのファイルを指定する
fnames=[os.path.join(train_cats_dir,fname) for fname in os.listdir(train_cats_dir)]

#水増しする画像を選択
img_path=fnames[3]

#画像を読み込みサイズを変更
#(150,150)で読み込み
#load_img;読み込み、デフォルトではRGBのPIL形式で読み込み
img=image.load_img(img_path,target_size=(150,150))

#形状が(150,150,3)のnumpy配列に変換
x=image.img_to_array(img)
#(1,150,150,3)に変更
x=x.reshape((1,)+x.shape)

#ランダムに変換いsた画像のバッチを生成する
#無限ループになるため何らかのタイミングでbreak
i=0
#flow:拡張されたデータを返す
for batch in datagen.flow(x,batch_size=1):
    plt.figure(i)
    imgplot=plt.imshow(image.array_to_img(batch[0]))
    i+=1
    if i%4==0:
        break

plt.show()

#Dropoutが追加された新たなCNNを定義する
from keras import layers
from keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
#Dropout層を追加
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])


#データ拡張とDropoutを適用したCNNを訓練
train_datagen=ImageDataGenerator(rescale=1./255,rotation_range=40,width_shift_range=0.2,height_shift_range=0.2,shear_range=0.2,horizontal_flip=True)
#テストデータは水増ししない
test_datagen=ImageDataGenerator(rescale=1./255)

train_generator=train_datagen.flow_from_directory(
    train_dir,
    target_size=(150,150),
    batch_size=32,
    class_mode='binary')

validation_generator=test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150,150),
    batch_size=32,
    class_mode='binary')

history=model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=50)
    
model.save('cats_and_dogs_small_2.f5')


