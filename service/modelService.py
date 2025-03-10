from pathlib import Path

import dill
from .api.exception import ModelNotFoundError


class ModelService:
    def __init__(self) -> None:
        self.user_knn = None
        self.popular_model = None
        self._load_user_knn()
        self._load_popular_model()

    def _load_user_knn(self):
        try:
            with open(Path("", "./user_knn.dill"), "rb") as f:
                self.user_knn = dill.load(f)
        except Exception:
            raise ModelNotFoundError

    def _load_popular_model(self):
        try:
            with open(Path("", "./popular.dill"), "rb") as f:
                self.popular_model = dill.load(f)
        except Exception:
            raise ModelNotFoundError

    def get_user_knn_prediction(self, id):
        return self.user_knn.recommend(int(id), N_recs=10)

    def get_popular_prediction(self):
        return list(self.popular_model.popularity_list[0][:10])
