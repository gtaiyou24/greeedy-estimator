import pickle

from pathlib import Path
from typing import NoReturn

import numpy as np
import pandas as pd
from injector import singleton, inject
from keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from slf4py import set_logger

from application.estimator.command import PredictCommand
from application.estimator.dpo import LoadEstimatorDpo, PredictedColorsDpo
from domain.model.color import Color
from domain.model.dataset import DatasetStorageService
from domain.model.estimator.color import ColorEstimator
from domain.model.feature import FeaturesFactory, Feature
from domain.model.image.url import ImageUrl
from port.adapter.service.dataset import DatasetStorageServiceImpl


@singleton
@set_logger
class EstimatorApplicationService:
    @inject
    def __init__(self, dataset_storage_service: DatasetStorageService):
        self.__dataset_storage_service = dataset_storage_service
        self.__features_factory = FeaturesFactory({'アイテム名': Feature.ItemName, '画像URL': Feature.ItemImage})

    def train(self, dataset_path: Path, artifact_path: Path) -> NoReturn:
        self.log.debug('start training')

        self.log.debug(isinstance(self.__dataset_storage_service, DatasetStorageServiceImpl))

        dataset = self.__dataset_storage_service.load(dataset_path.joinpath(Path('items.csv')))
        dataset = dataset[~dataset['カラー'].isnull()][['アイテム名', '画像URL', 'カラー']]

        # 学習データとテストデータに分ける
        train_dataset, test_dataset = train_test_split(dataset, test_size=0.3, shuffle=True, random_state=0)

        self.log.debug('データセットをダウンロードしました！')

        X_train, train_index = self.__features_factory.make(train_dataset)
        X_test, test_index = self.__features_factory.make(test_dataset)

        # ベクトル変換器の学習
        text_vectorizer = CountVectorizer()
        text_vectorizer.fit(X_train[:, 0])

        X_train = [np.array([x for x in X_train[:, 1]]), text_vectorizer.transform(X_train[:, 0]).toarray()]
        X_test = [np.array([x for x in X_test[:, 1]]), text_vectorizer.transform(X_test[:, 0]).toarray()]

        self.log.debug('特徴量データを生成しました！')

        Y_train = np.array([Color.value_of_ja_name(y).id() for y in train_dataset.iloc[train_index]['カラー']])
        Y_test = np.array([Color.value_of_ja_name(y).id() for y in test_dataset.iloc[test_index]['カラー']])

        n_class = len([e for e in Color])
        Y_train = to_categorical(Y_train.reshape((-1, 1)), n_class)
        Y_test = to_categorical(Y_test.reshape((-1, 1)), n_class)

        self.log.debug('教師データを生成しました！')

        self.log.debug('学習を開始します')

        estimator = ColorEstimator(
            ColorEstimator.TextLayer(len(text_vectorizer.get_feature_names_out())),
            ColorEstimator.ImageLayer(300, 300, 3),
            n_class
        )
        estimator.fit((X_train, X_test), (Y_train, Y_test))

        self.log.debug('学習が完了しました！')

        # TODO : テストデータ(test_items.csv)を用いてモデルを評価する

        with open(artifact_path / 'estimator.pkl', 'wb') as pkl:
            self.log.debug(f"save {estimator.name()}-{estimator.version()} to {artifact_path / 'estimator.pkl'}")
            pickle.dump(estimator, pkl)

        with open(artifact_path / 'text_vectorizer.pkl', 'wb') as pkl:
            self.log.debug(f"save text_vectorizer to {artifact_path / 'text_vectorizer.pkl'}")
            pickle.dump(text_vectorizer, pkl)

    def load(self, artifact_path: Path) -> LoadEstimatorDpo:
        with open(artifact_path / 'estimator.pkl', 'rb') as pkl:
            estimator = pickle.load(pkl)

        with open(artifact_path / 'text_vectorizer.pkl', 'rb') as pkl:
            text_vectorizer = pickle.load(pkl)

        return LoadEstimatorDpo(estimator, text_vectorizer)

    def predict(self, command: PredictCommand) -> PredictedColorsDpo:
        dataset = pd.DataFrame([{'アイテム名': item.name, '画像URL': item.image_url} for item in command.items])
        items = {i: {'url': dataset.loc[i, '画像URL'], 'color': Color.Unknown} for i in dataset.index}

        X, index = self.__features_factory.make(dataset)

        X = [np.array([x for x in X[:, 1]]), command.vectorizer.transform(X[:, 0]).toarray()]

        for i, y in zip(index, command.estimator.predict(X)):
            y_ser = pd.Series(y, index=[e.id() for e in Color])
            if command.option_colors:
                y_ser = y_ser[command.option_colors]
            items[i]['color'] = Color.value_of(int(y_ser.idxmax()) - 1)

        return PredictedColorsDpo(
            [PredictedColorsDpo.Predicted(ImageUrl(item['url']), item['color']) for item in items.values()]
        )
