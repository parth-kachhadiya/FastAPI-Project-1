import joblib
import numpy as np
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import getCachedPrediction, setCache


model = joblib.load(settings.MODEL_LOCATION)
preprocessor = joblib.load(settings.PREPROCESSOR_LOCATION)

def predictPrice(data : dict):
    cache_key = " ".join([str(val) for val in data.values()])
    cachedResult = getCachedPrediction(cache_key)

    if cachedResult:
        return cachedResult

    framed_input = pd.DataFrame([data])

    transformed_data = preprocessor.transform(framed_input)
    log_prediction = model.predict(transformed_data)
    predicted_price = float(np.expm1(log_prediction[0]))

    setCache(cache_key, predicted_price)

    return predicted_price
