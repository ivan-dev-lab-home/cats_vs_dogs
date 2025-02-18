import os
from pathlib import Path
from keras.preprocessing.image import ImageDataGenerator
from src.create_model import create_model
  
ROOT_DIR = "D:/!BackUp/программирование/python/Ai/данные/cats_vs_dogs"
train_dir, val_dir, test_dir = os.path.join(ROOT_DIR, "train"), os.path.join(ROOT_DIR, "val"), os.path.join(ROOT_DIR, "test")
train_size, val_size, test_size = len(list(Path(train_dir).rglob("*.jpg"))), len(list(Path(val_dir).rglob("*.jpg"))), len(list(Path(test_dir).rglob("*.jpg")))

if len(list(Path(os.path.join(ROOT_DIR, "images")).rglob("*.jpg"))) > train_size+val_size+test_size:
    raise ValueError("Каталоги с тренировочной, валидационной и тестовой выборками не заполнены до конца")
elif len(list(Path(os.path.join(ROOT_DIR, "images")).rglob("*.jpg"))) < train_size+val_size+test_size:
    raise ValueError("Каталоги с тренировочной, валидационной и тестовой выборками содержат больше файлов, чем исходный каталог")
else:
    img_width, img_height = 32, 32
    
    # проверка наличия сохраненной модели. Если сохраненных моделей в каталоге models/ нет, то будет процесс обучения
    if len(os.listdir("./models/")) == 1:
        input_shape = (img_width, img_height, 3)

        data_gen = ImageDataGenerator(rescale=1/255)
        batch_size = 32

        train_gen = data_gen.flow_from_directory(
            directory=train_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode="binary"
        )

        val_gen = data_gen.flow_from_directory(
            directory=val_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode="binary"
        )

        test_gen = data_gen.flow_from_directory(
            directory=test_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode="binary"
        )

        model = create_model(input_shape)

        model.fit(
            train_gen,
            steps_per_epoch=train_size//batch_size,
            epochs=30,
            validation_data=val_gen,
            validation_steps=val_size//batch_size
        )

        scores = model.evaluate(
            test_gen,
            steps=test_size//batch_size
        )

        print(f"Точность модели на тестовых данных = {scores[1]*100}%")

        model.save("models/Classification.h5")
    