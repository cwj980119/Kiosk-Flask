from inception_resnet_v1_lcl import *
from keras.models import Model
from keras.layers import *
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
import os

class Make_model():
    def __init__(self):
        return("makemodel")

    def makemodel(self):
        history = self.parent.my_model.fit(self.train_generator,
                                         steps_per_epoch=len(self.train_generator),
                                         epochs=self.epochs,
                                         validation_data=self.val_generator,
                                         validation_steps=len(self.val_generator),
                                         callbacks=[self.checkpoint])
        #이름 변경
        self.my_model.save('face_model.h5')
        print("model saved")


class Learnig():
    def __init__(self):
        #경로수정
        path = './image/dataset/train'
        file_list = os.listdir(path)
        self.len = len(file_list)
        self.init_model()
   
    def init_model(self):
        #수정필요
        base_model = InceptionResNetV1(weights_path='./facenet_keras_weights.h5',
                                       input_shape=(224, 224, 3),
                                       dropout_keep_prob=0.8)

        for layer in base_model.layers[:]:
            layer.trainable = False

        #base_model.summary()

        classes = self.len
        self.epochs = 20
        # epochs = 500
        targetx = 224
        targety = 224

        x = base_model.get_layer(index=442).output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        x = Dense(1024, activation='relu', kernel_initializer='he_normal', bias_initializer='zeros')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        predictions = Dense(classes, activation='softmax')(x)

        self.my_model = Model(inputs=base_model.input, outputs=predictions)
        #my_model.summary()

        # making the instance of 'ImageDataGenerator'
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=30,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True,
                                           fill_mode='nearest')

        val_datagen = ImageDataGenerator(rescale=1. / 255)

        # setting the path of datasets
        train_dir = './image/train'
        val_dir = './image/test'

        self.train_generator = train_datagen.flow_from_directory(train_dir,
                                                            batch_size=200,
                                                            target_size=(targetx, targety),
                                                            shuffle=True,
                                                            class_mode='categorical')

        self.val_generator = val_datagen.flow_from_directory(val_dir,
                                                        batch_size=100,
                                                        target_size=(targetx, targety),
                                                        shuffle=True,
                                                        class_mode='categorical')
        checkpoint_dir = "./model"
        os.makedirs(checkpoint_dir, exist_ok=True)
        self.checkpoint = ModelCheckpoint(filepath=checkpoint_dir + "/" + "weight_1.hdf5",
                                     monitor='loss',
                                     mode='min',
                                     save_best_only=True)

        self.my_model.compile(optimizer='adam',
                         loss="categorical_crossentropy",
                         metrics=["accuracy"])

        print("1")
        self.learn_model()
    