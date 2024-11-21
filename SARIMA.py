import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_excel('your file_path', parse_dates=['Date'], index_col='Date', date_parser=lambda x: pd.to_datetime(x, format='%Y/%m'))

# 设置时间序列频率为每月
data = data.asfreq('MS')

# 数据分割
train = data['2009':'2016']
test = data['2017':'2019']

# 数据预处理：对数变换
train_log = np.log(train['PE'])
test_log = np.log(test['PE'])

# 季节性分解
decomposition = sm.tsa.seasonal_decompose(train_log, model='additive')
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# 绘制分解结果
plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(train_log, label='Original (Log)')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# 平稳性检验
def adf_test(series):
    result = adfuller(series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

# 检验原始数据的平稳性
print("ADF Test for Original Data (Log):")
adf_test(train_log)

# 检验去除季节项和周期项后的数据的平稳性
print("ADF Test for Residuals (Log):")
adf_test(residual.dropna())

# 白噪声检验
def ljung_box_test(series, lags=10):
    result = acorr_ljungbox(series, lags=[lags])
    print('Ljung-Box Statistic: %f' % result.lb_stat.values[0])
    print('p-value: %f' % result.lb_pvalue.values[0])

# 检验去除季节项和周期项后的数据的白噪声性
print("Ljung-Box Test for Residuals (Log):")
ljung_box_test(residual.dropna())

# ACF和PACF图
plot_acf(residual.dropna())
plot_pacf(residual.dropna())
plt.show()

# 模型定阶
def optimize_arima(order_list, exog):
    results = []
    for order in order_list:
        try:
            model = sm.tsa.SARIMAX(exog, order=order, seasonal_order=(1, 1, 1, 12))
            result = model.fit(maxiter=500, method='bfgs', disp=False)
            aic = result.aic
            results.append([order, aic])
        except:
            continue
    results_df = pd.DataFrame(results, columns=['order', 'aic'])
    return results_df.sort_values(by='aic', ascending=True).head()

order_list = [(p, d, q) for p in range(3) for d in range(2) for q in range(3)]
best_order = optimize_arima(order_list, train_log).iloc[0]['order']
print("Best Order:", best_order)

# 模型训练
model = sm.tsa.SARIMAX(train_log, order=best_order, seasonal_order=(1, 1, 1, 12))
result = model.fit(maxiter=500, method='bfgs', disp=False)
print(result.summary())

# 残差自相关图检验
residuals = result.resid
plot_acf(residuals)
plt.show()

# 预测
forecast = result.get_forecast(steps=len(test))
forecast_conf_int = forecast.conf_int()
forecast_mean = forecast.predicted_mean

# 将预测结果从对数变换还原
forecast_mean_exp = np.exp(forecast_mean)
forecast_conf_int_exp = np.exp(forecast_conf_int)

# 计算RMSE
rmse = np.sqrt(mean_squared_error(test['PE'], forecast_mean_exp))
print('RMSE: %.4f' % rmse)

# 输出预测结果到Excel
output = pd.DataFrame({
    'Date': test.index,
    'Actual': test['PE'],
    'Predicted': forecast_mean_exp
})
output.to_excel('your output_file_path', index=False)

# 绘制预测结果和测试集数据的比较图
plt.figure(figsize=(12, 6))
plt.plot(train['PE'], label='Train')
plt.plot(test['PE'], label='Test')
plt.plot(forecast_mean_exp, label='Predicted', color='red')
plt.fill_between(forecast_conf_int_exp.index, forecast_conf_int_exp.iloc[:, 0], forecast_conf_int_exp.iloc[:, 1], color='pink', alpha=0.3)
plt.title('Actual vs Predicted')
plt.legend(loc='best')
plt.show()