import numpy as np
from sklearn.linear_model import LinearRegression
from rest_framework import viewsets
from sklearn.metrics import mean_squared_error
from rest_framework.response import Response
import orjson

class GuessPrice(viewsets.ViewSet):
    def get_guess_price(self, request):
        data = orjson.loads(request.body)
        list_real_estate = data.get("list_real_estate")

        squads = [i[0] for i in list_real_estate]
        prices = [i[1] for i in list_real_estate]
        squads_temp = np.reshape(squads, (-1, 1))

        model = LinearRegression()
        model.fit(squads_temp, prices)

        r_sq = model.score(squads_temp, prices)
        print('coefficient of determination:', r_sq)
        print('intercept:(b0)', model.intercept_)
        print('slope:(b1)', model.coef_)
        prices_pred = model.predict(squads_temp)

        delta = mean_squared_error(squads, prices)

        result = {
            "coefficient of determination": r_sq,
            "intercept": model.intercept_,
            "slope": model.coef_,
            "delta": delta
        }
        return Response(result)
